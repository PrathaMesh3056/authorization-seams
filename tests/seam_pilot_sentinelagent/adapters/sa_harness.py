"""SentinelAgent-side harness: bridge token synthesis (T0/T1), attestation (T2),
and the receiving gate that runs the pinned prototype's own P6/P7 checks.

Reuses, read-only:
  - seam_pilot_v2: APCV2, ScopeSnapshot, V2Oracle, case_snapshot, load_frozen_cases,
    the v2 arms (arms 1/3/4 are executed by `arms.run_case` verbatim), the event
    constructor `arms._event`, and `shadow_evidence_values`/`resource_value`/
    `recipient_value` from tracegrant_adapter.
  - sentinelagent_audit_20261014/upstream: the pinned DelegationToken and
    DelegationAuthorityService. Files are not modified; only the module-level key
    constant `DAS_SECRET` is set to the harness bridge key at runtime
    (design/call_to_token_mapping.md section 6), before any token is constructed.

Arm semantics for this pair (design/call_to_token_mapping.md sections 4-10):
  2 sentinelagent_alone              T0 from the frozen case root scope; no APC anywhere.
  5 apc_sentinelagent_scope_only     shadow APC first; T0 from the pre-admission
                                     post-handoff snapshot; shadow denial recorded,
                                     not propagated.
  6 apc_sentinelagent_retained       shadow APC decision and pre-admission budget
                                     carried as a signature-verified attestation token
                                     (verified with the prototype's own
                                     verify_signature()).
  7 apc_sentinelagent_fail_closed    shadow denial retained; T1 refuses any
                                     untranslatable exercised aspect.
Arms 1/3/4 (`apc_alone`, `apc_apc_preserved`, `apc_apc_reset`) run through the reused
v2 runner (`arms.run_case`), which is byte-identical behavior for the shared 80 cases.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any

SA_ROOT = Path(__file__).resolve().parents[1]
RPAPER_ROOT = SA_ROOT.parent
V2_ROOT = RPAPER_ROOT / "seam_pilot_v2"
PILOT_ROOT = RPAPER_ROOT / "authorization_pilot"
SA_DESIGN = SA_ROOT / "design"
V2_DESIGN = V2_ROOT / "design"
V2_ADAPTERS = V2_ROOT / "adapters"
UPSTREAM_DIR = RPAPER_ROOT / "sentinelagent_audit_20261014" / "upstream"
UPSTREAM_FILE = UPSTREAM_DIR / "sentinelagent_das_prototype.py"

for _path in (str(SA_DESIGN), str(V2_ADAPTERS), str(V2_DESIGN), str(PILOT_ROOT), str(UPSTREAM_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import sentinelagent_das_prototype as sa_native  # noqa: E402
from seam_pilot.model import Call, MockWorld  # noqa: E402
from v2_common import (  # noqa: E402
    APCV2,
    ScopeSnapshot,
    V2Oracle,
    case_snapshot,
    load_frozen_cases,
)
from arms import _event  # noqa: E402
from tracegrant_adapter import recipient_value, resource_value, shadow_evidence_values  # noqa: E402
from sa_case_generator import SACase, load_locked  # noqa: E402

# ---------------------------------------------------------------------------
# Constants (locked in design/call_to_token_mapping.md sections 4-6)
# ---------------------------------------------------------------------------

SA_ARMS = (
    "apc_alone",
    "sentinelagent_alone",
    "apc_apc_preserved",
    "apc_apc_reset",
    "apc_sentinelagent_scope_only",
    "apc_sentinelagent_retained",
    "apc_sentinelagent_fail_closed",
)
SA_NEW_ARMS = (
    "sentinelagent_alone",
    "apc_sentinelagent_scope_only",
    "apc_sentinelagent_retained",
    "apc_sentinelagent_fail_closed",
)

BRIDGE_KEY = b"seam-pilot-sentinelagent-bridge-test-key-2026"
REAL_DAS_KEY = b"sentinelagent-das-secret-key-2026"
EXPIRY_CURRENT = 4102444800.0  # 2100-01-01Z; deterministic far-future constant
EXPIRY_PAST = 978307200.0  # 2001-01-01Z; deterministic past constant

VERB = {
    "read_confidential": "READ",
    "read_public": "READ",
    "save_internal": "WRITE",
    "send_external": "SEND",
}
STANDARD_TAG = {
    "read_confidential": "confidential_record",
    "read_public": "public_record",
    "save_internal": "internal_write",
    "send_external": "external_send",
}
DYNAMIC_ASPECTS = {"composition_history", "replay_state", "budget_consumed", "expiry", "revocation"}
REQUIRED_ATT_FIELDS = (
    "apc_allowed", "apc_reasons", "budget_remaining", "composition_clear", "freshness",
    "revoked", "principal", "task", "tool", "resource", "recipient", "evidence_digest",
)

SA_CHECKED_BY = {
    "sentinelagent_alone": ["SentinelAgent-alone"],
    "apc_sentinelagent_scope_only": ["SentinelAgent-scope-only"],
    "apc_sentinelagent_retained": ["APC-attestation", "SentinelAgent-retained"],
    "apc_sentinelagent_fail_closed": ["APC-shadow", "SentinelAgent-fail-closed"],
}
SA_MECHANISM = {
    "sentinelagent_alone": "SentinelAgent",
    "apc_sentinelagent_scope_only": "SentinelAgent",
    "apc_sentinelagent_retained": "SentinelAgent",
    "apc_sentinelagent_fail_closed": "SentinelAgent",
}
SA_MAPPING = {
    "sentinelagent_alone": "T0",
    "apc_sentinelagent_scope_only": "T0",
    "apc_sentinelagent_retained": "T2-attest",
    "apc_sentinelagent_fail_closed": "T1",
}


# ---------------------------------------------------------------------------
# Key material / trust relationship (call_to_token_mapping.md section 6)
# ---------------------------------------------------------------------------

def install_bridge_key() -> dict[str, Any]:
    """Set the prototype's module key constant to the harness bridge key.

    The upstream file is not edited; the module attribute is assigned in-process.
    Returns the proof block recorded in the run manifest.
    """
    raw = UPSTREAM_FILE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    original = bytes(sa_native.DAS_SECRET)
    if original != REAL_DAS_KEY:
        raise RuntimeError(f"unexpected upstream key constant: {original!r}")
    sa_native.DAS_SECRET = BRIDGE_KEY
    return {
        "upstream_file": str(UPSTREAM_FILE),
        "upstream_sha256": digest,
        "trusted_key_hex": BRIDGE_KEY.hex(),
        "original_das_key_hex": original.hex(),
        "note": ("module-level constant set at runtime; upstream file byte-identical; "
                 "models the trust relationship (receiver must hold the issuer's key)"),
    }


# ---------------------------------------------------------------------------
# Token synthesis
# ---------------------------------------------------------------------------

def authority_value(call: Call, args: dict[str, Any]) -> str:
    """The value P6 checks for this call: the canonical recipient or resource."""
    if call.tool == "send_external":
        return recipient_value(args)
    return resource_value(args)


def t0_ops(snapshot: ScopeSnapshot, tool: str) -> list[str]:
    if tool == "send_external":
        return [f"SEND {snapshot.recipient}"]
    return [f"{VERB[tool]} {r}" for r in snapshot.handoff_resources]


def expiry_for(snapshot: ScopeSnapshot) -> float:
    return EXPIRY_PAST if snapshot.status == "expired" else EXPIRY_CURRENT


def make_token(token_id: str, src: str, tool: str, ops: list[str], intent: str, expiry: float):
    return sa_native.DelegationToken(
        token_id=token_id,
        src=src,
        dst="mock-tool-executor",
        scope={tool},
        manifest={tool: list(ops)},
        output_schema={tool: {"permitted": [STANDARD_TAG[tool]], "prohibited": []}},
        policy=set(),
        parent_hash="ROOT",
        expiry=expiry,
        intent_text=intent,
    )


def sign_foreign(token: Any) -> None:
    """Re-sign the token's canonical payload with the prototype's published key."""
    token.signature = hmac.new(
        REAL_DAS_KEY, token._canonical().encode("utf-8"), hashlib.sha256
    ).hexdigest()


def build_presented(case: SACase, snapshot: ScopeSnapshot, call: Call, args: dict[str, Any],
                    sequence: int) -> dict[str, Any]:
    """The token the receiving check sees, per the case-declared provenance."""
    tool = call.tool
    token_id = f"tau-{case.id}-{sequence:02d}"
    provenance = getattr(case, "token_provenance", "bridge")
    if provenance == "bridge":
        token = make_token(token_id, call.actor, tool, t0_ops(snapshot, tool),
                           f"one-step bridge call: {tool}", expiry_for(snapshot))
        minter, signer = "bridge", "bridge-key"
    elif provenance == "foreign_signer":
        token = make_token(token_id, call.actor, tool, t0_ops(snapshot, tool),
                           f"one-step bridge call: {tool}", expiry_for(snapshot))
        sign_foreign(token)
        minter, signer = "bridge", "foreign-key"
    elif provenance == "delegate":
        value = getattr(case, "presented_resource", "") or authority_value(call, args)
        token = make_token(token_id, call.actor, tool, [f"{VERB[tool]} {value}"],
                           f"delegate-minted call: {tool}", expiry_for(snapshot))
        minter, signer = "delegate", "bridge-key"
    else:
        raise ValueError(f"unknown token provenance {provenance!r}")
    return {"token": token, "minter": minter, "signer": signer}


# ---------------------------------------------------------------------------
# Receiving checks (native P6/P7)
# ---------------------------------------------------------------------------

def native_check_with(svc: Any, token: Any, tool: str, value: str) -> dict[str, Any]:
    ok6, msg6 = svc.check_api_call(token.token_id, VERB[tool], value)
    ok7, msg7 = svc.check_output(token.token_id, {STANDARD_TAG[tool]})
    return {
        "p6_allowed": bool(ok6),
        "p6_message": msg6,
        "p7_allowed": bool(ok7),
        "p7_message": msg7,
        "signature_ok": bool(token.verify_signature()),
    }


def native_check(token: Any, tool: str, value: str) -> dict[str, Any]:
    svc = sa_native.DelegationAuthorityService()
    svc.tokens[token.token_id] = token
    return native_check_with(svc, token, tool, value)


# ---------------------------------------------------------------------------
# Attestation (arm 6)
# ---------------------------------------------------------------------------

def build_attestation(case: Any, snapshot: ScopeSnapshot, call: Call, args: dict[str, Any],
                      sequence: int, shadow_allowed: bool, shadow_reasons: list[str],
                      pre_remaining: float) -> dict[str, Any]:
    values = shadow_evidence_values(case, snapshot, call, args, shadow_allowed,
                                    list(shadow_reasons), pre_remaining)
    payload = {key: values[key] for key in REQUIRED_ATT_FIELDS}
    token = sa_native.DelegationToken(
        token_id=f"att-{getattr(case, 'id', 'control')}-{sequence:02d}",
        src="apc-bridge",
        dst="sentinelagent-receiver",
        scope={"apc-attestation"},
        manifest={"apc-attestation": [f"tool={call.tool}", f"apc_allowed={values['apc_allowed']}"]},
        output_schema={},
        policy=set(),
        parent_hash="ROOT",
        expiry=EXPIRY_CURRENT,
        intent_text=json.dumps(payload, sort_keys=True, default=str),
    )
    return {"token": token, "values": values}


def attestation_checks(snapshot: ScopeSnapshot, call: Call, args: dict[str, Any],
                       attestation: dict[str, Any], cost: float) -> tuple[bool, str, dict[str, Any]]:
    checks: dict[str, Any] = {"present": True}
    token = attestation["token"]
    ok = token.verify_signature()
    checks["signature_valid"] = bool(ok)
    if not ok:
        return False, "ATTESTATION-SIGNATURE-INVALID", checks
    try:
        payload = json.loads(token.intent_text)
    except (TypeError, ValueError):
        checks["payload_valid"] = False
        return False, "ATTESTATION-PAYLOAD-INVALID", checks
    checks["payload_valid"] = isinstance(payload, dict) and all(k in payload for k in REQUIRED_ATT_FIELDS)
    if not checks["payload_valid"]:
        return False, "ATTESTATION-PAYLOAD-INVALID", checks
    binding = {
        "tool": str(payload["tool"]) == call.tool,
        "resource": str(payload["resource"]) == resource_value(args),
        "recipient": str(payload["recipient"]) == recipient_value(args),
        "task": str(payload["task"]) == str(snapshot.task),
        "principal": str(payload["principal"]) == str(snapshot.principal),
    }
    checks["binding"] = binding
    checks["binding_ok"] = all(binding.values())
    if not checks["binding_ok"]:
        return False, "ATTESTATION-BINDING-MISMATCH", checks
    checks["apc_allowed"] = bool(payload["apc_allowed"])
    if not checks["apc_allowed"]:
        return False, "APC-DENY", checks
    checks["budget_ok"] = float(payload["budget_remaining"]) >= float(cost)
    if not checks["budget_ok"]:
        return False, "BUDGET-INSUFFICIENT", checks
    checks["freshness_ok"] = str(payload["freshness"]) in ("current", "renewed")
    if not checks["freshness_ok"]:
        return False, "FRESHNESS-INVALID", checks
    checks["revoked_ok"] = not bool(payload["revoked"])
    if not checks["revoked_ok"]:
        return False, "REVOKED-INVALID", checks
    checks["composition_ok"] = bool(payload["composition_clear"])
    if not checks["composition_ok"]:
        return False, "COMPOSITION-INVALID", checks
    return True, "ATTESTATION-OK", checks


# ---------------------------------------------------------------------------
# T1 refusals (arm 7)
# ---------------------------------------------------------------------------

def t1_refusal(case: SACase, snapshot: ScopeSnapshot, call: Call, args: dict[str, Any]) -> str | None:
    if call.tool not in snapshot.actions:
        return "T1-REFUSE:tool_untranslated"
    if call.tool == "send_external":
        if recipient_value(args) != snapshot.recipient:
            return "T1-REFUSE:recipient_untranslated"
    else:
        derivable = set(snapshot.root_resources) & set(snapshot.handoff_resources)
        if resource_value(args) not in derivable:
            return "T1-REFUSE:resource_untranslated"
    derivable_tags = {STANDARD_TAG[t] for t in snapshot.actions if t in STANDARD_TAG}
    if STANDARD_TAG[call.tool] not in derivable_tags:
        return "T1-REFUSE:tags_untranslated"
    if set(case.exercised_aspects) & DYNAMIC_ASPECTS:
        return "T1-REFUSE:dynamic_state_untranslated"
    if case.verify_kind == "unsatisfiable":
        return "T1-REFUSE:completion_untranslated"
    if call.actor != case.handoff_principal or call.session != case.handoff_task:
        return "T1-REFUSE:principal_untranslated"
    return None


def chain_refusal(token: Any) -> str | None:
    # T1 constructs one-hop tokens (parent "ROOT"); a non-ROOT parent could not be
    # resolved and is refused for completeness (vacuous under this construction).
    if token.parent_hash != "ROOT":
        return "T1-REFUSE:chain_untranslated"
    return None


# ---------------------------------------------------------------------------
# Gate result / gate evaluation
# ---------------------------------------------------------------------------

@dataclass
class SAGateResult:
    admitted: bool
    code: str
    reasons: list[str] = field(default_factory=list)
    checks: dict[str, Any] = field(default_factory=dict)
    mapping_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "code": self.code,
            "reasons": list(self.reasons),
            "checks": self.checks,
            "mapping_note": self.mapping_note,
        }


def evaluate_presented(snapshot: ScopeSnapshot, call: Call, args: dict[str, Any],
                       presented: dict[str, Any] | None,
                       attestation: dict[str, Any] | None) -> SAGateResult:
    checks: dict[str, Any] = {}
    if attestation is not None:
        ok, att_code, att_checks = attestation_checks(snapshot, call, args, attestation, float(call.cost))
        checks["attestation"] = att_checks
        if not ok:
            reasons = [att_code]
            payload_reasons = str(attestation["values"].get("apc_reasons", "") or "")
            if att_code == "APC-DENY" and payload_reasons:
                reasons.append(payload_reasons)
            return SAGateResult(admitted=False, code=att_code, reasons=reasons, checks=checks,
                                mapping_note="signed APC attestation denied the call")
    if presented is None:
        return SAGateResult(admitted=False, code="NO-TOKEN", reasons=["no token presented"], checks=checks)
    native = native_check(presented["token"], call.tool, authority_value(call, args))
    checks["native"] = native
    if not native["p6_allowed"]:
        return SAGateResult(admitted=False, code=native["p6_message"], reasons=[native["p6_message"]],
                            checks=checks, mapping_note="native P6 refused the call")
    if not native["p7_allowed"]:
        return SAGateResult(admitted=False, code=native["p7_message"], reasons=[native["p7_message"]],
                            checks=checks, mapping_note="native P7 refused the output tags")
    return SAGateResult(admitted=True, code="ADMITTED", reasons=["P6_ALLOWED", "P7_ALLOWED"],
                        checks=checks, mapping_note="native P6 and P7 admitted the call")


def presented_meta(presented: dict[str, Any] | None) -> dict[str, Any] | None:
    if presented is None:
        return None
    token = presented["token"]
    return {
        "presented": True,
        "token_id": token.token_id,
        "src": token.src,
        "dst": token.dst,
        "scope": sorted(token.scope),
        "manifest": {k: sorted(v) for k, v in token.manifest.items()},
        "output_schema": {k: dict(v) for k, v in token.output_schema.items()},
        "policy": sorted(token.policy),
        "parent_hash": token.parent_hash,
        "expiry": token.expiry,
        "intent_text": token.intent_text,
        "minter": presented["minter"],
        "signer": presented["signer"],
        "signature": token.signature,
        "signature_ok": bool(token.verify_signature()),
    }


def attestation_meta(attestation: dict[str, Any] | None) -> dict[str, Any] | None:
    if attestation is None:
        return None
    token = attestation["token"]
    return {
        "token_id": token.token_id,
        "src": token.src,
        "dst": token.dst,
        "scope": sorted(token.scope),
        "manifest": {k: list(v) for k, v in token.manifest.items()},
        "expiry": token.expiry,
        "intent_text": token.intent_text,
        "signature": token.signature,
        "signature_ok": bool(token.verify_signature()),
    }


# ---------------------------------------------------------------------------
# The 4 new-arm runner (2/5/6/7)
# ---------------------------------------------------------------------------

def run_case_sa(case: SACase, arm: str) -> dict[str, Any]:
    if arm not in SA_NEW_ARMS:
        raise ValueError(f"run_case_sa handles {SA_NEW_ARMS}; arms 1/3/4 use arms.run_case")
    world = MockWorld(case)
    oracle = V2Oracle(case)
    apc: APCV2 | None = APCV2(case) if arm != "sentinelagent_alone" else None
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
                events.append(_event(phase, index, call, dict(call.args), ["invalid_tool_signature"],
                                     False, [str(error)], ["mock_tool_signature"], [], 0))
                continue

            oracle_reasons = oracle.decide(call, args, phase)
            evaluated = phase == "downstream" or arm == "sentinelagent_alone"

            if evaluated:
                snapshot = apc.snapshot() if (apc is not None and phase == "downstream") else case_snapshot(case)
                presented: dict[str, Any] | None = None
                attestation: dict[str, Any] | None = None
                shadow: dict[str, Any] | None = None
                start = time.perf_counter_ns()
                if arm == "sentinelagent_alone":
                    presented = build_presented(case, snapshot, call, args, sequence)
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
                        presented = build_presented(case, pre_snapshot, call, args, sequence)
                        result = evaluate_presented(pre_snapshot, call, args, presented, None)
                    elif arm == "apc_sentinelagent_retained":
                        attestation = build_attestation(case, pre_snapshot, call, args, sequence,
                                                        shadow_decision.allowed,
                                                        list(shadow_decision.reasons), pre_remaining)
                        presented = build_presented(case, pre_snapshot, call, args, sequence)
                        result = evaluate_presented(pre_snapshot, call, args, presented, attestation)
                    else:  # apc_sentinelagent_fail_closed
                        if not shadow_decision.allowed:
                            result = SAGateResult(admitted=False, code="SHADOW-DENY",
                                                  reasons=list(shadow_decision.reasons),
                                                  checks={"shadow_allowed": False},
                                                  mapping_note="upstream APC denial retained")
                        else:
                            refusal = t1_refusal(case, pre_snapshot, call, args)
                            if refusal:
                                result = SAGateResult(admitted=False, code=refusal, reasons=[refusal],
                                                      checks={"t1_refused": True},
                                                      mapping_note="T1 fail-closed refusal")
                            else:
                                presented = build_presented(case, pre_snapshot, call, args, sequence)
                                result = evaluate_presented(pre_snapshot, call, args, presented, None)
                                chain = chain_refusal(presented["token"]) if presented is not None else None
                                if chain:
                                    result = SAGateResult(admitted=False, code=chain, reasons=[chain],
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
                event = _event(phase, index, call, args, oracle_reasons, allowed,
                               result.reasons, SA_CHECKED_BY[arm], effects, elapsed,
                               gate=gate_dict, shadow=shadow)
                token_block = presented_meta(presented) if presented is not None else {"presented": False}
                event["token"] = token_block
                if attestation is not None:
                    event["attestation"] = attestation_meta(attestation)
                    attestations.append(event["attestation"])
                sig_ok = token_block.get("signature_ok") if presented is not None else None
                event["unauthorized_effect"] = bool(
                    (oracle_reasons and effects) or (allowed and presented is not None and not sig_ok))
                event["false_denial"] = bool(
                    (not oracle_reasons) and (not allowed) and not (presented is not None and not sig_ok))
                events.append(event)
                continue

            # prelude of arms 5/6/7: shadow APC only
            assert apc is not None
            start = time.perf_counter_ns()
            decision = apc.authorize(call, args)
            elapsed = time.perf_counter_ns() - start
            allowed = decision.allowed
            effects = world.execute(call, args) if allowed else []
            if effects:
                oracle.observe(call, effects)
            events.append(_event(phase, index, call, args, oracle_reasons, allowed,
                                 list(decision.reasons), ["APC-shadow"], effects, elapsed,
                                 shadow={"allowed": allowed, "reasons": list(decision.reasons)}))

    return {
        "case": case.to_dict(),
        "arm": arm,
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
# Controls S1 (freshness), S2 (signature), S3 (attestation)
# ---------------------------------------------------------------------------

def control_snapshot(status: str = "current") -> ScopeSnapshot:
    return ScopeSnapshot(
        source="control",
        root_resources=("control-doc",),
        handoff_resources=("control-doc",),
        actions=("read_confidential",),
        recipient="control@partner.test",
        principal="agent:b",
        task="root-task",
        budget_consumed=0.0,
        budget_ceiling=100.0,
        status=status,
        revoked=False,
    )


def _p6_allowed(message: str) -> bool:
    return message.startswith("ALLOWED by scope")


def run_controls_sa() -> dict[str, Any]:
    snapshot = control_snapshot()
    call = Call("read_confidential", {"resource": "control-doc"}, actor="agent:b")
    args = {"resource": "control-doc", "content": None}
    records: list[dict[str, Any]] = []

    # --- S1: freshness (expired token passes P6/P7) + failure control + revoked probe
    token = make_token("ctl-s1-valid", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: expired token", EXPIRY_PAST)
    obs = native_check(token, "read_confidential", "control-doc")
    records.append({
        "id": "S1-valid",
        "setup": "validly signed token with expiry in the past (2001-01-01Z) presented to native P6/P7",
        "expected": {"p6": "ALLOWED by scope", "p7": "OUTPUT_ALLOWED"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": bool(obs["p6_allowed"]) and bool(obs["p7_allowed"])
        and _p6_allowed(obs["p6_message"]) and obs["p7_message"] == "OUTPUT_ALLOWED",
    })

    token = make_token("ctl-s1-failure", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: mutated after signing", EXPIRY_PAST)
    token.manifest["read_confidential"] = ["READ other-doc"]
    obs = native_check(token, "read_confidential", "control-doc")
    records.append({
        "id": "S1-failure",
        "setup": "failure control: same token content, manifest mutated after signing",
        "expected": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": obs["p6_message"] == "SIGNATURE_INVALID" and obs["p7_message"] == "SIGNATURE_INVALID",
    })

    token = make_token("ctl-s1-probe", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: revocation probe", EXPIRY_CURRENT)
    svc = sa_native.DelegationAuthorityService()
    svc.tokens[token.token_id] = token
    revoked_count = svc.revoke_chain(token.token_id)
    obs = native_check_with(svc, token, "read_confidential", "control-doc")
    records.append({
        "id": "S1-probe",
        "setup": f"revoked via revoke_chain (count={revoked_count}); proves P6/P7 are not blanket no-ops",
        "expected": {"p6": "TOKEN_REVOKED", "p7": "TOKEN_REVOKED"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": obs["p6_message"] == "TOKEN_REVOKED" and obs["p7_message"] == "TOKEN_REVOKED",
    })

    # --- S2: signature (key material vs signer identity)
    token = make_token("ctl-s2-foreign", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: foreign key", EXPIRY_CURRENT)
    sign_foreign(token)
    obs = native_check(token, "read_confidential", "control-doc")
    records.append({
        "id": "S2-foreign",
        "setup": "T0 content signed with the prototype's published key (REAL_DAS_KEY)",
        "expected": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": obs["p6_message"] == "SIGNATURE_INVALID" and obs["p7_message"] == "SIGNATURE_INVALID",
    })

    token = make_token("ctl-s2-trusted", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: trusted key", EXPIRY_CURRENT)
    obs = native_check(token, "read_confidential", "control-doc")
    records.append({
        "id": "S2-trusted",
        "setup": "failure control for S2-foreign: identical content signed with the trusted bridge key",
        "expected": {"p6": "ALLOWED by scope", "p7": "OUTPUT_ALLOWED"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": _p6_allowed(obs["p6_message"]) and obs["p7_message"] == "OUTPUT_ALLOWED",
    })

    token_bridge = make_token("ctl-s2m-bridge", "agent:b", "read_confidential", ["READ control-doc"],
                              "control: bridge-minted", EXPIRY_CURRENT)
    token_delegate = make_token("ctl-s2m-delegate", "agent:b", "read_confidential", ["READ control-doc"],
                                "control: delegate-minted", EXPIRY_CURRENT)
    obs_bridge = native_check(token_bridge, "read_confidential", "control-doc")
    obs_delegate = native_check(token_delegate, "read_confidential", "control-doc")
    codes_identical = (obs_bridge["p6_message"] == obs_delegate["p6_message"]
                       and obs_bridge["p7_message"] == obs_delegate["p7_message"])
    records.append({
        "id": "S2-two-minters",
        "setup": ("identical scope/manifest/tags; one token attributed to the bridge, one to the "
                  "delegate (token ids differ only for auditability); both signed with the trusted key"),
        "expected": {"p6_both": "ALLOWED by scope", "p7_both": "OUTPUT_ALLOWED", "codes_identical": True},
        "observed": {"p6_bridge": obs_bridge["p6_message"], "p6_delegate": obs_delegate["p6_message"],
                     "p7_bridge": obs_bridge["p7_message"], "p7_delegate": obs_delegate["p7_message"],
                     "codes_identical": codes_identical},
        "ok": _p6_allowed(obs_bridge["p6_message"]) and _p6_allowed(obs_delegate["p6_message"])
        and obs_bridge["p7_message"] == "OUTPUT_ALLOWED" and obs_delegate["p7_message"] == "OUTPUT_ALLOWED"
        and codes_identical,
    })

    token = make_token("ctl-s2-mutated", "agent:b", "read_confidential", ["READ control-doc"],
                       "control: delegate minted, widened after signing", EXPIRY_CURRENT)
    token.manifest["read_confidential"] = ["READ control-doc", "READ other-doc"]
    obs = native_check(token, "read_confidential", "other-doc")
    records.append({
        "id": "S2-mutated",
        "setup": "failure control: delegate-minted token, manifest widened after signing without re-signing",
        "expected": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
        "observed": {"p6": obs["p6_message"], "p7": obs["p7_message"]},
        "ok": obs["p6_message"] == "SIGNATURE_INVALID" and obs["p7_message"] == "SIGNATURE_INVALID",
    })

    # --- S3: attestation gate
    ctl_case = SimpleNamespace(id="control", status="current")
    allowed_decision = SimpleNamespace(allowed=True, reasons=[])
    denied_decision = SimpleNamespace(allowed=False, reasons=["resource scope: control-doc"])
    attest = build_attestation(ctl_case, snapshot, call, args, 0, True, [], 100.0)
    ok, code, _checks = attestation_checks(snapshot, call, args, attest, 1.0)
    tampered = build_attestation(ctl_case, snapshot, call, args, 0, True, [], 100.0)
    sig = list(tampered["token"].signature)
    sig[0] = "0" if sig[0] != "0" else "1"
    tampered["token"].signature = "".join(sig)
    ok_t, code_t, _ = attestation_checks(snapshot, call, args, tampered, 1.0)
    records.append({
        "id": "S3-valid",
        "setup": "signed attestation for the control call; probe tampers one signature character",
        "expected": {"gate": "ALLOWED", "tamper": "ATTESTATION-SIGNATURE-INVALID"},
        "observed": {"gate": code, "tamper": code_t},
        "ok": ok and code == "ATTESTATION-OK" and code_t == "ATTESTATION-SIGNATURE-INVALID",
    })

    attested_denied = build_attestation(ctl_case, snapshot, call, args, 1, False,
                                        list(denied_decision.reasons), 100.0)
    mutated = build_attestation(ctl_case, snapshot, call, args, 1, False,
                                list(denied_decision.reasons), 100.0)
    payload = json.loads(mutated["token"].intent_text)
    payload["apc_allowed"] = True
    mutated["token"].intent_text = json.dumps(payload, sort_keys=True, default=str)
    ok_m, code_m, _ = attestation_checks(snapshot, call, args, mutated, 1.0)
    ok_d, code_d, _ = attestation_checks(snapshot, call, args, attested_denied, 1.0)
    records.append({
        "id": "S3-mutated",
        "setup": "failure control: apc_allowed flipped to true after signing; probe is the unmutated denied attestation",
        "expected": {"gate": "ATTESTATION-SIGNATURE-INVALID", "probe": "APC-DENY"},
        "observed": {"gate": code_m, "probe": code_d},
        "ok": (not ok_m) and code_m == "ATTESTATION-SIGNATURE-INVALID" and (not ok_d) and code_d == "APC-DENY",
    })

    attest = build_attestation(ctl_case, snapshot, call, args, 2, True, [], 100.0)
    replay_args = {"resource": "other-doc", "content": None}
    call_replay = Call("read_confidential", {"resource": "other-doc"}, actor="agent:b")
    ok_r, code_r, _ = attestation_checks(snapshot, call_replay, replay_args, attest, 1.0)
    ok_p, code_p, _ = attestation_checks(snapshot, call, args, attest, 1.0)
    records.append({
        "id": "S3-replay",
        "setup": "valid attestation bound to the control call presented for a different resource",
        "expected": {"gate": "ATTESTATION-BINDING-MISMATCH", "probe": "ALLOWED"},
        "observed": {"gate": code_r, "probe": code_p},
        "ok": (not ok_r) and code_r == "ATTESTATION-BINDING-MISMATCH" and ok_p and code_p == "ATTESTATION-OK",
    })

    return {"records": records, "ok": all(r["ok"] for r in records)}
