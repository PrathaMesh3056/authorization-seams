"""Seven-arm v2 runner. Strictly sequential: no arm runs concurrently.

Arm semantics (design/call_to_contract_mapping.md section 8):
  1 apc_alone                       APC gate only, full root state.
  2 tracegrant_alone                TraceGrant gate only, M0 from the frozen root scope.
  3 apc_apc_preserved               same-mechanism control, budget/composition preserved.
  4 apc_apc_reset                   same-mechanism control, budget/composition reset.
  5 apc_tracegrant_scope_only       shadow APC runs first; TraceGrant M0 gets the post-handoff
                                    scope only; shadow denial is recorded, not propagated.
  6 apc_tracegrant_retained         M2; shadow APC decision and pre-admission budget carried
                                    as admitted `apc_state` evidence.
  7 apc_tracegrant_fail_closed      shadow denial retained; M1 denies any untranslatable field.
"""
from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any

from v2_common import (
    APCV2,
    ARM_MAPPING,
    ARM_MECHANISM,
    ARMS_V2,
    Call,
    MockWorld,
    V2Case,
    V2Oracle,
    case_snapshot,
)
from tracegrant_adapter import GateResult, TraceGrantGate, shadow_evidence_values

ARM_SPEC: dict[str, dict[str, Any]] = {
    "apc_alone": {"apc": True, "reset": False, "gate": None},
    "tracegrant_alone": {"apc": False, "reset": False, "gate": "M0"},
    "apc_apc_preserved": {"apc": True, "reset": False, "gate": None},
    "apc_apc_reset": {"apc": True, "reset": True, "gate": None},
    "apc_tracegrant_scope_only": {"apc": True, "reset": False, "gate": "M0"},
    "apc_tracegrant_retained": {"apc": True, "reset": False, "gate": "M2"},
    "apc_tracegrant_fail_closed": {"apc": True, "reset": False, "gate": "M1"},
}

CHECKED_BY = {
    "apc_alone": ["APC"],
    "tracegrant_alone": ["TraceGrant-alone"],
    "apc_apc_preserved": ["APC-preserved"],
    "apc_apc_reset": ["APC-reset"],
    "apc_tracegrant_scope_only": ["TraceGrant-scope-only"],
    "apc_tracegrant_retained": ["APC-shadow-evidence", "TraceGrant-retained"],
    "apc_tracegrant_fail_closed": ["APC-shadow", "TraceGrant-fail-closed"],
}


def _event(
    phase: str,
    index: int,
    call: Call,
    args: dict[str, Any],
    oracle_reasons: list[str],
    allowed: bool,
    reasons: list[str],
    checked_by: list[str],
    effects: list[dict[str, Any]],
    authorization_ns: int,
    gate: dict[str, Any] | None = None,
    shadow: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "phase": phase,
        "index": index,
        "tool": call.tool,
        "proposed": asdict(call),
        "canonical_args": args,
        "oracle_allowed": not oracle_reasons,
        "oracle_reasons": list(oracle_reasons),
        "allowed": bool(allowed),
        "reasons": list(reasons),
        "checked_by": list(checked_by),
        "effects": effects,
        "unauthorized_effect": bool(oracle_reasons and effects),
        "false_denial": bool(not oracle_reasons and not allowed),
        "authorization_ns": authorization_ns,
        "gate": gate,
        "shadow": shadow,
        "receipt_ok": (gate or {}).get("receipt_ok"),
        "verify_failed": bool((gate or {}).get("verify_failed")),
    }


def run_case(case: V2Case, arm: str) -> dict[str, Any]:
    if arm not in ARMS_V2:
        raise ValueError(arm)
    spec = ARM_SPEC[arm]
    world = MockWorld(case)
    oracle = V2Oracle(case)
    apc: APCV2 | None = APCV2(case) if spec["apc"] else None
    gate: TraceGrantGate | None = TraceGrantGate() if spec["gate"] else None
    mapping: str | None = spec["gate"]
    mechanism = ARM_MECHANISM[arm]
    events: list[dict[str, Any]] = []
    handoff: dict[str, Any] = {}
    sequence = 0
    last_gate: dict[str, Any] | None = None

    for phase, calls in (("prelude", case.prelude), ("downstream", case.attempts)):
        if phase == "downstream":
            if apc is not None:
                before = apc.state()
                apc.handoff(reset=spec["reset"],
                            fresh_pdp=(arm in ("apc_apc_preserved", "apc_apc_reset")))
                handoff = {"before": before, "after": apc.state(), "snapshot": apc.snapshot().to_dict()}
            else:
                handoff = {"before": None, "after": None, "snapshot": case_snapshot(case).to_dict()}

        for index, call in enumerate(calls):
            sequence += 1
            try:
                args = world.canonical(call)
            except (TypeError, KeyError) as error:
                reasons = ["invalid_tool_signature"]
                oracle_reasons = ["invalid_tool_signature"]
                events.append(_event(phase, index, call, dict(call.args), oracle_reasons, False,
                                     [str(error)], ["mock_tool_signature"], [], 0))
                continue

            oracle_reasons = oracle.decide(call, args, phase)

            if gate is not None and (phase == "downstream" or arm == "tracegrant_alone"):
                snapshot = apc.snapshot() if (apc is not None and phase == "downstream") else case_snapshot(case)
                if arm == "apc_tracegrant_scope_only":
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
                    pre_snapshot = apc.snapshot()
                    pre_remaining = pre_snapshot.budget_ceiling - pre_snapshot.budget_consumed
                    start = time.perf_counter_ns()
                    shadow_decision = apc.authorize(call, args)
                    evidence_values = shadow_evidence_values(
                        case, pre_snapshot, call, args,
                        shadow_decision.allowed, list(shadow_decision.reasons), pre_remaining)
                    gate_result = gate.evaluate(case, pre_snapshot, call, args, "M2",
                                                case.verify_kind, sequence, call.cost, evidence_values)
                    elapsed = time.perf_counter_ns() - start
                    shadow = {"allowed": shadow_decision.allowed, "reasons": list(shadow_decision.reasons),
                              "checked_by": list(shadow_decision.checked_by),
                              "pre_budget_remaining": pre_remaining}
                elif arm == "apc_tracegrant_fail_closed":
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
                events.append(_event(phase, index, call, args, oracle_reasons, allowed,
                                     gate_result.reasons, CHECKED_BY[arm], effects, elapsed,
                                     gate=last_gate, shadow=shadow))
                continue

            # APC-gated phase (arm 1/3/4) or the shadow-gated prelude of arms 5/6/7.
            start = time.perf_counter_ns()
            if apc is not None:
                decision = apc.authorize(call, args)
                checked = CHECKED_BY[arm] if phase == "downstream" else ["APC-shadow" if arm.startswith("apc_tracegrant") else "APC"]
            else:
                raise AssertionError("no gate for this arm")
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
        "mechanism": mechanism,
        "mapping": mapping,
        "handoff": handoff,
        "events": events,
        "final_state": (apc.state() if apc is not None else {"gate": last_gate}),
        "oracle_state": {
            "spent": oracle.total_cost,
            "confidential_read": oracle.confidential_read,
            "external_send": oracle.external_send,
        },
    }
