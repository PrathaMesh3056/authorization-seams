"""Eq. 2-9 interpreter. No compiler, eval, subprocess, network, or native tools.

Pure state transitions are for a single sequential harness. Gateway serializes
authoritative state and certificate use within one process. See ASSUMPTIONS.md.
"""
from collections import Counter
from decimal import Decimal
import hashlib
import hmac
import json
import math
import re
import secrets
from threading import RLock
from typing import Callable

from .models import (
    ArgumentProof, Binding, CallRequest, CertificateEntry, Constraint, Contract,
    Decision, DecisionCode, EffectCertificate, EffectReceipt, EvidenceRecord,
    Ledger, NativeResult, Obligation, ObligationState as OS, Registry,
    RuntimeState, StaticResult, ValueType,
)


def canon(value) -> str:
    """No coercion, NaN, Unicode normalization, or default insertion."""
    def plain(item):
        if hasattr(item, 'model_dump'):
            return item.model_dump(mode='json')
        if isinstance(item, dict):
            return {k: plain(v) for k, v in item.items()}
        if isinstance(item, (list, tuple)):
            return [plain(v) for v in item]
        return item
    value = plain(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False)


def digest(value) -> str:
    return hashlib.sha256(canon(value).encode('utf-8')).hexdigest()


def same(a, b) -> bool:
    return canon(a) == canon(b)


def type_matches(value, expected: ValueType) -> bool:
    return {
        ValueType.STRING: lambda: type(value) is str,
        ValueType.INTEGER: lambda: type(value) is int,
        ValueType.NUMBER: lambda: type(value) in (int, float) and math.isfinite(value),
        ValueType.BOOLEAN: lambda: type(value) is bool,
        ValueType.OBJECT: lambda: type(value) is dict,
        ValueType.ARRAY: lambda: type(value) is list,
    }[expected]()


def satisfies(value, rule: Constraint) -> bool:
    if not type_matches(value, rule.type):
        return False
    if rule.has_equals and not same(value, rule.equals):
        return False
    if rule.choices is not None and not any(same(value, x) for x in rule.choices):
        return False
    if rule.minimum is not None and (type(value) not in (int, float) or value < rule.minimum):
        return False
    if rule.maximum is not None and (type(value) not in (int, float) or value > rule.maximum):
        return False
    return True


def constraint_valid(rule: Constraint) -> bool:
    if any(x is not None and not math.isfinite(x) for x in (rule.minimum, rule.maximum)):
        return False
    if (rule.minimum is not None or rule.maximum is not None) and rule.type not in (
            ValueType.INTEGER, ValueType.NUMBER):
        return False
    if rule.minimum is not None and rule.maximum is not None and rule.minimum > rule.maximum:
        return False
    if rule.choices is not None and (not rule.choices or not all(
            type_matches(x, rule.type) for x in rule.choices)):
        return False
    if rule.has_equals and not satisfies(rule.equals, rule):
        return False
    if rule.choices is not None and not any(satisfies(x, rule) for x in rule.choices):
        return False
    return True


def normalize(contract: Contract) -> Contract:
    data = contract.model_dump(mode='json')
    data['MUST'] = sorted(data['MUST'], key=lambda o: o['id'])
    for obligation in data['MUST']:
        obligation['dependencies'] = sorted(set(obligation['dependencies']))
    for permission in data['MAY'].values():
        permission['allowed_args'] = sorted(set(permission['allowed_args']))
    return Contract.model_validate(json.loads(canon(data)))


def ancestors(obligation: Obligation, nodes: dict[str, Obligation]) -> set[str]:
    seen, todo = set(), list(obligation.dependencies)
    while todo:
        node = todo.pop()
        if node not in seen:
            seen.add(node)
            todo.extend(nodes[node].dependencies)
    return seen


def static_analyze(contract: Contract, registry: Registry,
                   binding_mode: str = 'complete') -> StaticResult:
    """Algorithm 1, ordered rejection; no executable state on rejection."""
    if binding_mode not in ('complete', 'diagnostic_coverage_gap'):
        raise ValueError('unknown binding mode')
    checks = {}
    try:
        c = normalize(contract)
        canon(registry)
    except (ValueError, TypeError) as exc:
        return StaticResult(accepted=False, failed_predicate='WellFormed', reasons=[str(exc)])
    nodes = {o.id: o for o in c.MUST}

    def reject(predicate, errors):
        checks[predicate] = not errors
        if errors:
            return StaticResult(accepted=False, failed_predicate=predicate,
                                reasons=errors, checks=checks, normalized=c)
        return None

    errors = []
    if not c.MUST or len(nodes) != len(c.MUST):
        errors.append('empty graph or duplicate obligation id')
    for tool, permission in c.MAY.items():
        schema = registry.tools.get(tool)
        if schema is None:
            errors.append(f'unknown MAY tool {tool}')
            continue
        if set(permission.allowed_args) - set(schema.args):
            errors.append(f'unknown allowed argument on {tool}')
        if not {a for a, spec in schema.args.items() if spec.required} <= set(permission.allowed_args):
            errors.append(f'MAY excludes required argument on {tool}')
        for arg, constraint in permission.constraints.items():
            if arg not in permission.allowed_args or constraint.type != schema.args[arg].type:
                errors.append(f'MAY type/reference mismatch {tool}.{arg}')
        for arg, value in permission.trusted_payloads.items():
            if arg not in schema.args or schema.args[arg].role != 'payload' or not type_matches(value, schema.args[arg].type):
                errors.append(f'bad trusted payload {tool}.{arg}')
    for o in c.MUST:
        if set(o.dependencies) - set(nodes):
            errors.append(f'unknown dependency for {o.id}')
        if o.kind == 'output':
            if o.tool is not None or o.evidence is not None:
                errors.append(f'output {o.id} has tool/evidence')
            continue
        schema = registry.tools.get(o.tool)
        if o.tool not in c.MAY or schema is None:
            errors.append(f'unknown/unpermitted obligation tool {o.id}')
            continue
        if schema.kind != ('query' if o.kind == 'evidence' else 'effect'):
            errors.append(f'tool kind mismatch {o.id}')
        if o.kind == 'evidence':
            rule = o.evidence
            if rule is None or not schema_args_valid(rule.query_args, schema):
                errors.append(f'invalid evidence query {o.id}')
            else:
                for field, constraint in rule.fields.items():
                    if field not in schema.result_fields or constraint.type != schema.result_fields[field]:
                        errors.append(f'evidence field type/reference {o.id}.{field}')
                for field, value in rule.integrity.items():
                    if field not in schema.result_fields or not type_matches(value, schema.result_fields[field]):
                        errors.append(f'integrity type/reference {o.id}.{field}')
        elif o.evidence is not None:
            errors.append(f'effect has evidence query {o.id}')
    for oid, bindings in c.BIND.items():
        if oid not in nodes or nodes[oid].kind != 'effect':
            errors.append(f'unknown BIND effect {oid}')
            continue
        schema = registry.tools.get(nodes[oid].tool)
        if schema is None:
            continue
        for arg, b in bindings.items():
            if arg not in schema.args or schema.args[arg].role != 'authority' or b.constraints.type != schema.args[arg].type:
                errors.append(f'BIND type/reference {oid}.{arg}')
            if b.source == 'constant':
                if b.evidence_obligation is not None or b.field is not None or b.selector is not None or b.derivation != 'copy':
                    errors.append(f'nonconstant rule in constant binding {oid}.{arg}')
                if not type_matches(b.constant, b.constraints.type):
                    errors.append(f'constant type mismatch {oid}.{arg}')
            elif b.evidence_obligation not in nodes or nodes[b.evidence_obligation].kind != 'evidence' or not b.field:
                errors.append(f'bad evidence binding reference {oid}.{arg}')
    for oid in c.VERIFY:
        if oid not in nodes or nodes[oid].kind != 'effect':
            errors.append(f'unknown VERIFY effect {oid}')
    failure = reject('WellFormed', errors)
    if failure:
        return failure

    reachable = set()
    while True:
        additions = {o.id for o in c.MUST if o.enabled and set(o.dependencies) <= reachable}
        if additions <= reachable:
            break
        reachable |= additions
    # Topological elimination over all nodes distinguishes cycles from disabled roots.
    ordered = set()
    while True:
        additions = {o.id for o in c.MUST if set(o.dependencies) <= ordered}
        if additions <= ordered:
            break
        ordered |= additions
    errors = []
    if ordered != set(nodes):
        errors.append('illegal dependency cycle')
    if not {o.id for o in c.MUST if o.hard} <= reachable:
        errors.append('unreachable hard obligation')
    failure = reject('ControlSafe', errors)
    if failure:
        return failure

    effects = [o for o in c.MUST if o.kind == 'effect' and o.id in reachable]
    errors = []
    for o in effects:
        schema = registry.tools[o.tool]
        rules = c.BIND.get(o.id, {})
        required = {a for a, spec in schema.args.items() if spec.role == 'authority'
                    and a in c.MAY[o.tool].allowed_args
                    and (binding_mode == 'complete' or spec.required)}
        if required - set(rules):
            errors.append(f'{o.id}: unbound authority arguments {sorted(required - set(rules))}')
        for arg, b in rules.items():
            if b.source == 'constant':
                continue
            source = nodes[b.evidence_obligation]
            if source.id not in ancestors(o, nodes):
                errors.append(f'{o.id}.{arg}: evidence is not a prerequisite')
            source_schema = registry.tools[source.tool]
            fields = source_schema.result_fields
            if b.selector:
                selection = b.selector
                fields = source_schema.item_fields.get(selection.collection, {})
                if source_schema.result_fields.get(selection.collection) != ValueType.ARRAY:
                    errors.append(f'{o.id}.{arg}: selector requires a structured array')
                if selection.collection not in source.evidence.fields:
                    errors.append(f'{o.id}.{arg}: collection not admitted by evidence rule')
                used = set(selection.where) | {b.field}
                if not used <= set(selection.allowed_fields) or not set(selection.allowed_fields) <= set(fields):
                    errors.append(f'{o.id}.{arg}: unauthorized selector field')
                if any(not type_matches(v, fields[k]) for k, v in selection.where.items() if k in fields):
                    errors.append(f'{o.id}.{arg}: selector value type')
            elif b.field not in source.evidence.fields:
                errors.append(f'{o.id}.{arg}: field not covered by evidence type check')
            source_type = fields.get(b.field)
            if source_type is None:
                errors.append(f'{o.id}.{arg}: unobservable source field')
            elif b.derivation == 'copy' and source_type != b.constraints.type:
                errors.append(f'{o.id}.{arg}: copy changes type')
            elif b.derivation == 'to_integer' and (source_type not in (ValueType.STRING, ValueType.INTEGER) or b.constraints.type != ValueType.INTEGER):
                errors.append(f'{o.id}.{arg}: invalid integer conversion')
            elif b.derivation == 'affine' and (source_type not in (ValueType.INTEGER, ValueType.NUMBER) or b.constraints.type not in (ValueType.INTEGER, ValueType.NUMBER)):
                errors.append(f'{o.id}.{arg}: invalid numeric derivation')
    failure = reject('FlowSafe', errors)
    if failure:
        return failure

    errors = []
    counts = Counter(o.tool for o in c.MUST if o.hard and o.enabled and o.tool)
    for tool, permission in c.MAY.items():
        if permission.budget < counts[tool]:
            errors.append(f'{tool}: budget cannot cover hard obligations')
        if any(not constraint_valid(rule) for rule in permission.constraints.values()):
            errors.append(f'{tool}: inconsistent MAY constraint')
        for o in c.MUST:
            if o.tool != tool:
                continue
            if o.evidence and (not may_arguments(o.evidence.query_args, permission, registry.tools[tool]) or
                               any(not constraint_valid(rule) for rule in o.evidence.fields.values())):
                errors.append(f'{o.id}: query/evidence contradicts scope')
            for arg, b in c.BIND.get(o.id, {}).items():
                if arg not in permission.allowed_args or not constraint_valid(b.constraints):
                    errors.append(f'{o.id}.{arg}: BIND contradicts scope')
                if b.source == 'constant' and (not satisfies(b.constant, b.constraints) or
                       (arg in permission.constraints and not satisfies(b.constant, permission.constraints[arg]))):
                    errors.append(f'{o.id}.{arg}: constant outside scope')
                # Dynamic ranges must have at least one common point.
                if arg in permission.constraints and not constraints_overlap(b.constraints, permission.constraints[arg]):
                    errors.append(f'{o.id}.{arg}: disjoint BIND/MAY ranges')
    failure = reject('ScopeSafe', errors)
    if failure:
        return failure

    errors = []
    for o in effects:
        verification = c.VERIFY.get(o.id)
        fields = registry.tools[o.tool].result_fields
        if verification is None or not verification.postconditions:
            errors.append(f'{o.id}: missing observable verification')
        elif any(k not in fields or not type_matches(v, fields[k]) for k, v in verification.postconditions.items()):
            errors.append(f'{o.id}: unobservable/ill-typed postcondition')
    failure = reject('VerifySafe', errors)
    if failure:
        return failure
    return StaticResult(accepted=True, normalized=c, checks=checks)


def constraints_overlap(a: Constraint, b: Constraint) -> bool:
    if a.type != b.type:
        return False
    for rule in (a, b):
        finite = [rule.equals] if rule.has_equals else rule.choices
        if finite is not None:
            return any(satisfies(v, a) and satisfies(v, b) for v in finite)
    low = max(x for x in (a.minimum, b.minimum, -math.inf) if x is not None)
    high = min(x for x in (a.maximum, b.maximum, math.inf) if x is not None)
    return low <= high and (a.type != ValueType.INTEGER or low == -math.inf or high == math.inf or math.ceil(low) <= math.floor(high))


def schema_args_valid(args, schema) -> bool:
    return (not set(args) - set(schema.args) and
            all(not spec.required or name in args for name, spec in schema.args.items()) and
            all(type_matches(v, schema.args[k].type) for k, v in args.items()))


def may_arguments(args, permission, schema) -> bool:
    return (schema_args_valid(args, schema) and set(args) <= set(permission.allowed_args) and
            all(k not in args or satisfies(args[k], rule) for k, rule in permission.constraints.items()))


def refresh(state: RuntimeState):
    for o in state.contract.MUST:
        if o.enabled and state.ledger.S[o.id] == OS.PENDING and all(
                state.ledger.S[d] in (OS.VERIFIED, OS.WAIVED) for d in o.dependencies):
            state.ledger.S[o.id] = OS.ACTIVE


def establish(contract: Contract, registry: Registry, session: str,
              binding_mode: str = 'complete') -> RuntimeState:
    analysis = static_analyze(contract, registry, binding_mode)
    if not analysis.accepted:
        raise ValueError(f'{analysis.failed_predicate}: {analysis.reasons}')
    c = analysis.normalized
    state = RuntimeState(contract=c, registry=registry.model_copy(deep=True),
                         contract_digest=digest(c), registry_digest=digest(registry),
                         session=session, binding_mode=binding_mode,
                         ledger=Ledger(S={o.id: OS.PENDING for o in c.MUST},
                                       B={t: p.budget for t, p in c.MAY.items()}))
    refresh(state)
    return state


def frozen(state):
    if digest(state.contract) != state.contract_digest or digest(state.registry) != state.registry_digest:
        raise ValueError('frozen contract/registry changed')


def obligation(state, oid):
    return next((o for o in state.contract.MUST if o.id == oid), None)


def evidence_qualifies(record: EvidenceRecord, o: Obligation, state: RuntimeState) -> bool:
    rule = o.evidence
    if o.kind != 'evidence' or rule is None or record.obligation != o.id or record.tool != o.tool:
        return False
    if not same(record.query_args, rule.query_args):
        return False
    if not all(k in record.data and satisfies(record.data[k], constraint) for k, constraint in rule.fields.items()):
        return False
    if not all(k in record.data and same(record.data[k], v) for k, v in rule.integrity.items()):
        return False
    schema = state.registry.tools[o.tool]
    for collection, fields in schema.item_fields.items():
        if collection in record.data:
            rows = record.data[collection]
            if type(rows) is not list or any(type(row) is not dict or not all(
                    k in row and type_matches(row[k], typ) for k, typ in fields.items()) for row in rows):
                return False
    return True


def admit_evidence(record: EvidenceRecord, state: RuntimeState) -> tuple[bool, RuntimeState]:
    """Eq. 4. Query budget counts the protected query represented by this result."""
    frozen(state)
    new = state.model_copy(deep=True)
    o = obligation(new, record.obligation)
    if o is None or o.kind != 'evidence':
        return False, new
    # A modeled native query uses budget even if its result fails admission.
    if record.tool != o.tool or not same(record.query_args, o.evidence.query_args) or new.ledger.B[o.tool] <= 0:
        return False, new
    new.ledger.B[o.tool] -= 1
    accepted = (new.ledger.S[o.id] == OS.ACTIVE and record.id not in new.ledger.E and
                evidence_qualifies(record, o, new))
    if accepted:
        new.ledger.E[record.id] = record.model_copy(deep=True)
        new.ledger.S[o.id] = OS.VERIFIED
        refresh(new)
    return accepted, new


def derived_value(b: Binding, record: EvidenceRecord | None):
    extra = {}
    if b.source == 'constant':
        value = b.constant
    else:
        data = record.data
        if b.selector:
            s = b.selector
            rows = data[s.collection]
            matches = [row for row in rows if all(k in row and same(row[k], v) for k, v in s.where.items())]
            if len(matches) != 1:
                raise ValueError('selector did not yield exactly one record')
            data = matches[0]
            extra = dict(candidate_set_digest=digest(rows), selector_digest=digest(s),
                         selected_record_digest=digest(data))
        value = data[b.field]
        if b.derivation == 'to_integer':
            if type(value) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)', value):
                value = int(value)
            elif type(value) is not int:
                raise ValueError('noncanonical integer')
        elif b.derivation == 'affine':
            if type(value) not in (int, float):
                raise ValueError('non-numeric affine input')
            computed = Decimal(str(value)) * b.multiplier + b.offset
            if b.constraints.type == ValueType.INTEGER:
                if computed != computed.to_integral_value():
                    raise ValueError('lossy arithmetic')
                value = int(computed)
            else:
                value = float(computed)
    if not satisfies(value, b.constraints):
        raise ValueError('derived value outside BIND constraints')
    return value, extra


def argument_proofs(request: CallRequest, oid: str, state: RuntimeState):
    schema = state.registry.tools[request.tool]
    rules = state.contract.BIND.get(oid, {})
    required = {arg for arg in request.arguments if schema.args[arg].role == 'authority'
                and (state.binding_mode == 'complete' or arg in rules or schema.args[arg].required)}
    proofs, missing = {}, []
    for arg in sorted(required):
        b = rules.get(arg)
        try:
            if b is None:
                raise ValueError('missing BIND rule')
            record = None
            if b.source == 'evidence':
                records = [r for r in state.ledger.E.values() if r.obligation == b.evidence_obligation]
                if len(records) != 1 or state.ledger.S[b.evidence_obligation] != OS.VERIFIED:
                    raise ValueError('missing admitted record')
                record = records[0]
                if not evidence_qualifies(record, obligation(state, b.evidence_obligation), state):
                    raise ValueError('record no longer qualifies')
            value, selection = derived_value(b, record)
            if not same(value, request.arguments[arg]):
                raise ValueError('candidate differs from deterministic derivation')
            proofs[arg] = ArgumentProof(argument=arg, value=value, binding_digest=digest(b),
                                        evidence_id=record.id if record else None,
                                        evidence_digest=digest(record) if record else None, **selection)
        except (ValueError, KeyError, TypeError, OverflowError) as exc:
            missing.append(f'{arg}: {exc}')
    return proofs, missing


RISK = re.compile(r'<script\b|javascript:|\b(?:eval|exec)\s*\(|\b(?:bash|powershell|cmd)\s+-|'
                  r'ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions|'
                  r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|\b(?:password|api[_ -]?key)\s*[:=]', re.I)


def check_call(request: CallRequest, state: RuntimeState) -> tuple[Decision, RuntimeState]:
    """Harness interface; Eq. 5. Authorization alone never spends effect budget."""
    frozen(state)
    new = state.model_copy(deep=True)
    schema = new.registry.tools.get(request.tool)
    permission = new.contract.MAY.get(request.tool)
    H = False
    if schema and permission:
        H = any(arg in request.arguments and arg in schema.args and schema.args[arg].role == 'payload'
                and (arg not in permission.trusted_payloads or not same(request.arguments[arg], permission.trusted_payloads[arg]))
                and RISK.search(canon(request.arguments[arg])) is not None for arg in request.tainted_payloads)
    M = bool(schema and schema.kind == 'effect' and permission and may_arguments(request.arguments, permission, schema))
    matching = [o for o in new.contract.MUST if o.kind == 'effect' and o.tool == request.tool
                and new.ledger.S[o.id] == OS.ACTIVE and (request.obligation is None or request.obligation == o.id)]
    O = len(matching) == 1
    B = new.ledger.B.get(request.tool, 0) > 0
    proofs, missing = ({}, [])
    if M and O:
        proofs, missing = argument_proofs(request, matching[0].id, new)
    P = M and O and not missing
    code = (DecisionCode.STEP_UP_AUTH if H else DecisionCode.ALLOW if M and O and P and B
            else DecisionCode.PROOF_GAP if M and O and B and not P else DecisionCode.DENY)
    return Decision(code=code, checks=dict(H=H, M=M, O=O, P=P, B=B), missing=missing,
                    obligation=matching[0].id if O else None, proofs=proofs), new


def certificate_mac(cert: EffectCertificate, key: bytes) -> str:
    data = cert.model_dump(mode='json', exclude={'mac'})
    return hmac.new(key, canon(data).encode('utf-8'), hashlib.sha256).hexdigest()


def issue_certificate(request: CallRequest, state: RuntimeState, key: bytes,
                      now: int, ttl: int = 60) -> tuple[EffectCertificate, RuntimeState]:
    if len(key) < 32 or ttl <= 0:
        raise ValueError('HMAC key must have >=32 bytes and TTL must be positive')
    decision, new = check_call(request, state)
    if decision.code != DecisionCode.ALLOW:
        raise ValueError(f'certificate unavailable: {decision.code}')
    if any(e.lifecycle == 'ISSUED' and e.certificate.obligation == decision.obligation
           and e.certificate.expires_at > now for e in new.ledger.K.values()):
        raise ValueError('outstanding unexpired certificate for obligation')
    cert = EffectCertificate(nonce=secrets.token_hex(16), contract_digest=new.contract_digest,
                             registry_digest=new.registry_digest, session=new.session,
                             binding_mode=new.binding_mode,
                             obligation=decision.obligation, tool=request.tool,
                             canonical_arguments=canon(request.arguments), proofs=decision.proofs,
                             budget=new.ledger.B[request.tool], issued_at=now, expires_at=now + ttl)
    cert.mac = certificate_mac(cert, key)
    new.ledger.K[cert.nonce] = CertificateEntry(certificate=cert.model_copy(deep=True))
    return cert, new


def authentic_registered(cert, state, key):
    entry = state.ledger.K.get(cert.nonce)
    return bool(entry and same(entry.certificate, cert) and
                hmac.compare_digest(cert.mac, certificate_mac(cert, key)) and
                cert.contract_digest == state.contract_digest and
                cert.registry_digest == state.registry_digest and cert.session == state.session and
                cert.binding_mode == state.binding_mode)


def validate_certificate(cert: EffectCertificate, request: CallRequest,
                         state: RuntimeState, key: bytes, now: int) -> bool:
    frozen(state)
    if not authentic_registered(cert, state, key):
        return False
    entry = state.ledger.K[cert.nonce]
    if (entry.lifecycle != 'ISSUED' or not cert.issued_at <= now < cert.expires_at or
            request.tool != cert.tool or canon(request.arguments) != cert.canonical_arguments or
            request.obligation not in (None, cert.obligation) or state.ledger.B[cert.tool] != cert.budget):
        return False
    decision, _ = check_call(request.model_copy(update={'obligation': cert.obligation}), state)
    return (decision.code == DecisionCode.ALLOW and same(decision.proofs, cert.proofs))


def dispatch(cert: EffectCertificate, request: CallRequest, state: RuntimeState,
             key: bytes, now: int) -> tuple[bool, RuntimeState]:
    """Eq. 7 transition, consumed before any protected runner invocation."""
    new = state.model_copy(deep=True)
    if not validate_certificate(cert, request, new, key, now):
        return False, new
    entry = new.ledger.K[cert.nonce]
    entry.lifecycle = 'CONSUMED'
    entry.dispatched_at = now
    new.ledger.B[cert.tool] -= 1
    return True, new


def check_receipt(native: NativeResult, cert: EffectCertificate, state: RuntimeState,
                  key: bytes) -> tuple[bool, RuntimeState]:
    """Eq. 8. Protected runner alone supplies NativeResult; no planner claims."""
    frozen(state)
    new = state.model_copy(deep=True)
    if not authentic_registered(cert, new, key):
        return False, new
    entry = new.ledger.K[cert.nonce]
    if entry.lifecycle != 'CONSUMED' or entry.receipt_processed:
        return False, new
    # One native outcome per dispatch, even when unsuccessful.
    entry.receipt_processed = True
    if (native.certificate_nonce != cert.nonce or native.tool != cert.tool or
            canon(native.arguments) != cert.canonical_arguments or not native.success or
            new.ledger.S[cert.obligation] != OS.ACTIVE):
        return False, new
    conditions = new.contract.VERIFY[cert.obligation].postconditions
    schema = new.registry.tools[cert.tool]
    if not all(k in native.result and type_matches(native.result[k], schema.result_fields[k]) and
               same(native.result[k], v) for k, v in conditions.items()):
        return False, new
    request = CallRequest(tool=cert.tool, arguments=native.arguments, obligation=cert.obligation)
    proofs, missing = argument_proofs(request, cert.obligation, new)
    if missing or not same(proofs, cert.proofs):
        return False, new
    new.ledger.receipts[cert.nonce] = EffectReceipt(certificate_nonce=cert.nonce,
                                                obligation=cert.obligation,
                                                native_result_digest=digest(native))
    new.ledger.S[cert.obligation] = OS.VERIFIED
    refresh(new)
    return True, new


def waive(oid: str, code: str, state: RuntimeState) -> RuntimeState:
    frozen(state)
    new = state.model_copy(deep=True)
    o = obligation(new, oid)
    if o is None or o.waiver_code is None or code != o.waiver_code or new.ledger.S[oid] != OS.ACTIVE:
        raise ValueError('no applicable contract exemption')
    new.ledger.waivers[oid] = code
    new.ledger.S[oid] = OS.WAIVED
    refresh(new)
    return new


def verify_output(oid: str, value, state: RuntimeState) -> RuntimeState:
    frozen(state)
    new = state.model_copy(deep=True)
    o = obligation(new, oid)
    if not o or o.kind != 'output' or new.ledger.S[oid] != OS.ACTIVE or not same(value, o.output_equals):
        raise ValueError('output requirement unsatisfied')
    new.ledger.outputs[oid] = value
    new.ledger.S[oid] = OS.VERIFIED
    refresh(new)
    return new


def final_gate(state: RuntimeState) -> bool:
    """Eq. 9 assumes protected state; additionally check completion support exists."""
    frozen(state)
    for o in state.contract.MUST:
        if not o.hard:
            continue
        status = state.ledger.S[o.id]
        if status == OS.WAIVED:
            if o.waiver_code is None or state.ledger.waivers.get(o.id) != o.waiver_code:
                return False
        elif status != OS.VERIFIED:
            return False
        elif o.kind == 'evidence' and not any(r.obligation == o.id for r in state.ledger.E.values()):
            return False
        elif o.kind == 'effect' and not any(r.obligation == o.id for r in state.ledger.receipts.values()):
            return False
        elif o.kind == 'output' and o.id not in state.ledger.outputs:
            return False
    return True


class Gateway:
    """Single-process authoritative mediator with atomic one-shot dispatch.

    runner is trusted infrastructure. A crash burns the ticket and budget;
    it never verifies an obligation. No real network runner is included.
    """
    def __init__(self, state: RuntimeState, key: bytes):
        if len(key) < 32:
            raise ValueError('HMAC key too short')
        self._state = state.model_copy(deep=True)
        self._key = key
        self._lock = RLock()

    def snapshot(self):
        with self._lock:
            return self._state.model_copy(deep=True)

    def issue(self, request: CallRequest, now: int, ttl: int = 60):
        with self._lock:
            cert, self._state = issue_certificate(request, self._state, self._key, now, ttl)
            return cert

    def execute(self, cert: EffectCertificate, request: CallRequest, now: int,
                runner: Callable[[CallRequest, str], NativeResult]):
        with self._lock:
            allowed, self._state = dispatch(cert, request, self._state, self._key, now)
            if not allowed:
                return False
            try:
                # Isolate caller/runner mutations from the authorized request.
                native = runner(request.model_copy(deep=True), cert.nonce)
            except Exception:
                self._state.ledger.K[cert.nonce].receipt_processed = True
                raise
            valid, self._state = check_receipt(native, cert, self._state, self._key)
            return valid
