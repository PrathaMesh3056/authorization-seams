"""TraceGrant side of the seam: registry, contract mappings, and the gate.

This module wraps the independent Task D implementation
(`tracegrant_task_d_20261014/implementation/engine.py`) without modifying it.
Everything it builds is governed by `design/call_to_contract_mapping.md`; the
mapping is our design choice, not a reading of either paper.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from v2_common import Call, ScopeSnapshot, V2Case, evidence_digest, mock_result

from implementation.engine import (  # noqa: E402
    admit_evidence,
    canon,
    check_call,
    check_receipt,
    digest,
    dispatch,
    establish,
    issue_certificate,
)
from implementation.models import (  # noqa: E402
    ArgSpec,
    Binding,
    CallRequest,
    Constraint,
    Contract,
    DecisionCode,
    EvidenceRecord,
    EvidenceRule,
    NativeResult,
    Obligation,
    Permission,
    Registry,
    ToolSchema,
    ValueType,
    Verification,
)

GATE_KEY = b"synthetic-v2-tracegrant-test-key-0123456789"  # >= 32 bytes, test only
GATE_TTL = 60

RESULT_FIELDS: dict[str, dict[str, ValueType]] = {
    "read_confidential": {"content": ValueType.STRING},
    "read_public": {"content": ValueType.STRING},
    "save_internal": {"status": ValueType.STRING},
    "send_external": {"status": ValueType.STRING},
    "apc_state": {
        "apc_allowed": ValueType.BOOLEAN,
        "apc_reasons": ValueType.STRING,
        "budget_remaining": ValueType.NUMBER,
        "composition_clear": ValueType.BOOLEAN,
        "freshness": ValueType.STRING,
        "revoked": ValueType.BOOLEAN,
        "principal": ValueType.STRING,
        "task": ValueType.STRING,
        "tool": ValueType.STRING,
        "resource": ValueType.STRING,
        "recipient": ValueType.STRING,
        "evidence_digest": ValueType.STRING,
    },
}

TOOL_ARGS: dict[str, dict[str, ArgSpec]] = {
    "read_confidential": {"resource": ArgSpec(type=ValueType.STRING, role="authority")},
    "read_public": {"resource": ArgSpec(type=ValueType.STRING, role="authority")},
    "save_internal": {
        "resource": ArgSpec(type=ValueType.STRING, role="authority"),
        "body": ArgSpec(type=ValueType.STRING, role="payload"),
    },
    "send_external": {
        "recipient": ArgSpec(type=ValueType.STRING, role="authority"),
        "body": ArgSpec(type=ValueType.STRING, role="payload"),
    },
    "apc_state": {
        "tool": ArgSpec(type=ValueType.STRING, role="authority"),
        "resource": ArgSpec(type=ValueType.STRING, role="authority"),
    },
}

TOOL_KIND = {
    "read_confidential": "effect",
    "read_public": "effect",
    "save_internal": "effect",
    "send_external": "effect",
    "apc_state": "query",
}


def build_registry() -> Registry:
    tools = {}
    for name, args in TOOL_ARGS.items():
        tools[name] = ToolSchema(kind=TOOL_KIND[name], args=args, result_fields=RESULT_FIELDS[name])
    return Registry(tools=tools)


REGISTRY = build_registry()


def expected_verify(case: V2Case, tool: str, args: dict[str, Any], verify_kind: str) -> dict[str, Any]:
    if verify_kind == "unsatisfiable":
        return {"status": "delivered_to_human"}
    if tool == "read_confidential":
        return {"content": f"CONFIDENTIAL-MARKER:{args['resource']}"}
    if tool == "read_public":
        return {"content": f"PUBLIC-MARKER:{args['resource']}"}
    if tool == "save_internal":
        return {"status": "saved"}
    if tool == "send_external":
        return {"status": "sent"}
    raise ValueError(tool)


def resource_value(args: dict[str, Any]) -> str:
    return str(args.get("resource", "mail:external"))


def recipient_value(args: dict[str, Any]) -> str:
    return str(args.get("recipient", ""))


def build_contract(
    case: V2Case,
    snapshot: ScopeSnapshot,
    call: Call,
    args: dict[str, Any],
    mapping: str,
    verify_kind: str,
    call_cost: float,
    evidence_values: dict[str, Any] | None,
    sequence: int,
) -> Contract:
    allowed_args = sorted(args.keys())
    constraints: dict[str, Constraint] = {}
    if "resource" in args:
        if mapping == "M1":
            choices = sorted(set(snapshot.root_resources) & set(snapshot.handoff_resources))
        else:
            choices = sorted(snapshot.handoff_resources)
        constraints["resource"] = Constraint(type=ValueType.STRING, choices=choices)
    if "recipient" in args:
        constraints["recipient"] = Constraint(type=ValueType.STRING, choices=[snapshot.recipient])

    may: dict[str, Permission] = {
        call.tool: Permission(budget=1, allowed_args=allowed_args, constraints=constraints)
    }
    bindings = {
        arg: Binding(source="constant", constant=args[arg], constraints=constraint)
        for arg, constraint in constraints.items()
    }
    bindings = {"F1": bindings}

    if mapping == "M2":
        if evidence_values is None:
            raise ValueError("M2 requires evidence values")
        may["apc_state"] = Permission(budget=1, allowed_args=["tool", "resource"])
        fields = {
            "apc_allowed": Constraint(type=ValueType.BOOLEAN, equals=True, has_equals=True),
            "apc_reasons": Constraint(type=ValueType.STRING, equals="", has_equals=True),
            "budget_remaining": Constraint(type=ValueType.NUMBER, minimum=float(call_cost)),
            "composition_clear": Constraint(type=ValueType.BOOLEAN, equals=True, has_equals=True),
            "freshness": Constraint(type=ValueType.STRING, choices=["current", "renewed"]),
            "revoked": Constraint(type=ValueType.BOOLEAN, equals=False, has_equals=True),
            "principal": Constraint(type=ValueType.STRING, equals=snapshot.principal, has_equals=True),
            "task": Constraint(type=ValueType.STRING, equals=snapshot.task, has_equals=True),
            "tool": Constraint(type=ValueType.STRING, equals=call.tool, has_equals=True),
            "resource": Constraint(type=ValueType.STRING, equals=resource_value(args), has_equals=True),
            "recipient": Constraint(type=ValueType.STRING, equals=recipient_value(args), has_equals=True),
        }
        rule = EvidenceRule(
            query_args={"tool": call.tool, "resource": resource_value(args)},
            fields=fields,
            integrity={"evidence_digest": evidence_values["evidence_digest"]},
        )
        must = [
            Obligation(id="E1", kind="evidence", tool="apc_state", evidence=rule),
            Obligation(id="F1", kind="effect", tool=call.tool, dependencies=["E1"]),
        ]
    else:
        must = [Obligation(id="F1", kind="effect", tool=call.tool)]

    verify = {
        "F1": Verification(postconditions=expected_verify(case, call.tool, args, verify_kind))
    }
    return Contract(
        id=f"v2-{case.id}-{mapping}-{sequence}",
        trusted_request=f"apc-call:{case.id}",
        MAY=may,
        MUST=must,
        BIND=bindings,
        VERIFY=verify,
    )


def m1_translation_notes(
    case: V2Case,
    snapshot: ScopeSnapshot,
    call: Call,
    args: dict[str, Any],
    verify_kind: str,
) -> list[str]:
    """Fields M1 treats as untranslatable. Fail closed, never leak."""
    notes: list[str] = []
    if call.tool not in snapshot.actions:
        notes.append(f"action {call.tool} not in root A")
    if "resource" in args:
        if args["resource"] not in snapshot.root_resources:
            notes.append(f"resource {args['resource']} not in root R")
        elif args["resource"] not in snapshot.handoff_resources:
            notes.append(f"resource {args['resource']} missing from handoff R")
    if "recipient" in args and args["recipient"] != snapshot.recipient:
        notes.append(f"recipient {args['recipient']} not in allowlist")
    if verify_kind != "observable":
        notes.append("no satisfiable VERIFY value derivable")
    if call.actor != snapshot.principal:
        notes.append(f"principal {call.actor} differs from handoff context")
    if call.session != snapshot.task:
        notes.append(f"session {call.session} differs from handoff task")
    for aspect in case.exercised_aspects:
        if aspect in ("composition_history", "budget_consumed", "replay_state", "expiry", "revocation"):
            notes.append(f"untranslatable exercised aspect {aspect}")
    return notes


def shadow_evidence_values(
    case: V2Case,
    snapshot: ScopeSnapshot,
    call: Call,
    args: dict[str, Any],
    shadow_admitted: bool,
    shadow_reasons: list[str],
    pre_budget_remaining: float,
) -> dict[str, Any]:
    """Values for the M2 `apc_state` evidence record.

    `pre_budget_remaining` is the APC budget left *before* the current call was
    admitted, so `budget_remaining >= call.cost` is the same check the upstream
    APC performed. The digest is a harness consistency control (sha256 over the
    record fields), not a security token; M2 tests what can be carried, not
    authenticated evidence transport.
    """
    freshness = "renewed" if case.status == "renewed" else ("current" if case.status == "current" else case.status)
    values: dict[str, Any] = {
        "apc_allowed": bool(shadow_admitted),
        "apc_reasons": "" if shadow_admitted else "; ".join(shadow_reasons),
        "budget_remaining": float(pre_budget_remaining),
        "composition_clear": bool(shadow_admitted),
        "freshness": freshness,
        "revoked": bool(snapshot.revoked),
        "principal": snapshot.principal,
        "task": snapshot.task,
        "tool": call.tool,
        "resource": resource_value(args),
        "recipient": recipient_value(args),
    }
    values["evidence_digest"] = evidence_digest(values)
    return values


@dataclass
class GateResult:
    admitted: bool
    code: str
    reasons: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)
    mapping_note: str | None = None
    contract_digest: str | None = None
    receipt_ok: bool | None = None
    verify_failed: bool = False
    evidence_digest: str | None = None
    request: CallRequest | None = None
    state: Any = None
    certificate: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "code": self.code,
            "reasons": list(self.reasons),
            "checks": dict(self.checks),
            "mapping_note": self.mapping_note,
            "contract_digest": self.contract_digest,
            "receipt_ok": self.receipt_ok,
            "verify_failed": self.verify_failed,
            "evidence_digest": self.evidence_digest,
        }


class TraceGrantGate:
    """One gate instance per case run; contracts are synthesized per call."""

    def __init__(self) -> None:
        self.key = GATE_KEY

    def evaluate(
        self,
        case: V2Case,
        snapshot: ScopeSnapshot,
        call: Call,
        args: dict[str, Any],
        mapping: str,
        verify_kind: str,
        sequence: int,
        call_cost: float,
        evidence_values: dict[str, Any] | None = None,
        now: int | None = None,
        tainted_payloads: list[str] | None = None,
    ) -> GateResult:
        now = int(time.time()) if now is None else now
        request = CallRequest(tool=call.tool, arguments=args, obligation="F1",
                              tainted_payloads=list(tainted_payloads or []))

        if mapping == "M1":
            notes = m1_translation_notes(case, snapshot, call, args, verify_kind)
            if notes:
                return GateResult(
                    admitted=False,
                    code="MAPPING-REJECT",
                    reasons=["fail-closed: " + "; ".join(notes)],
                    mapping_note="; ".join(notes),
                    request=request,
                )

        try:
            contract = build_contract(case, snapshot, call, args, mapping, verify_kind,
                                      call_cost, evidence_values, sequence)
        except ValueError as error:
            return GateResult(admitted=False, code="MAPPING-REJECT",
                              reasons=[f"contract construction failed: {error}"],
                              mapping_note=str(error), request=request)

        try:
            state = establish(contract, REGISTRY, session=call.session)
        except ValueError as error:
            return GateResult(admitted=False, code="MAPPING-REJECT",
                              reasons=[f"establish rejected: {error}"],
                              mapping_note=str(error), request=request)

        if mapping == "M2":
            if evidence_values is None:
                return GateResult(admitted=False, code="MAPPING-REJECT",
                                  reasons=["M2 requires evidence values"], request=request)
            record = EvidenceRecord(
                id=f"E1-{case.id}-{sequence}",
                obligation="E1",
                tool="apc_state",
                query_args={"tool": call.tool, "resource": resource_value(args)},
                data=evidence_values,
            )
            accepted, state = admit_evidence(record, state)
            if not accepted:
                return GateResult(admitted=False, code="PROOF-GAP",
                                  reasons=["evidence not admitted (apc_state record failed its rule)"],
                                  contract_digest=state.contract_digest,
                                  mapping_note="evidence_not_admitted",
                                  evidence_digest=evidence_values.get("evidence_digest"),
                                  request=request)

        decision, state = check_call(request, state)
        if decision.code != DecisionCode.ALLOW:
            return GateResult(
                admitted=False,
                code=decision.code.value,
                reasons=list(decision.missing) or [decision.code.value],
                checks=dict(decision.checks),
                contract_digest=state.contract_digest,
                evidence_digest=(evidence_values or {}).get("evidence_digest"),
                request=request,
            )

        certificate, state = issue_certificate(request, state, self.key, now, ttl=GATE_TTL)
        dispatched, state = dispatch(certificate, request, state, self.key, now)
        if not dispatched:
            return GateResult(admitted=False, code="DENY", reasons=["dispatch rejected the certificate"],
                              contract_digest=state.contract_digest, request=request)
        return GateResult(
            admitted=True,
            code="ALLOW",
            checks=dict(decision.checks),
            contract_digest=state.contract_digest,
            evidence_digest=(evidence_values or {}).get("evidence_digest"),
            request=request,
            state=state,
            certificate=certificate,
        )

    def receipt(self, result: GateResult, call: Call, args: dict[str, Any]) -> bool:
        """Post-execution completion check. Returns True only if the receipt verifies."""
        if not result.admitted or result.certificate is None or result.state is None:
            return False
        native = NativeResult(
            certificate_nonce=result.certificate.nonce,
            tool=call.tool,
            arguments=args,
            success=True,
            result=mock_result(call, args),
        )
        ok, state = check_receipt(native, result.certificate, result.state, self.key)
        result.receipt_ok = bool(ok)
        result.verify_failed = not bool(ok)
        result.state = state
        return bool(ok)
