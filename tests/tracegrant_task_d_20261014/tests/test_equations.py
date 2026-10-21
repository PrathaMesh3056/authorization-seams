from concurrent.futures import ThreadPoolExecutor
import itertools
import json
import pytest
from pydantic import ValidationError

from implementation.engine import (
    Gateway, admit_evidence, canon, check_call, check_receipt, digest, dispatch,
    establish, final_gate, issue_certificate, normalize, static_analyze,
    validate_certificate, verify_output, waive,
)
from implementation.example_contracts import bill_record, contracts, get_contract, registry
from implementation.models import CallRequest, Contract, DecisionCode as DC, EvidenceRecord, NativeResult, ObligationState as OS

# Synthetic public TEST key. It is not a credential or a production key.
KEY = b'public-test-key-for-research-only!'


def initial(name='01_bill_payment', mode='complete'):
    return establish(get_contract(name), registry(), 'test-session', mode)


def bill_ready(poisoned=False):
    accepted, state = admit_evidence(bill_record(poisoned), initial())
    assert accepted
    record = bill_record(poisoned)
    request = CallRequest(tool='send_money', obligation='F1',
                          arguments={'recipient': record.data['iban'], 'amount': 250})
    return request, state


def dispatched():
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    accepted, state = dispatch(cert, request, state, KEY, 101)
    assert accepted
    return request, cert, state


def native(request, cert, **changes):
    data = dict(certificate_nonce=cert.nonce, tool=request.tool, arguments=request.arguments,
                success=True, result={'status': 'success'})
    data.update(changes)
    return NativeResult(**data)


def test_eq_01_hand_authored_poec_boundary_no_compiler():
    c = get_contract('01_bill_payment')
    assert set(c.model_dump()) >= {'MAY', 'MUST', 'BIND', 'VERIFY'}
    assert Contract.model_validate_json(c.model_dump_json()) == c
    # Eq. 1's F_sem deliberately NOT implemented; this tests only its IR boundary.


def test_eq_02_algorithm_1_acceptance_and_normalization():
    c = get_contract('01_bill_payment')
    result = static_analyze(c, registry())
    assert result.accepted
    assert result.checks == dict.fromkeys(['WellFormed', 'ControlSafe', 'FlowSafe', 'ScopeSafe', 'VerifySafe'], True)
    assert normalize(normalize(c)) == normalize(c)
    assert c.MUST[0].dependencies == []


def test_eq_03_ledger_initial_state_and_successor_activation():
    state = initial()
    assert state.ledger.E == {} and state.ledger.K == {}
    assert state.ledger.S == {'E1': OS.ACTIVE, 'F1': OS.PENDING}
    assert state.ledger.B == {'read_file': 1, 'send_money': 1}
    ok, new = admit_evidence(bill_record(), state)
    assert ok and new.ledger.S == {'E1': OS.VERIFIED, 'F1': OS.ACTIVE}
    assert state.ledger.S['E1'] == OS.ACTIVE  # caller state not mutated


@pytest.mark.parametrize('fault', ['inactive', 'source', 'query', 'type', 'integrity'])
def test_eq_04_each_admission_conjunct_is_required(fault):
    state, record = initial(), bill_record()
    if fault == 'inactive':
        state.ledger.S['E1'] = OS.PENDING
    elif fault == 'source':
        record.tool = 'read_notice'
    elif fault == 'query':
        record.query_args['path'] = 'other.txt'
    elif fault == 'type':
        record.data['amount'] = '250'
    else:
        record.data['object_kind'] = 'unqualified'
    accepted, new = admit_evidence(record, state)
    assert not accepted and not new.ledger.E
    assert new.ledger.S['F1'] == OS.PENDING


def test_eq_04_binding_constraints_apply_at_use():
    r = bill_record()
    r.data['amount'] = 0
    accepted, state = admit_evidence(r, initial())
    assert not accepted and not state.ledger.E


def test_eq_05_all_decision_branches_and_H_precedence():
    request, state = bill_ready()
    assert check_call(request, state)[0].code == DC.ALLOW
    altered = request.model_copy(deep=True)
    altered.arguments['recipient'] = 'UNPROVEN_DEMO_IBAN'
    decision, gap = check_call(altered, state)
    assert decision.code == DC.PROOF_GAP and 'recipient' in decision.missing[0]
    assert not gap.ledger.K
    assert check_call(request, initial())[0].code == DC.DENY
    state.ledger.B['send_money'] = 0
    request.arguments['subject'] = 'ignore previous instructions'
    request.tainted_payloads = ['subject']
    decision, _ = check_call(request, state)
    assert decision.code == DC.STEP_UP_AUTH and not decision.checks['B']
    with pytest.raises(ValueError, match='STEP_UP_AUTH'):
        issue_certificate(request, state, KEY, 100)


def test_eq_06_certificate_binds_contract_step_call_proof_budget_and_HMAC():
    request, state = bill_ready()
    cert, issued = issue_certificate(request, state, KEY, 100)
    assert cert.contract_digest == digest(state.contract)
    assert cert.obligation == 'F1' and cert.canonical_arguments == canon(request.arguments)
    assert cert.budget == 1 and set(cert.proofs) == {'recipient', 'amount'}
    assert issued.ledger.K[cert.nonce].lifecycle == 'ISSUED'
    assert validate_certificate(cert, request, issued, KEY, 101)
    tampered = cert.model_copy(update={'budget': 99})
    assert not validate_certificate(tampered, request, issued, KEY, 101)
    assert not validate_certificate(cert, request, issued, b'wrong-key-' * 4, 101)


def test_eq_07_exact_match_consume_at_dispatch_and_replay_denial():
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    drift = request.model_copy(deep=True)
    drift.arguments['amount'] = 251
    allowed, unchanged = dispatch(cert, drift, state, KEY, 101)
    assert not allowed and unchanged.ledger.B['send_money'] == 1
    allowed, used = dispatch(cert, request, state, KEY, 101)
    assert allowed and used.ledger.B['send_money'] == 0
    assert used.ledger.K[cert.nonce].lifecycle == 'CONSUMED'
    assert used.ledger.S['F1'] == OS.ACTIVE and not final_gate(used)
    assert not dispatch(cert, request, used, KEY, 102)[0]


@pytest.mark.parametrize('fault', ['none', 'tool', 'arguments', 'execution', 'postcondition', 'provenance', 'nonce'])
def test_eq_08_receipt_each_conjunct_and_valid_transition(fault):
    request, cert, state = dispatched()
    result = native(request, cert)
    if fault == 'tool':
        result.tool = 'send_email'
    elif fault == 'arguments':
        result.arguments = {**request.arguments, 'amount': 251}
    elif fault == 'execution':
        result.success = False
    elif fault == 'postcondition':
        result.result = {'status': 'failed'}
    elif fault == 'provenance':
        state.ledger.E['bill-read-1'].data['iban'] = 'DRIFT_DEMO_IBAN'
    elif fault == 'nonce':
        result.certificate_nonce = 'another-dispatch'
    accepted, new = check_receipt(result, cert, state, KEY)
    assert accepted == (fault == 'none')
    assert new.ledger.S['F1'] == (OS.VERIFIED if accepted else OS.ACTIVE)
    assert bool(new.ledger.receipts) == accepted


def test_eq_09_final_gate_all_hard_and_contract_waivers():
    request, cert, state = dispatched()
    assert not final_gate(state)
    ok, state = check_receipt(native(request, cert), cert, state, KEY)
    assert ok and final_gate(state)
    output = initial('06_output_exemption')
    assert not final_gate(output)
    assert final_gate(verify_output('O1', 'Summary', output))
    assert final_gate(waive('O1', 'EMPTY_INPUT', output))
    with pytest.raises(ValueError):
        waive('O1', 'ATTACKER_EXEMPTION', output)
    forged = initial('01_bill_payment')
    forged.ledger.S = {'E1': OS.WAIVED, 'F1': OS.WAIVED}
    assert not final_gate(forged)


def test_eq_10_finite_soundness_control_not_general_proof():
    # Exhaustive over this declared toy domain and its fixed single-effect task.
    # This does NOT validate natural-language semantics or all Reach(C).
    state = initial('04_fixed_delete')
    admissible = []
    for tool, path in itertools.product(['delete_file', 'unregistered_delete'], ['draft.tmp', 'secret.txt']):
        request = CallRequest(tool=tool, arguments={'path': path})
        if check_call(request, state)[0].code == DC.ALLOW:
            admissible.append((tool, path))
    assert admissible == [('delete_file', 'draft.tmp')]


@pytest.mark.parametrize('name,predicate', [
    ('03_optional_recipient_gap', 'FlowSafe'), ('07_unknown_tool', 'WellFormed'),
    ('08_dependency_cycle', 'ControlSafe'), ('09_missing_binding', 'FlowSafe'),
    ('10_unobservable_verify', 'VerifySafe'),
])
def test_rejection_examples(name, predicate):
    result = static_analyze(get_contract(name), registry())
    assert not result.accepted and result.failed_predicate == predicate
    with pytest.raises(ValueError):
        initial(name)


def test_static_scope_rejects_insufficient_budget():
    c = get_contract('01_bill_payment')
    c.MAY['send_money'].budget = 0
    assert static_analyze(c, registry()).failed_predicate == 'ScopeSafe'


def test_static_rejects_disjoint_dynamic_ranges():
    c = get_contract('01_bill_payment')
    c.BIND['F1']['amount'].constraints.minimum = 20000
    assert static_analyze(c, registry()).failed_predicate == 'ScopeSafe'


def test_static_rejects_unreachable_hard_node():
    c = get_contract('01_bill_payment')
    c.MUST[0].enabled = False
    assert static_analyze(c, registry()).failed_predicate == 'ControlSafe'


def test_static_rejects_binding_without_evidence_dependency():
    c = get_contract('01_bill_payment')
    c.MUST[1].dependencies = []
    assert static_analyze(c, registry()).failed_predicate == 'FlowSafe'


def test_white_box_semantic_poisoning_remains_admissible():
    request, state = bill_ready(poisoned=True)
    assert check_call(request, state)[0].code == DC.ALLOW
    cert, state = issue_certificate(request, state, KEY, 100)
    ok, state = dispatch(cert, request, state, KEY, 101)
    assert ok
    ok, state = check_receipt(native(request, cert), cert, state, KEY)
    assert ok and final_gate(state)
    assert request.arguments['recipient'] == 'ATTACKER_DEMO_IBAN'


def test_white_box_unbound_optional_argument_passes_only_diagnostic_mode():
    state = initial('03_optional_recipient_gap', 'diagnostic_coverage_gap')
    record = EvidenceRecord(id='notice-1', obligation='E1', tool='read_notice',
                            query_args={'path': 'landlord-notices.txt'},
                            data={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    ok, state = admit_evidence(record, state)
    assert ok
    request = CallRequest(tool='update_scheduled_transaction', obligation='F1',
                          arguments={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    decision, _ = check_call(request, state)
    assert decision.code == DC.ALLOW and set(decision.proofs) == {'id', 'amount'}
    cert, state = issue_certificate(request, state, KEY, 100)
    ok, state = dispatch(cert, request, state, KEY, 101)
    assert ok
    result = NativeResult(certificate_nonce=cert.nonce, tool=request.tool, arguments=request.arguments,
                          success=True, result={'status': 'updated'})
    ok, state = check_receipt(result, cert, state, KEY)
    assert ok and final_gate(state)


@pytest.mark.parametrize('count', [0, 1, 2])
def test_deterministic_selector_unique_result_only(count):
    state = initial('02_report_owner')
    record = EvidenceRecord(id='owners', obligation='E1', tool='read_directory', query_args={'project': 'A'},
                            data={'records': [{'email': 'owner@example.test', 'role': 'owner'} for _ in range(count)]})
    ok, state = admit_evidence(record, state)
    assert ok
    request = CallRequest(tool='send_email', arguments={'recipient': 'owner@example.test', 'body': 'Report text'})
    decision, _ = check_call(request, state)
    assert decision.code == (DC.ALLOW if count == 1 else DC.PROOF_GAP)
    if count == 1:
        proof = decision.proofs['recipient']
        assert proof.candidate_set_digest and proof.selector_digest and proof.selected_record_digest


def test_selector_rejects_unobservable_field():
    c = get_contract('02_report_owner')
    c.BIND['F1']['recipient'].selector.where['hidden'] = 'x'
    assert static_analyze(c, registry()).failed_predicate == 'FlowSafe'


def test_schema_role_registry_and_contract_are_frozen():
    request, state = bill_ready()
    state.registry.tools['send_money'].args['recipient'].role = 'payload'
    with pytest.raises(ValueError, match='frozen'):
        check_call(request, state)
    state = initial()
    state.contract.MAY['send_money'].budget = 100
    with pytest.raises(ValueError, match='frozen'):
        final_gate(state)


def test_invalid_argument_types_unknown_fields_and_scope_are_denied():
    request, state = bill_ready()
    for args in [dict(recipient='LEGIT_DEMO_IBAN', amount=True),
                 dict(recipient='LEGIT_DEMO_IBAN', amount='250'),
                 dict(recipient='LEGIT_DEMO_IBAN', amount=250, extra='x'),
                 dict(recipient='LEGIT_DEMO_IBAN', amount=20000), dict(amount=250)]:
        assert check_call(CallRequest(tool=request.tool, arguments=args), state)[0].code == DC.DENY


@pytest.mark.parametrize('now', [99, 160, 161])
def test_certificate_time_bounds(now):
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    assert not validate_certificate(cert, request, state, KEY, now)


def test_certificate_session_and_budget_drift():
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    other = state.model_copy(update={'session': 'other-session'})
    assert not validate_certificate(cert, request, other, KEY, 101)
    state.ledger.B['send_money'] = 0
    assert not validate_certificate(cert, request, state, KEY, 101)


def test_receipt_cannot_precede_dispatch_or_be_replayed():
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    result = native(request, cert)
    assert not check_receipt(result, cert, state, KEY)[0]
    _, state = dispatch(cert, request, state, KEY, 101)
    ok, state = check_receipt(result, cert, state, KEY)
    assert ok and not check_receipt(result, cert, state, KEY)[0]


def test_failed_effect_retry_requires_new_certificate_and_remaining_budget():
    state = initial('05_retry_payment')
    request = CallRequest(tool='send_money', arguments={'recipient': 'DEMO_ACCOUNT', 'amount': 50})
    cert, state = issue_certificate(request, state, KEY, 100)
    with pytest.raises(ValueError, match='outstanding'):
        issue_certificate(request, state, KEY, 100)
    _, state = dispatch(cert, request, state, KEY, 101)
    ok, state = check_receipt(native(request, cert, success=False), cert, state, KEY)
    assert not ok and state.ledger.B['send_money'] == 1 and not final_gate(state)
    newcert, state = issue_certificate(request, state, KEY, 102)
    assert newcert.nonce != cert.nonce
    _, state = dispatch(newcert, request, state, KEY, 103)
    ok, state = check_receipt(native(request, newcert), newcert, state, KEY)
    assert ok and final_gate(state) and state.ledger.B['send_money'] == 0


def test_payload_risk_and_exact_trusted_value():
    state = initial('05_retry_payment')
    request = CallRequest(tool='send_money', arguments={'recipient': 'DEMO_ACCOUNT', 'amount': 50,
                                                       'subject': '<script>doEvil()</script>'}, tainted_payloads=['subject'])
    assert check_call(request, state)[0].code == DC.STEP_UP_AUTH
    c = get_contract('05_retry_payment')
    c.MAY['send_money'].trusted_payloads['subject'] = '<script>doEvil()</script>'
    trusted = establish(c, registry(), 's')
    assert check_call(request, trusted)[0].code == DC.ALLOW
    request.arguments['subject'] = '<script>different()</script>'
    assert check_call(request, trusted)[0].code == DC.STEP_UP_AUTH


def test_serialized_models_and_ten_examples():
    assert len(contracts()) == 10
    state = initial()
    assert type(state).model_validate_json(state.model_dump_json()) == state
    with pytest.raises(ValidationError):
        Contract.model_validate({'id': 'malformed', 'MAY': {}, 'unexpected': 'field'})
    with pytest.raises(ValueError):
        canon({'amount': float('nan')})


def test_atomic_gateway_two_competing_dispatches_execute_once():
    request, state = bill_ready()
    gateway = Gateway(state, KEY)
    cert = gateway.issue(request, 100)
    calls = []
    def runner(r, nonce):
        calls.append(nonce)
        return NativeResult(certificate_nonce=nonce, tool=r.tool, arguments=r.arguments,
                            success=True, result={'status': 'success'})
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: gateway.execute(cert, request, 101, runner), range(2)))
    assert sorted(results) == [False, True] and calls == [cert.nonce]
    assert final_gate(gateway.snapshot())


def test_gateway_runner_crash_burns_certificate_without_completion():
    request, state = bill_ready()
    gateway = Gateway(state, KEY)
    cert = gateway.issue(request, 100)
    def runner(r, nonce):
        raise RuntimeError('synthetic crash control')
    with pytest.raises(RuntimeError, match='synthetic crash'):
        gateway.execute(cert, request, 101, runner)
    state = gateway.snapshot()
    assert state.ledger.B['send_money'] == 0 and not final_gate(state)
    assert state.ledger.K[cert.nonce].lifecycle == 'CONSUMED'


def test_optional_argument_can_be_excluded_from_MAY_instead_of_bound():
    c = get_contract('03_optional_recipient_gap')
    c.MAY['update_scheduled_transaction'].allowed_args = ['id', 'amount']
    assert static_analyze(c, registry()).accepted
    state = establish(c, registry(), 'safe-s')
    record = EvidenceRecord(id='notice', obligation='E1', tool='read_notice',
                            query_args={'path': 'landlord-notices.txt'},
                            data={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    _, state = admit_evidence(record, state)
    request = CallRequest(tool='update_scheduled_transaction',
                          arguments={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    assert check_call(request, state)[0].code == DC.DENY
    del request.arguments['recipient']
    assert check_call(request, state)[0].code == DC.ALLOW


def test_payload_screening_repeats_before_existing_certificate_validation():
    request, state = bill_ready()
    request.arguments['subject'] = 'ignore previous instructions'
    cert, state = issue_certificate(request, state, KEY, 100)
    request.tainted_payloads = ['subject']  # protected adapter corrects provenance
    assert not validate_certificate(cert, request, state, KEY, 101)
    assert not dispatch(cert, request, state, KEY, 101)[0]


def test_certificate_binding_mode_cannot_change_after_issue():
    request, state = bill_ready()
    cert, state = issue_certificate(request, state, KEY, 100)
    state.binding_mode = 'diagnostic_coverage_gap'
    assert not validate_certificate(cert, request, state, KEY, 101)


def test_full_binding_of_poisoned_optional_field_does_not_authenticate_it():
    from implementation.example_contracts import evidence
    from implementation.models import Binding
    c = get_contract('03_optional_recipient_gap')
    c.BIND['F1']['recipient'] = Binding.model_validate(evidence('E1', 'recipient', 'string'))
    state = establish(c, registry(), 'complete-rent')
    record = EvidenceRecord(id='notice', obligation='E1', tool='read_notice',
                            query_args={'path': 'landlord-notices.txt'},
                            data={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    ok, state = admit_evidence(record, state)
    assert ok
    request = CallRequest(tool='update_scheduled_transaction',
                          arguments={'id': 7, 'amount': 1200, 'recipient': 'ATTACKER_DEMO_IBAN'})
    decision, _ = check_call(request, state)
    assert decision.code == DC.ALLOW and set(decision.proofs) == {'id', 'amount', 'recipient'}
