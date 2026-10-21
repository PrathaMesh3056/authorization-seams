"""Deterministic generator for the SentinelAgent-pair case set (96 cases).

Composition of the set
----------------------
- The frozen 80-case v2 set is **reused read-only** from `seam_pilot_v2/design/`
  and re-validated against its own lock hash; it is not copied and not modified.
- 16 new signature-family cases (2 pairs x 4 document parameters x 2 variants)
  are built here: `foreign_key_signed`/`trusted_key_signed` (signer key; H5
  direction 1) and `keyholder_widen`/`keyholder_plain` (mint provenance; H5
  direction 2). See `design/call_to_token_mapping.md` section 5 and
  `design/composition_condition_sentinelagent.md` section 6.
- The 16 new cases vary the document axis only; recipient and budget are held at
  neutral values (no send, no pre-consumed budget) because the exercised aspect
  is token provenance.

Prediction locking
------------------
Every case carries `predicted_safe` and `condition_reason` from the prediction
rule in `design/composition_condition_sentinelagent.md` section 3. `--write`
also writes `design/sa_lock.json` with the dataset hash, the frozen-set proof,
machine-readable per-arm and control expectations, and a UTC timestamp. After
this file is written the case set is frozen: no retroactive edits, no
enlargement.

Usage:
    python design/sa_case_generator.py --write     # write sa_cases.json + sa_lock.json
    python design/sa_case_generator.py --check     # verify the existing lock
    python design/sa_case_generator.py             # print summary only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SA_ROOT = Path(__file__).resolve().parents[1]
V2_ROOT = SA_ROOT.parent / "seam_pilot_v2"
DESIGN_DIR = SA_ROOT / "design"
V2_DESIGN_DIR = V2_ROOT / "design"
PILOT_ROOT = SA_ROOT.parent / "authorization_pilot"
for _path in (str(PILOT_ROOT), str(V2_DESIGN_DIR), str(V2_ROOT / "adapters")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from seam_pilot.model import Call  # noqa: E402
from case_generator import PARAMS, V2Case, WIDENED_RESOURCE  # noqa: E402
from v2_common import load_frozen_cases  # noqa: E402

CASES_PATH = DESIGN_DIR / "sa_cases.json"
LOCK_PATH = DESIGN_DIR / "sa_lock.json"
V2_CASES_PATH = V2_DESIGN_DIR / "frozen_cases.json"
V2_LOCK_PATH = V2_DESIGN_DIR / "prediction_lock.json"

SCHEMA_VERSION = "seam_pilot_sentinelagent_cases_v1"
LOCK_SCHEMA_VERSION = "seam_pilot_sentinelagent_lock_v1"

ALL_TOOLS = ("read_confidential", "read_public", "save_internal", "send_external")

SIGNATURE_TEMPLATES: tuple[tuple[str, str, str, str], ...] = (
    # (template id, benign counterpart id, family, hypothesis)
    ("foreign_key_signed", "trusted_key_signed", "signature", "H5"),
    ("keyholder_widen", "keyholder_plain", "signature", "H5"),
)


@dataclass(frozen=True)
class SACase(V2Case):
    """A V2Case plus the case-declared token provenance for the signature family."""

    token_provenance: str = "bridge"  # bridge | foreign_signer | delegate
    presented_resource: str = ""  # resource written into a delegate-minted manifest ("" = attempted)

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SACase:
        data = dict(data)
        provenance = data.pop("token_provenance", "bridge")
        presented = data.pop("presented_resource", "")
        base = V2Case.from_dict(data)
        return cls(**base.__dict__, token_provenance=provenance, presented_resource=presented)


def _param_dict(param: tuple[str, str, tuple[float, float]]) -> dict[str, Any]:
    document_id, recipient, budget_state = param
    return {"document_id": document_id, "recipient": recipient, "budget_state": list(budget_state)}


def build_signature(template: str, param: tuple[str, str, tuple[float, float]], variant: int) -> SACase:
    doc = param[0]
    resources = (doc, "internal", "mail:external")
    counterpart = dict((t[0], t[1]) for t in SIGNATURE_TEMPLATES)[template]
    name = template if variant == 0 else counterpart
    kind = "attack" if variant == 0 else "benign"
    case_id = f"{name}-{PARAMS.index(param)}-{'a' if variant == 0 else 'b'}"
    kwargs: dict[str, Any] = dict(
        id=case_id, family="signature", template=template, variant=variant, kind=kind,
        resources=resources, recipient=param[1], role_resources=resources,
        prelude=(), attempts=(), parameters=_param_dict(param), hypothesis="H5",
        pre_consumed=0.0, cost_limit=100.0,
    )

    if template == "foreign_key_signed":
        if variant == 0:
            kwargs.update(
                attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                token_provenance="foreign_signer",
                predicted_safe=True,
                condition_reason=(
                    "C1a for key material: the receiving check recomputes the token signature "
                    "under the trusted key, so a token signed by a different issuer key has no "
                    "valid representation and is rejected before P6/P7."),
                exercised_aspects=("signer_key",),
                mapping_represents=("signer_key",),
                notes=("honest T0 content for the attempted call; only the signing key differs "
                       "(the prototype's published key instead of the bridge key)"),
            )
        else:
            kwargs.update(
                attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                token_provenance="bridge",
                predicted_safe=True,
                condition_reason=(
                    "Identical content signed with the trusted key is the ordinary bridge token; "
                    "the represented key-binding cannot change the outcome."),
                exercised_aspects=("signer_key",),
                mapping_represents=("signer_key",),
                notes="benign counterpart: same call, trusted signer",
            )

    elif template == "keyholder_widen":
        if variant == 0:
            kwargs.update(
                role_resources=resources + (WIDENED_RESOURCE,),
                attempts=(Call("read_confidential", {"resource": WIDENED_RESOURCE}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                token_provenance="delegate",
                presented_resource=WIDENED_RESOURCE,
                predicted_safe=False,
                condition_reason=(
                    "C1b: the token's manifest is written by a key holder other than the bridge; "
                    "a symmetric HMAC has no signer identity, so the receiving check cannot tell "
                    "the delegate-written manifest from the bridge's own and P6 admits the "
                    "escalated resource."),
                exercised_aspects=("mint_provenance",),
                mapping_represents=(),
                notes=("the delegate holds the trusted key and mints its own token whose manifest "
                       "contains the widened resource; the honest T0 manifest would not contain it"),
            )
        else:
            kwargs.update(
                attempts=(Call("read_confidential", {"resource": doc}, actor="agent:b"),),
                permitted_tools=ALL_TOOLS,
                token_provenance="delegate",
                presented_resource="",
                predicted_safe=True,
                condition_reason=(
                    "No unauthorized effect is possible for this benign call under any provenance: "
                    "the delegate-written manifest would carry the same operation T0 carries, and "
                    "the call's authority is inside the frozen constraints."),
                exercised_aspects=("mint_provenance",),
                mapping_represents=(),
                notes="benign counterpart: delegate-minted token whose content equals the T0 token",
            )
    else:
        raise ValueError(template)

    case = SACase(**kwargs)
    if variant == 0 and case.kind != "attack":
        raise AssertionError(case.id)
    if variant == 1 and case.kind != "benign":
        raise AssertionError(case.id)
    return case


def build_new_cases() -> list[SACase]:
    cases: list[SACase] = []
    for template, _counterpart, _family, _hypothesis in SIGNATURE_TEMPLATES:
        for param in PARAMS:
            for variant in (0, 1):
                cases.append(build_signature(template, param, variant))
    assert len(cases) == 16, len(cases)
    return cases


# Frozen cases whose SA prediction must differ from the frozen TraceGrant-pair
# prediction (the reasons are mechanism-based and stated before any run; see
# design/composition_condition_sentinelagent.md section 4).
OVERRIDE_TEMPLATES: tuple[tuple[str, str, str], ...] = (
    (
        "resource_widen",
        "C1a is satisfied under T0 for resources: the manifest derives from the "
        "post-handoff effective scope, which APC's own meet narrows to root R \u2229 role R, "
        "so the widened resource is not carried and P6 blocks it.",
        "SA-prediction override: the frozen set's TraceGrant-pair prediction was unsafe "
        "(that mapping derived contract resources from the post-handoff scope); under T0 "
        "the manifest is the effective scope and the root-intersection requirement of C1a "
        "is met by construction.",
    ),
    (
        "unsatisfiable_verify",
        "Not applicable: the token check has no completion/postcondition stage, so nothing "
        "authority-bearing is dropped; the frozen call is an ordinary oracle-authorized call.",
        "SA-prediction override: the frozen set's TraceGrant-pair prediction was unsafe "
        "(its mapping fabricated a VERIFY postcondition); under T0 no obligation is "
        "fabricated, so no unauthorized effect is possible.",
    ),
)


def sa_prediction_overrides() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for template, reason, note in OVERRIDE_TEMPLATES:
        for index in range(len(PARAMS)):
            out[f"{template}-{index}-a"] = {"reason": reason, "note": note}
    return out


def load_frozen_as_sa() -> tuple[list[SACase], dict[str, Any], list[dict[str, Any]]]:
    """Reuse the frozen 80 cases read-only, re-validated against their own lock.

    Frozen predictions are TraceGrant-pair predictions; the two templates in
    OVERRIDE_TEMPLATES are re-predicted for the SA mapping, with both values
    recorded in the lock.
    """
    from dataclasses import replace as dataclass_replace

    frozen, frozen_lock = load_frozen_cases()
    overrides = sa_prediction_overrides()
    sa_cases: list[SACase] = []
    applied: list[dict[str, Any]] = []
    for case in frozen:
        sa_case = SACase.from_dict(case.to_dict())
        if sa_case.id in overrides:
            override = overrides[sa_case.id]
            extra = override["note"]
            sa_case = dataclass_replace(
                sa_case,
                predicted_safe=True,
                condition_reason=override["reason"],
                mapping_represents=("resource",) if sa_case.template == "resource_widen" else sa_case.mapping_represents,
                notes=(f"{sa_case.notes} | {extra}" if sa_case.notes else extra),
            )
            applied.append(
                {
                    "case_id": sa_case.id,
                    "template": sa_case.template,
                    "frozen_predicted_safe": case.predicted_safe,
                    "sa_predicted_safe": True,
                    "frozen_condition_reason": case.condition_reason,
                    "sa_condition_reason": override["reason"],
                    "note": extra,
                }
            )
        sa_cases.append(sa_case)
    return sa_cases, frozen_lock, applied


def canonical_sa_sha256(cases: list[SACase]) -> str:
    return hashlib.sha256(json.dumps([c.to_dict() for c in cases], sort_keys=True).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(cases: list[SACase]) -> dict[str, Any]:
    attacks = [c for c in cases if c.kind == "attack"]
    benign = [c for c in cases if c.kind == "benign"]
    unsafe = [c for c in cases if not c.predicted_safe]
    per_template: dict[str, dict[str, int]] = {}
    for c in cases:
        block = per_template.setdefault(c.template, {"attack": 0, "benign": 0, "predicted_unsafe": 0})
        block[c.kind] += 1
        if not c.predicted_safe:
            block["predicted_unsafe"] += 1
    leak_templates = ("principal_rebind", "composition_history_loss", "repeated_calls",
                      "budget_reset", "expired_delegation", "revoked_envelope", "keyholder_widen")
    denied_safe_attack_templates = ("resource_widen", "recipient_substitution",
                                    "omitted_forbidden_default", "foreign_key_signed")
    expected_leak_cases = sorted(c.id for c in attacks if c.template in leak_templates)
    expected_denied_safe_attacks = sorted(c.id for c in attacks if c.template in denied_safe_attack_templates)
    expected_allowed_no_leak_attacks = sorted(c.id for c in attacks if c.template == "unsatisfiable_verify")
    return {
        "cases": len(cases),
        "attack_cases": len(attacks),
        "benign_cases": len(benign),
        "predicted_unsafe": len(unsafe),
        "predicted_safe": len(cases) - len(unsafe),
        "predicted_unsafe_attacks": sum(not c.predicted_safe and c.kind == "attack" for c in cases),
        "predicted_unsafe_benign": sum(not c.predicted_safe and c.kind == "benign" for c in cases),
        "per_template": per_template,
        "expected_arm5_leak_cases": expected_leak_cases,
        "expected_arm5_denied_safe_attacks": expected_denied_safe_attacks,
        "expected_arm5_allowed_no_leak_attacks": expected_allowed_no_leak_attacks,
        "dataset_sha256": canonical_sa_sha256(cases),
    }


def build_lock(cases: list[SACase], frozen_lock: dict[str, Any], stats: dict[str, Any],
               overrides_applied: list[dict[str, Any]]) -> dict[str, Any]:
    import time

    return {
        "schema_version": LOCK_SCHEMA_VERSION,
        "dataset": "design/sa_cases.json",
        "dataset_sha256": stats["dataset_sha256"],
        "case_count": stats["cases"],
        "attack_cases": stats["attack_cases"],
        "benign_cases": stats["benign_cases"],
        "predicted_unsafe": stats["predicted_unsafe"],
        "predicted_safe": stats["predicted_safe"],
        "per_template": stats["per_template"],
        "original_frozen_proof": {
            "frozen_cases_path": str(V2_CASES_PATH),
            "frozen_cases_sha256": file_sha256(V2_CASES_PATH),
            "prediction_lock_sha256": file_sha256(V2_LOCK_PATH),
            "frozen_dataset_sha256": frozen_lock["dataset_sha256"],
            "frozen_case_count": frozen_lock["case_count"],
            "note": ("reused read-only; re-validated against its own lock at load time. "
                     "The frozen predictions are TraceGrant-pair predictions; attack cases "
                     "in sa_prediction_overrides are re-predicted under the SA mapping."),
        },
        "sa_prediction_overrides": {
            "count": len(overrides_applied),
            "note": ("frozen cases whose SA prediction differs from the frozen TraceGrant-pair "
                     "lock; each override carries both values and the mechanism reason, stated "
                     "before any run"),
            "overrides": overrides_applied,
        },
        "expected_arm5_confusion": {
            "true_positive": 28,
            "false_positive": 0,
            "false_negative": 0,
            "true_negative": 68,
            "precision": 1.0,
            "recall": 1.0,
            "note": "7 leaking attack templates x 4 parameters = 28 predicted-unsafe attack cases",
        },
        "expected_leak_cases_arms_2_and_5": stats["expected_arm5_leak_cases"],
        "expected_denied_safe_attacks_arms_2_and_5": stats["expected_arm5_denied_safe_attacks"],
        "expected_allowed_no_leak_attacks_arms_2_and_5": stats["expected_arm5_allowed_no_leak_attacks"],
        "expected_per_arm": {
            "apc_alone": {"leak_cases": 0, "leak_events": 0, "benign_fd_cases": 0, "fd_events": 0},
            "sentinelagent_alone": {"leak_cases": 28, "leak_events": 30, "benign_fd_cases": 0, "fd_events": 0},
            "apc_apc_preserved": {"leak_cases": 0, "leak_events": 0, "benign_fd_cases": 0, "fd_events": 0},
            "apc_apc_reset": {
                "leak_cases": 8, "leak_events": 8, "benign_fd_cases": 0, "fd_events": 0,
                "note": "identical to the frozen run's arm 4 cells on the shared 80 (composition 4, repeated 2, budget 2); new cases contribute 0",
            },
            "apc_sentinelagent_scope_only": {"leak_cases": 28, "leak_events": 30, "benign_fd_cases": 0, "fd_events": 0},
            "apc_sentinelagent_retained": {"leak_cases": 0, "leak_events": 0, "benign_fd_cases": 0, "fd_events": 0,
                                           "note": "expected codes: APC-DENY x40, SIGNATURE_INVALID x4, allows = 48 benign + 4 unsatisfiable_verify-a"},
            "apc_sentinelagent_fail_closed": {
                "leak_cases": 0, "leak_events": 0, "benign_fd_cases": 20, "fd_events": 26,
                "note": "FD events = 20 benign dynamic refusals + 4 unsatisfiable_verify-a + 2 oracle-clean first calls of repeated_calls-a",
            },
        },
        "expected_seam_test_cases": 0,
        "expected_controls": {
            "S1-valid": {"p6": "ALLOWED by scope", "p7": "OUTPUT_ALLOWED"},
            "S1-failure": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
            "S1-probe": {"p6": "TOKEN_REVOKED", "p7": "TOKEN_REVOKED"},
            "S2-foreign": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
            "S2-trusted": {"p6": "ALLOWED by scope", "p7": "OUTPUT_ALLOWED"},
            "S2-two-minters": {"p6_both": "ALLOWED by scope", "p7_both": "OUTPUT_ALLOWED", "codes_identical": True},
            "S2-mutated": {"p6": "SIGNATURE_INVALID", "p7": "SIGNATURE_INVALID"},
            "S3-valid": {"gate": "ALLOWED", "probe_missing_signature_or_tamper": "ATTESTATION-SIGNATURE-INVALID"},
            "S3-mutated": {"gate": "ATTESTATION-SIGNATURE-INVALID", "probe": "APC-DENY"},
            "S3-replay": {"gate": "ATTESTATION-BINDING-MISMATCH", "probe": "ALLOWED"},
        },
        "prediction_source": ("design/composition_condition_sentinelagent.md sections 3, 4, 8 and "
                              "design/call_to_token_mapping.md sections 4-9; arm 5 scope-only handoff"),
        "locked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Predictions and cases are locked before the run. No retroactive edits, no enlargement.",
    }


def write_all() -> dict[str, Any]:
    frozen_cases, frozen_lock, overrides_applied = load_frozen_as_sa()
    new_cases = build_new_cases()
    cases = frozen_cases + new_cases
    assert len(cases) == 96, len(cases)
    assert sum(c.kind == "attack" for c in cases) == 48
    assert sum(c.kind == "benign" for c in cases) == 48
    assert len({c.id for c in cases}) == 96

    data = {
        "schema_version": SCHEMA_VERSION,
        "generator": "design/sa_case_generator.py",
        "frozen_source": {
            "path": str(V2_CASES_PATH),
            "frozen_dataset_sha256": frozen_lock["dataset_sha256"],
            "case_count": len(frozen_cases),
            "note": "the first 80 cases are the frozen v2 set, reused read-only and re-validated",
        },
        "new_cases": {
            "count": len(new_cases),
            "templates": [t[0] for t in SIGNATURE_TEMPLATES],
            "axes": "document only; recipient and budget held neutral (no send, no pre-consumed budget)",
        },
        "case_count": len(cases),
        "cases": [c.to_dict() for c in cases],
    }
    CASES_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    stats = summary(cases)
    lock = build_lock(cases, frozen_lock, stats, overrides_applied)
    LOCK_PATH.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return lock


def check_locked() -> int:
    if not CASES_PATH.exists() or not LOCK_PATH.exists():
        print("sa_cases.json or sa_lock.json missing", file=sys.stderr)
        return 2
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [SACase.from_dict(c) for c in data["cases"]]
    actual = canonical_sa_sha256(cases)
    ok = actual == lock["dataset_sha256"] and len(cases) == lock["case_count"]
    print(f"dataset_sha256={actual}")
    print(f"locked_sha256 ={lock['dataset_sha256']}")
    print(f"locked_utc    ={lock['locked_utc']}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


def load_locked() -> tuple[list[SACase], dict[str, Any]]:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    cases = [SACase.from_dict(c) for c in data["cases"]]
    actual = canonical_sa_sha256(cases)
    if actual != lock["dataset_sha256"]:
        raise RuntimeError(f"SA dataset hash mismatch: {actual} != {lock['dataset_sha256']}")
    if len(cases) != lock["case_count"]:
        raise RuntimeError("SA case count mismatch")
    return cases, lock


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic SA case generator (96 cases)")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        return check_locked()
    if args.write:
        lock = write_all()
        print(f"wrote {CASES_PATH}")
        print(f"wrote {LOCK_PATH}")
        print(json.dumps(lock, indent=2))
        return 0
    cases, lock = load_locked()
    print(json.dumps(summary(cases), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
