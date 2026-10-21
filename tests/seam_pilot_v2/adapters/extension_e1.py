"""Extension E1 harness: action-narrow family, M2-authenticated evidence.

Reuses the seam_pilot_v2 adapters and the frozen upstream code paths without
modifying them. Adds only:

  - `E1Oracle`: `V2Oracle` plus one downstream rule — a call's tool must be in
    the handoff's narrowed action set (`handoff_tools`), mirroring the base
    oracle's existing resource rule (resources are already intersected with
    `role_resources` for downstream calls).
  - `ExtensionAPC`: `APCV2` whose handoff narrows the delegate role's action set
    to `case.handoff_tools` using the public `Scope`/`AuthorizationEnvelope.narrow`
    API — the same call path as `native.APC.handoff`, with the role scope's
    actions replaced by the narrowed set.
  - M2-auth: HMAC-signed evidence records and gate-side verification *before*
    `admit_evidence`, with three new denial reasons.
  - `run_case_e1`: the 5-arm runner for the 8 extension cases (40 executions).

M2-auth signing scheme (fixed before the E1 run; documented exactly)
--------------------------------------------------------------------
- Key: `EVIDENCE_KEY = b"seam-pilot-v2-extension-e1-evidence-signing-test-key"`
  (ASCII, 56 bytes). A deliberate public test credential, not a production
  secret; this extension does not test key management.
- Signed message: `canon(payload)`, UTF-8 encoded, where:
  - `canon` is the Task D engine's canonical JSON (`engine.py:25-37`):
    `json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
    allow_nan=False)` with no coercion or default insertion;
  - `payload` is the evidence record's fields
    {apc_allowed, apc_reasons, budget_remaining, composition_clear, freshness,
     revoked, principal, task, tool, resource, recipient, evidence_digest},
    i.e. every record field except the signature field itself.
- Signature: `HMAC-SHA256(key, message).hexdigest()`, stored in the record field
  `evidence_signature`; verification uses `hmac.compare_digest`.
- The gate-side adapter verifies, in order:
  1. `evidence_signature` present -> else `EVIDENCE-SIGNATURE-MISSING`;
  2. digest matches -> else `EVIDENCE-SIGNATURE-INVALID`;
  3. the signed record's tool/resource/recipient/task/principal equal the call
     and handoff context being checked -> else `EVIDENCE-BINDING-MISMATCH`
     (this is the replay check: a validly-signed record for another call).
  Only after all three pass is the record handed to `admit_evidence`.
- New denial reasons are extension `GateResult.code` values, distinct from the
  upstream engine's decision codes; documented in `design/action_narrow_condition.md`
  section 5 before the run.
"""
from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from v2_common import (
    APCV2,
    Call,
    MockWorld,
    ScopeSnapshot,
    V2Oracle,
    case_snapshot,
)
from extension_e1_generator import E1Case, HANDOFF_TOOLS, ROOT_TOOLS  # noqa: E402
from tracegrant_adapter import (  # noqa: E402
    GateResult,
    TraceGrantGate,
    recipient_value,
    resource_value,
    shadow_evidence_values,
)
from arms import _event  # noqa: E402
from implementation.engine import canon  # noqa: E402
from implementation.models import CallRequest  # noqa: E402

EVIDENCE_KEY = b"seam-pilot-v2-extension-e1-evidence-signing-test-key"

E1_ARMS: tuple[str, ...] = (
    "apc_alone",
    "tracegrant_alone",
    "apc_tracegrant_scope_only",
    "apc_tracegrant_retained",
    "apc_tracegrant_fail_closed",
)

E1_MAPPING: dict[str, str | None] = {
    "apc_alone": None,
    "tracegrant_alone": "M0",
    "apc_tracegrant_scope_only": "M0",
    "apc_tracegrant_retained": "M2-auth",
    "apc_tracegrant_fail_closed": "M1",
}

E1_MECHANISM = {
    "apc_alone": "APC",
    "tracegrant_alone": "TraceGrant",
    "apc_tracegrant_scope_only": "TraceGrant",
    "apc_tracegrant_retained": "TraceGrant",
    "apc_tracegrant_fail_closed": "TraceGrant",
}

E1_CHECKED_BY = {
    "apc_alone": ["APC"],
    "tracegrant_alone": ["TraceGrant-alone"],
    "apc_tracegrant_scope_only": ["TraceGrant-scope-only"],
    "apc_tracegrant_retained": ["APC-shadow-evidence", "TraceGrant-retained-signed"],
    "apc_tracegrant_fail_closed": ["APC-shadow", "TraceGrant-fail-closed"],
}

E1_ARM_SPEC: dict[str, dict[str, Any]] = {
    "apc_alone": {"apc": True, "gate": None},
    "tracegrant_alone": {"apc": False, "gate": "M0"},
    "apc_tracegrant_scope_only": {"apc": True, "gate": "M0"},
    "apc_tracegrant_retained": {"apc": True, "gate": "M2-auth"},
    "apc_tracegrant_fail_closed": {"apc": True, "gate": "M1"},
}


class E1Oracle(V2Oracle):
    """Reference oracle for the action-narrow family.

    The delegate's effective authority after the handoff is `root A ∩ handoff A'`;
    for the downstream phase a tool outside `case.handoff_tools` is a violation
    (`handoff_action_scope`). Everything else is `V2Oracle` unchanged.
    """

    def decide(self, call: Call, args: dict[str, Any], phase: str) -> list[str]:
        reasons = super().decide(call, args, phase)
        if phase == "downstream" and call.tool not in self.case.handoff_tools:
            reasons.append("handoff_action_scope")
        return reasons


class ExtensionAPC(APCV2):
    """APCV2 with a handoff that narrows the role's action set.

    Replicates `native.APC.handoff` (seam_pilot/native.py:99-108) for the
    `status == "current"`, `reset=False`, `fresh_pdp=False` case with exactly one
    change: the delegate role scope's action set is `case.handoff_tools` instead
    of `self.root_scope.actions`. The envelope is narrowed with the public
    `AuthorizationEnvelope.narrow`, whose `Scope.meet` intersects actions, so the
    effective action set becomes `root A ∩ handoff A'`. No upstream file changes.
    """

    def handoff(self, reset: bool = False, fresh_pdp: bool = False) -> None:
        if reset or fresh_pdp:
            raise ValueError("extension E1 uses reset=False, fresh_pdp=False only")
        from apc.core import ExecutionRole, Principal, Scope

        case = self.case
        if case.status != "current":
            raise ValueError("extension action_narrow family is status=current only")
        role = Scope(frozenset(case.role_resources), frozenset(case.handoff_tools),
                     frozenset(self.native.root_scope.data_classifications))
        self.native.envelope = self.native.envelope.narrow(
            Principal("agent:b", ExecutionRole.ON_BEHALF_OF, role), self.native.key)
        self.downstream = True


# ---------------------------------------------------------------------------
# M2-auth: signing, verification, gate wrapper
# ---------------------------------------------------------------------------

def evidence_message(values: dict[str, Any]) -> str:
    """Canonical signed message: all record fields except the signature itself."""
    payload = {k: v for k, v in values.items() if k != "evidence_signature"}
    return canon(payload)


def sign_evidence(values: dict[str, Any]) -> str:
    return hmac.new(EVIDENCE_KEY, evidence_message(values).encode("utf-8"), hashlib.sha256).hexdigest()


def signed_evidence_values(
    case: E1Case,
    snapshot: ScopeSnapshot,
    call: Call,
    args: dict[str, Any],
    shadow_admitted: bool,
    shadow_reasons: list[str],
    pre_budget_remaining: float,
) -> dict[str, Any]:
    """The M2 evidence record values plus an HMAC signature over the record."""
    values = shadow_evidence_values(case, snapshot, call, args,
                                    shadow_admitted, shadow_reasons, pre_budget_remaining)
    values["evidence_signature"] = sign_evidence(values)
    return values


def verify_evidence_signature(
    values: dict[str, Any] | None,
    call: Call,
    args: dict[str, Any],
    snapshot: ScopeSnapshot,
) -> tuple[bool, str, str]:
    """Gate-side verification; returns (ok, code, message).

    Codes: EVIDENCE-VERIFIED on success; EVIDENCE-SIGNATURE-MISSING,
    EVIDENCE-SIGNATURE-INVALID, EVIDENCE-BINDING-MISMATCH on rejection.
    """
    if not isinstance(values, dict) or "evidence_signature" not in values:
        return False, "EVIDENCE-SIGNATURE-MISSING", "evidence record carries no signature field"
    if not hmac.compare_digest(str(values["evidence_signature"]), sign_evidence(values)):
        return False, "EVIDENCE-SIGNATURE-INVALID", "evidence signature does not verify"
    binding = {
        "tool": call.tool,
        "resource": resource_value(args),
        "recipient": recipient_value(args),
        "task": snapshot.task,
        "principal": snapshot.principal,
    }
    for field, expected in binding.items():
        if str(values.get(field)) != str(expected):
            return (False, "EVIDENCE-BINDING-MISMATCH",
                    f"signed record {field}={values.get(field)!r} does not match the call ({expected!r})")
    return True, "EVIDENCE-VERIFIED", "signature and call binding verified"


class AuthenticatedEvidenceGate(TraceGrantGate):
    """M2 with signed evidence: verify before admitting, otherwise unchanged."""

    def evaluate_signed(
        self,
        case: E1Case,
        snapshot: ScopeSnapshot,
        call: Call,
        args: dict[str, Any],
        verify_kind: str,
        sequence: int,
        call_cost: float,
        evidence_values: dict[str, Any] | None,
    ) -> GateResult:
        ok, code, message = verify_evidence_signature(evidence_values, call, args, snapshot)
        if not ok:
            request = CallRequest(tool=call.tool, arguments=args, obligation="F1")
            return GateResult(admitted=False, code=code, reasons=[message],
                              mapping_note="evidence transport rejected before admission",
                              request=request)
        return self.evaluate(case, snapshot, call, args, "M2", verify_kind,
                             sequence, call_cost, evidence_values)


# ---------------------------------------------------------------------------
# Runner for the 8 extension cases (arms 1, 2, 5, 6, 7)
# ---------------------------------------------------------------------------

def run_case_e1(case: E1Case, arm: str) -> dict[str, Any]:
    if arm not in E1_ARMS:
        raise ValueError(arm)
    if case.prelude:
        raise ValueError("extension action_narrow family has no prelude")
    spec = E1_ARM_SPEC[arm]
    world = MockWorld(case)
    oracle = E1Oracle(case)
    apc: ExtensionAPC | None = ExtensionAPC(case) if spec["apc"] else None
    gate: AuthenticatedEvidenceGate | TraceGrantGate | None = None
    if spec["gate"]:
        gate = (AuthenticatedEvidenceGate() if arm == "apc_tracegrant_retained"
                else TraceGrantGate())
    mapping: str | None = spec["gate"]
    events: list[dict[str, Any]] = []
    handoff: dict[str, Any] = {}
    sequence = 0
    last_gate: dict[str, Any] | None = None
    evidence_auth: list[dict[str, Any]] = []

    for phase, calls in (("prelude", case.prelude), ("downstream", case.attempts)):
        if phase == "downstream":
            if apc is not None:
                before = apc.state()
                apc.handoff()
                handoff = {"before": before, "after": apc.state(), "snapshot": apc.snapshot().to_dict()}
            else:
                handoff = {"before": None, "after": None, "snapshot": case_snapshot(case).to_dict()}

        for index, call in enumerate(calls):
            sequence += 1
            try:
                args = world.canonical(call)
            except (TypeError, KeyError) as error:
                reasons = ["invalid_tool_signature"]
                events.append(_event(phase, index, call, dict(call.args), reasons, False,
                                     [str(error)], ["mock_tool_signature"], [], 0))
                continue

            oracle_reasons = oracle.decide(call, args, phase)

            if gate is not None and (phase == "downstream" or arm == "tracegrant_alone"):
                snapshot = apc.snapshot() if (apc is not None and phase == "downstream") else case_snapshot(case)
                if arm == "apc_tracegrant_scope_only":
                    assert apc is not None
                    pre_snapshot = apc.snapshot()
                    pre_remaining = pre_snapshot.budget_ceiling - pre_snapshot.budget_consumed
                    start = time.perf_counter_ns()
                    shadow_decision = apc.authorize(call, args)
                    gate_result = gate.evaluate(case, pre_snapshot, call, args, mapping or "M0",
                                                case.verify_kind, sequence, call.cost, None)
                    elapsed = time.perf_counter_ns() - start
                    shadow = {"allowed": shadow_decision.allowed, "reasons": list(shadow_decision.reasons),
                              "checked_by": list(shadow_decision.checked_by),
                              "pre_budget_remaining": pre_remaining}
                elif arm == "apc_tracegrant_retained":
                    assert apc is not None
                    pre_snapshot = apc.snapshot()
                    pre_remaining = pre_snapshot.budget_ceiling - pre_snapshot.budget_consumed
                    start = time.perf_counter_ns()
                    shadow_decision = apc.authorize(call, args)
                    evidence_values = signed_evidence_values(
                        case, pre_snapshot, call, args,
                        shadow_decision.allowed, list(shadow_decision.reasons), pre_remaining)
                    gate_result = gate.evaluate_signed(case, pre_snapshot, call, args,
                                                       case.verify_kind, sequence, call.cost,
                                                       evidence_values)
                    elapsed = time.perf_counter_ns() - start
                    verified, verify_code, verify_message = verify_evidence_signature(
                        evidence_values, call, args, pre_snapshot)
                    evidence_auth.append({
                        "sequence": sequence,
                        "verified": bool(verified),
                        "code": verify_code,
                        "message": verify_message,
                        "evidence_digest": evidence_values.get("evidence_digest"),
                        "signature": evidence_values.get("evidence_signature"),
                    })
                    shadow = {"allowed": shadow_decision.allowed, "reasons": list(shadow_decision.reasons),
                              "checked_by": list(shadow_decision.checked_by),
                              "pre_budget_remaining": pre_remaining}
                elif arm == "apc_tracegrant_fail_closed":
                    assert apc is not None
                    pre_snapshot = apc.snapshot()
                    start = time.perf_counter_ns()
                    shadow_decision = apc.authorize(call, args)
                    shadow = {"allowed": shadow_decision.allowed, "reasons": list(shadow_decision.reasons),
                              "checked_by": list(shadow_decision.checked_by)}
                    if not shadow_decision.allowed:
                        gate_result = GateResult(admitted=False, code="SHADOW-DENY",
                                                 reasons=list(shadow_decision.reasons),
                                                 mapping_note="upstream APC denial retained")
                    else:
                        gate_result = gate.evaluate(case, pre_snapshot, call, args, "M1",
                                                    case.verify_kind, sequence, call.cost, None)
                    elapsed = time.perf_counter_ns() - start
                else:  # tracegrant_alone
                    start = time.perf_counter_ns()
                    gate_result = gate.evaluate(case, snapshot, call, args, "M0",
                                                case.verify_kind, sequence, call.cost, None)
                    elapsed = time.perf_counter_ns() - start
                    shadow = None

                last_gate = gate_result.to_dict()
                allowed = gate_result.admitted
                effects = world.execute(call, args) if allowed else []
                if allowed:
                    gate.receipt(gate_result, call, args)
                    last_gate = gate_result.to_dict()
                if effects:
                    oracle.observe(call, effects)
                event = _event(phase, index, call, args, oracle_reasons, allowed,
                               gate_result.reasons, E1_CHECKED_BY[arm], effects, elapsed,
                               gate=last_gate, shadow=shadow)
                if arm == "apc_tracegrant_retained" and evidence_auth:
                    event["evidence_auth"] = evidence_auth[-1]
                events.append(event)
                continue

            # APC-gated phase (arm 1) or the shadow-gated prelude of arms 5/6/7.
            start = time.perf_counter_ns()
            assert apc is not None
            decision = apc.authorize(call, args)
            checked = E1_CHECKED_BY[arm] if phase == "downstream" else ["APC-shadow"]
            elapsed = time.perf_counter_ns() - start
            allowed = decision.allowed
            effects = world.execute(call, args) if allowed else []
            if effects:
                oracle.observe(call, effects)
            events.append(_event(phase, index, call, args, oracle_reasons, allowed,
                                 list(decision.reasons), checked, effects, elapsed,
                                 shadow={"allowed": allowed, "reasons": list(decision.reasons)}
                                 if phase == "downstream" and arm.startswith("apc_tracegrant") else None))

    return {
        "case": case.to_dict(),
        "arm": arm,
        "extension": "E1",
        "mechanism": E1_MECHANISM[arm],
        "mapping": E1_MAPPING[arm],
        "handoff": handoff,
        "events": events,
        "evidence_auth": evidence_auth,
        "final_state": (apc.state() if apc is not None else {"gate": last_gate}),
        "oracle_state": {
            "spent": oracle.total_cost,
            "confidential_read": oracle.confidential_read,
            "external_send": oracle.external_send,
        },
    }
