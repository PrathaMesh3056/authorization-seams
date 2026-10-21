"""Boundary harness: APC -> SentinelAgent with parameterizable bridge manifest derivation.

Reuses, read-only:
  - seam_pilot_sentinelagent/adapters/sa_harness.py  (token synthesis, native checks,
    T1 refusals, attestation, S1-S3 controls, run_case_sa)
  - seam_pilot_v2/adapters/v2_common.py              (APCV2, ScopeSnapshot, V2Oracle,
    case_snapshot, load_frozen_cases)
  - seam_pilot_v2/adapters/arms.py                   (run_case for arm 1 apc_alone)
  - seam_pilot_v2/adapters/tracegrant_adapter.py     (resource_value, recipient_value)
  - sentinelagent_audit_20261014/upstream            (pinned DelegationToken / DAS)
No upstream file is modified. The bridge key is installed via sa_harness.install_bridge_key().

Arm semantics (pilot arms 1, 2, 2v, 5, 6, 7):
  1  apc_alone                       APC gate only, full root state (run_case_v2 verbatim).
  2  sentinelagent_alone             T0 from the frozen case root scope, CANONICAL derivation.
  2v sentinelagent_alone_variant     T0 from the frozen case root scope, variant derivation.
  5  apc_sentinelagent_scope_only   shadow APC first; T0 from the pre-admission post-handoff
                                     snapshot, variant derivation; shadow denial not propagated.
  6  apc_sentinelagent_retained     T2-attest; shadow APC decision + pre-admission budget
                                     carried as a signature-verified attestation token.
  7  apc_sentinelagent_fail_closed  T1; shadow denial retained; deny on any untranslatable field.

The variant axis (v1 / v2) changes ONLY the token-manifest derivation:
  V1 role-scope derivation:   resource ops derive from case.role_resources
                              (the delegate's pre-narrowing role scope) instead of the
                              post-handoff effective scope. The SEND endpoint is unchanged.
  V2 resolved-call default:   for calls that omit a recipient, the manifest SEND endpoint
                              derives from the resolved argument (MockWorld default filled in)
                              instead of the snapshot recipient. Resource ops unchanged.

Scope tags, expiry, key handling, attestation, and scoring are identical to canonical T0.
All runs are strictly sequential; no network (prepare() blocks it).
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path
from typing import Any

BOUNDARY_ROOT = Path(__file__).resolve().parents[1]
RPAPER_ROOT = BOUNDARY_ROOT.parent
SA_ROOT = RPAPER_ROOT / "seam_pilot_sentinelagent"
V2_ROOT = RPAPER_ROOT / "seam_pilot_v2"

for _path in (str(SA_ROOT / "adapters"), str(SA_ROOT / "design"),
              str(V2_ROOT / "adapters"), str(V2_ROOT / "design"),
              str(RPAPER_ROOT / "authorization_pilot")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import sa_harness  # noqa: E402
from sa_harness import (  # noqa: E402
    SA_NEW_ARMS, UPSTREAM_FILE, install_bridge_key, load_locked,
    make_token, native_check, build_attestation, attestation_checks,
    t1_refusal, chain_refusal, evaluate_presented, presented_meta,
    EXPIRY_CURRENT, EXPIRY_PAST, STANDARD_TAG, VERB,
)
from v2_common import (  # noqa: E402
    APCV2, ScopeSnapshot, V2Oracle, case_snapshot, load_frozen_cases,
)
from arms import run_case as run_case_v2  # noqa: E402
from tracegrant_adapter import resource_value, recipient_value  # noqa: E402
from sa_case_generator import SACase  # noqa: E402
from seam_pilot.model import Call, MockWorld  # noqa: E402

# ---------------------------------------------------------------------------
# Arm / variant constants
# ---------------------------------------------------------------------------

BOUNDARY_ARMS = (
    "apc_alone",
    "sentinelagent_alone",
    "sentinelagent_alone_variant",
    "apc_sentinelagent_scope_only",
    "apc_sentinelagent_retained",
    "apc_sentinelagent_fail_closed",
)

VARIANTS = ("v1", "v2")
# Arms that run under the non-canonical variants (v1 / v2). Arm 2 (sentinelagent_alone)
# is the canonical bridge reference and is always run with canonical derivation; arm 1
# (apc_alone) is APC-only and ignores the variant. Both arms 1 and 2 are still executed
# under each variant label (v1 and v2) so the matrix is 6 arms x 2 variants x 96 cases
# = 1152 runs per the pre-registered count.
VARIANT_ARMS = (
    "sentinelagent_alone_variant",
    "apc_sentinelagent_scope_only",
    "apc_sentinelagent_retained",
    "apc_sentinelagent_fail_closed",
)

DEFAULT_RECIPIENT = "forbidden-default@example.test"

SA_CHECKED_BY = {
    "sentinelagent_alone": ["SentinelAgent-alone"],
    "sentinelagent_alone_variant": ["SentinelAgent-alone-variant"],
    "apc_sentinelagent_scope_only": ["SentinelAgent-scope-only"],
    "apc_sentinelagent_retained": ["APC-attestation", "SentinelAgent-retained"],
    "apc_sentinelagent_fail_closed": ["APC-shadow", "SentinelAgent-fail-closed"],
}
SA_MECHANISM = {
    "sentinelagent_alone": "SentinelAgent",
    "sentinelagent_alone_variant": "SentinelAgent",
    "apc_sentinelagent_scope_only": "SentinelAgent",
    "apc_sentinelagent_retained": "SentinelAgent",
    "apc_sentinelagent_fail_closed": "SentinelAgent",
}
SA_MAPPING = {
    "sentinelagent_alone": "T0",
    "sentinelagent_alone_variant": "T0-variant",
    "apc_sentinelagent_scope_only": "T0",
    "apc_sentinelagent_retained": "T2-attest",
    "apc_sentinelagent_fail_closed": "T1",
}


# ---------------------------------------------------------------------------
# Variant-aware manifest derivation
# ---------------------------------------------------------------------------

def t0_ops_variant(snapshot: ScopeSnapshot, tool: str, variant: str,
                   case: Any = None, args: dict[str, Any] | None = None,
                   call: Any = None) -> list[str]:
    """Manifest operation list for a call, parameterized by bridge variant.

    canonical: T0 as in sa_harness.t0_ops (resource ops from snapshot.handoff_resources;
    SEND endpoint from snapshot.recipient).
    v1: resource ops derive from case.role_resources (delegate's pre-narrowing role scope)
        instead of the post-handoff effective scope. SEND endpoint unchanged.
    v2: for calls that omit a recipient, the manifest SEND endpoint derives from the
        resolved argument (MockWorld default filled in) instead of the snapshot recipient.
        Resource ops unchanged.
    """
    args = args or {}
    if tool == "send_external":
        if variant == "v2" and call is not None and "recipient" not in dict(getattr(call, "args", {}) or {}):
            return [f"SEND {DEFAULT_RECIPIENT}"]
        return [f"SEND {snapshot.recipient}"]
    if variant == "v1" and case is not None:
        return [f"{VERB[tool]} {r}" for r in case.role_resources]
    return sa_harness.t0_ops(snapshot, tool)


def call_args_raw(call: Any) -> dict[str, Any]:
    """Raw (pre-canonicalization) call arguments, to detect omitted recipients."""
    return dict(getattr(call, "args", {}) or {})


def build_presented_variant(case: SACase, snapshot: ScopeSnapshot, call: Any,
                            args: dict[str, Any], sequence: int, variant: str):
    """Build the presented token with variant-aware manifest derivation."""
    tool = call.tool
    token_id = f"tau-{case.id}-{sequence:02d}"
    provenance = getattr(case, "token_provenance", "bridge")
    if provenance == "bridge":
        ops = t0_ops_variant(snapshot, tool, variant, case=case, args=args, call=call)
        token = make_token(token_id, call.actor, tool, ops,
                           f"one-step bridge call: {tool}", expiry_for(snapshot))
        minter, signer = "bridge", "bridge-key"
    elif provenance == "foreign_signer":
        ops = sa_harness.t0_ops(snapshot, tool)
        token = make_token(token_id, call.actor, tool, ops,
                           f"one-step bridge call: {tool}", expiry_for(snapshot))
        sa_harness.sign_foreign(token)
        minter, signer = "bridge", "foreign-key"
    elif provenance == "delegate":
        value = getattr(case, "presented_resource", "") or sa_harness.authority_value(call, args)
        token = make_token(token_id, call.actor, tool, [f"{VERB[tool]} {value}"],
                           f"delegate-minted call: {tool}", expiry_for(snapshot))
        minter, signer = "delegate", "bridge-key"
    else:
        raise ValueError(f"unknown token provenance {provenance!r}")
    return {"token": token, "minter": minter, "signer": signer}


def expiry_for(snapshot: ScopeSnapshot) -> float:
    return EXPIRY_PAST if snapshot.status == "expired" else EXPIRY_CURRENT


# ---------------------------------------------------------------------------
# Per-case arm runner (arms 2, 2v, 5, 6, 7); arm 1 uses run_case_v2.
# ---------------------------------------------------------------------------

def run_case_boundary(case: SACase, arm: str, variant: str) -> dict[str, Any]:
    if arm not in BOUNDARY_ARMS:
        raise ValueError(f"run_case_boundary handles {BOUNDARY_ARMS}; got {arm!r}")
    world = MockWorld(case)
    oracle = V2Oracle(case)
    # Arms 2 and 2v are standalone (no APC anywhere); arms 5/6/7 run shadow APC first.
    apc: APCV2 | None = None if arm in ("sentinelagent_alone", "sentinelagent_alone_variant") else APCV2(case)
    events: list[dict[str, Any]] = []
    handoff: dict[str, Any] = {}
    sequence = 0
    last_gate: dict[str, Any] | None = None
    attestations: list[dict[str, Any]] = []

    for phase, calls in (("prelude", case.prelude), ("downstream", case.attempts)):
        if phase == "downstream":
            if apc is not None:
                before = apc.state()
                apc.handoff(reset=False, fresh_pdp=False)
                handoff = {"before": before, "after": apc.state(), "snapshot": apc.snapshot().to_dict()}
            else:
                handoff = {"before": None, "after": None, "snapshot": case_snapshot(case).to_dict()}

        for index, call in enumerate(calls):
            sequence += 1
            try:
                args = world.canonical(call)
            except (TypeError, KeyError) as error:
                events.append(_event_boundary(phase, index, call, dict(call.args),
                                              ["invalid_tool_signature"], False,
                                              [str(error)], ["mock_tool_signature"], [], 0))
                continue

            oracle_reasons = oracle.decide(call, args, phase)
            evaluated = phase == "downstream" or arm in ("sentinelagent_alone", "sentinelagent_alone_variant")

            if evaluated:
                snapshot = apc.snapshot() if (apc is not None and phase == "downstream") else case_snapshot(case)
                presented: dict[str, Any] | None = None
                attestation: dict[str, Any] | None = None
                shadow: dict[str, Any] | None = None
                start = time.perf_counter_ns()
                if arm in ("sentinelagent_alone", "sentinelagent_alone_variant"):
                    presented = build_presented_variant(case, snapshot, call, args, sequence, variant)
                    result = evaluate_presented(snapshot, call, args, presented, None)
                else:
                    assert apc is not None
                    pre_snapshot = apc.snapshot()
                    pre_remaining = pre_snapshot.budget_ceiling - pre_snapshot.budget_consumed
                    shadow_decision = apc.authorize(call, args)
                    shadow = {
                        "allowed": shadow_decision.allowed,
                        "reasons": list(shadow_decision.reasons),
                        "checked_by": list(shadow_decision.checked_by),
                        "pre_budget_remaining": pre_remaining,
                    }
                    if arm == "apc_sentinelagent_scope_only":
                        presented = build_presented_variant(case, pre_snapshot, call, args, sequence, variant)
                        result = evaluate_presented(pre_snapshot, call, args, presented, None)
                    elif arm == "apc_sentinelagent_retained":
                        attestation = build_attestation(case, pre_snapshot, call, args, sequence,
                                                        shadow_decision.allowed,
                                                        list(shadow_decision.reasons), pre_remaining)
                        presented = build_presented_variant(case, pre_snapshot, call, args, sequence, variant)
                        result = evaluate_presented(pre_snapshot, call, args, presented, attestation)
                    else:  # apc_sentinelagent_fail_closed
                        if not shadow_decision.allowed:
                            result = sa_harness.SAGateResult(admitted=False, code="SHADOW-DENY",
                                                             reasons=list(shadow_decision.reasons),
                                                             checks={"shadow_allowed": False},
                                                             mapping_note="upstream APC denial retained")
                        else:
                            refusal = t1_refusal(case, pre_snapshot, call, args)
                            if refusal:
                                result = sa_harness.SAGateResult(admitted=False, code=refusal, reasons=[refusal],
                                                                 checks={"t1_refused": True},
                                                                 mapping_note="T1 fail-closed refusal")
                            else:
                                presented = build_presented_variant(case, pre_snapshot, call, args, sequence, variant)
                                result = evaluate_presented(pre_snapshot, call, args, presented, None)
                                chain = chain_refusal(presented["token"]) if presented is not None else None
                                if chain:
                                    result = sa_harness.SAGateResult(admitted=False, code=chain, reasons=[chain],
                                                                     checks={"t1_refused": True},
                                                                     mapping_note="T1 chain refusal")
                elapsed = time.perf_counter_ns() - start

                allowed = result.admitted
                effects = world.execute(call, args) if allowed else []
                if effects:
                    oracle.observe(call, effects)
                gate_dict = result.to_dict()
                gate_dict["presented"] = presented_meta(presented)
                last_gate = gate_dict
                event = _event_boundary(phase, index, call, args, oracle_reasons, allowed,
                                        result.reasons, SA_CHECKED_BY[arm], effects, elapsed,
                                        gate=gate_dict, shadow=shadow)
                token_block = presented_meta(presented) if presented is not None else {"presented": False}
                event["token"] = token_block
                if attestation is not None:
                    event["attestation"] = sa_harness.attestation_meta(attestation)
                    attestations.append(event["attestation"])
                sig_ok = token_block.get("signature_ok") if presented is not None else None
                event["unauthorized_effect"] = bool(
                    (oracle_reasons and effects) or (allowed and presented is not None and not sig_ok))
                event["false_denial"] = bool(
                    (not oracle_reasons) and (not allowed) and not (presented is not None and not sig_ok))
                events.append(event)
                continue

            assert apc is not None
            start = time.perf_counter_ns()
            decision = apc.authorize(call, args)
            elapsed = time.perf_counter_ns() - start
            allowed = decision.allowed
            effects = world.execute(call, args) if allowed else []
            if effects:
                oracle.observe(call, effects)
            events.append(_event_boundary(phase, index, call, args, oracle_reasons, allowed,
                                          list(decision.reasons), ["APC-shadow"], effects, elapsed,
                                          shadow={"allowed": allowed, "reasons": list(decision.reasons)}))

    return {
        "case": case.to_dict(),
        "arm": arm,
        "variant": variant,
        "pair": "sentinelagent",
        "mechanism": SA_MECHANISM[arm],
        "mapping": SA_MAPPING[arm],
        "handoff": handoff,
        "events": events,
        "attestations": attestations,
        "final_state": (apc.state() if apc is not None else {"gate": last_gate}),
        "oracle_state": {
            "spent": oracle.total_cost,
            "confidential_read": oracle.confidential_read,
            "external_send": oracle.external_send,
        },
    }


# ---------------------------------------------------------------------------
# Event constructor (mirrors arms._event / sa_harness shape)
# ---------------------------------------------------------------------------

def _event_boundary(phase, index, call, args, oracle_reasons, allowed, reasons,
                    checked_by, effects, authorization_ns, gate=None, shadow=None) -> dict[str, Any]:
    from dataclasses import asdict
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
    }


# ---------------------------------------------------------------------------
# Controls (S1-S3) re-run for the boundary matrix
# ---------------------------------------------------------------------------

def run_controls_boundary() -> dict[str, Any]:
    """Re-run the S1-S3 key/signature/attestation controls (sa_harness.run_controls_sa)."""
    return sa_harness.run_controls_sa()


def install_bridge_key_boundary() -> dict[str, Any]:
    return install_bridge_key()
