"""Extension E1 runner: 8 action-narrow cases x arms 1, 2, 5, 6, 7 = 40 executions
plus the 3 M2-auth signature controls (own denominator, 6 executions).

Strictly sequential; no network; no paid calls; nothing re-runs or re-scores the
original 80 cases or the original arms 3/4. Artifacts -> results/extension_e1/.

Usage:
    python run_extension_e1.py            # run the extension, write artifacts
    python run_extension_e1.py --check    # verify the extension lock only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

V2_ROOT = Path(__file__).resolve().parent
DESIGN = V2_ROOT / "design"
RESULTS = V2_ROOT / "results" / "extension_e1"
LOGS = V2_ROOT / "logs"
sys.path.insert(0, str(V2_ROOT / "adapters"))
sys.path.insert(0, str(DESIGN))

from v2_common import MockWorld, prepare  # noqa: E402
from seam_pilot.native import provenance  # noqa: E402

from extension_e1_generator import E1Case, check_cases, load_locked  # noqa: E402
from extension_e1 import (  # noqa: E402
    E1_ARMS,
    AuthenticatedEvidenceGate,
    ExtensionAPC,
    run_case_e1,
    signed_evidence_values,
)
from metrics_v2 import case_false_denial, case_leaked, condition_confusion, summarize  # noqa: E402

E1_CHECK_NAMES = {
    "apc_alone": "A1",
    "tracegrant_alone": "A2",
    "apc_tracegrant_scope_only": "A5",
    "apc_tracegrant_retained": "A6",
    "apc_tracegrant_fail_closed": "A7",
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    with (LOGS / "extension_e1.log").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


# ---------------------------------------------------------------------------
# Matrix
# ---------------------------------------------------------------------------

def run_matrix(cases: list[E1Case], lock: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for arm in E1_ARMS:
        log(f"E1 matrix: arm {arm} ({len(cases)} cases)")
        for case in cases:
            runs.append(run_case_e1(case, arm))
    if len(runs) != len(cases) * len(E1_ARMS):
        raise AssertionError("matrix size mismatch")
    if any(not run["events"] for run in runs):
        raise AssertionError("an execution produced no events")

    metrics = summarize(runs, E1_ARMS)
    confusion = condition_confusion(runs, "apc_tracegrant_scope_only")
    leaked = {arm: sorted(r["case"]["id"] for r in runs if r["arm"] == arm and case_leaked(r))
              for arm in E1_ARMS}
    false_denials = {arm: sorted(r["case"]["id"] for r in runs if r["arm"] == arm and case_false_denial(r))
                     for arm in E1_ARMS}
    codes: dict[str, dict[str, int]] = {}
    for arm in E1_ARMS:
        block: dict[str, int] = {}
        for run in runs:
            if run["arm"] != arm:
                continue
            for event in run["events"]:
                code = (event.get("gate") or {}).get("code") or event["checked_by"][0]
                block[code] = block.get(code, 0) + 1
        codes[arm] = block

    assertions: list[dict[str, Any]] = []
    for arm in E1_ARMS:
        expected = lock["expected_by_arm"][arm]
        observed = {"attack_leaks": len(leaked[arm]), "benign_false_denials": len(false_denials[arm])}
        assertions.append({
            "arm": arm,
            "expected": {"attack_leaks": expected["attack_leaks"],
                         "benign_false_denials": expected["benign_false_denials"]},
            "observed": observed,
            "passed": bool(observed["attack_leaks"] == expected["attack_leaks"]
                           and observed["benign_false_denials"] == expected["benign_false_denials"]),
        })

    per_case = {arm: {r["case"]["id"]: case_leaked(r) for r in runs if r["arm"] == arm} for arm in E1_ARMS}
    seam_offenders = sorted(
        cid for cid in per_case["apc_alone"]
        if not per_case["apc_alone"][cid] and not per_case["tracegrant_alone"][cid]
        and any(per_case[a][cid] for a in ("apc_tracegrant_scope_only",
                                           "apc_tracegrant_retained",
                                           "apc_tracegrant_fail_closed")))
    same_set_arm2_arm5 = leaked["tracegrant_alone"] == leaked["apc_tracegrant_scope_only"]

    assertion_summary = {
        "assertions": assertions,
        "passed": all(a["passed"] for a in assertions),
        "seam_offenders": seam_offenders,
        "seam_note": ("cases where arms 1 and 2 were safe but arms 5/6/7 were unsafe "
                      "(the original seam-test definition, reused verbatim)"),
        "same_set_arm2_arm5": bool(same_set_arm2_arm5),
        "leaked_ids": leaked,
        "benign_false_denial_ids": false_denials,
        "gate_codes": codes,
    }
    if not assertion_summary["passed"]:
        log("E1 matrix: LOCKED PREDICTION MISMATCH -> reported as-is (no retroactive edits)")
    return runs, assertion_summary


# ---------------------------------------------------------------------------
# M2-auth controls (own denominator)
# ---------------------------------------------------------------------------

def _call_context(case: E1Case) -> tuple[Any, dict[str, Any], Any, float, Any]:
    world = MockWorld(case)
    call = case.attempts[0]
    args = world.canonical(call)
    apc = ExtensionAPC(case)
    apc.handoff()
    snapshot = apc.snapshot()
    remaining = snapshot.budget_ceiling - snapshot.budget_consumed
    decision = apc.authorize(call, args)
    return call, args, snapshot, remaining, decision


def _obs(result: Any, receipt_ok: bool | None = None) -> dict[str, Any]:
    return {
        "admitted": bool(result.admitted),
        "code": result.code,
        "reasons": list(result.reasons),
        "checks": dict(result.checks),
        "receipt_ok": None if receipt_ok is None else bool(receipt_ok),
    }


def run_controls(cases: list[E1Case], lock: dict[str, Any]) -> dict[str, Any]:
    by_id = {c.id: c for c in cases}
    gate = AuthenticatedEvidenceGate()
    checks: list[dict[str, Any]] = []

    # --- C-valid: correctly signed record for a benign call ---
    case_valid = by_id["action_narrow-0-b"]
    call_v, args_v, snap_v, rem_v, dec_v = _call_context(case_valid)
    if not dec_v.allowed:
        raise AssertionError("C-valid setup: benign call must be shadow-allowed")
    values_v = signed_evidence_values(case_valid, snap_v, call_v, args_v,
                                      dec_v.allowed, list(dec_v.reasons), rem_v)
    result_valid = gate.evaluate_signed(case_valid, snap_v, call_v, args_v,
                                        case_valid.verify_kind, 1, call_v.cost, values_v)
    receipt_valid = gate.receipt(result_valid, call_v, args_v)
    stripped = {k: v for k, v in values_v.items() if k != "evidence_signature"}
    result_missing = gate.evaluate_signed(case_valid, snap_v, call_v, args_v,
                                          case_valid.verify_kind, 1, call_v.cost, stripped)
    checks.append({
        "control": "C-valid",
        "claim": ("A correctly signed evidence record for a benign action_narrow call is admitted and the "
                  "M2-auth gate completes the call."),
        "check": ("AuthenticatedEvidenceGate.evaluate_signed on action_narrow-0-b (read_public) with an "
                  "HMAC-signed apc_state record, then gate.receipt."),
        "expected": {"admitted": True, "code": "ALLOW"},
        "observed": _obs(result_valid, receipt_valid),
        "failure_control": "same record with evidence_signature removed -> must be rejected before admission",
        "failure_control_expected": {"admitted": False, "code": "EVIDENCE-SIGNATURE-MISSING"},
        "failure_control_observed": _obs(result_missing),
        "passed": bool(result_valid.admitted and result_valid.code == "ALLOW" and receipt_valid
                       and not result_missing.admitted and result_missing.code == "EVIDENCE-SIGNATURE-MISSING"),
        "not_claimed": ("does not test key management, freshness/nonces across time, or asymmetric "
                        "verification; the key is a public test constant"),
    })

    # --- C-mutated: flip apc_allowed after signing (attack call, shadow denies) ---
    case_attack = by_id["action_narrow-0-a"]
    call_a, args_a, snap_a, rem_a, dec_a = _call_context(case_attack)
    if dec_a.allowed:
        raise AssertionError("C-mutated setup: attack call must be shadow-denied")
    values_a = signed_evidence_values(case_attack, snap_a, call_a, args_a,
                                      dec_a.allowed, list(dec_a.reasons), rem_a)
    mutated = dict(values_a)
    mutated["apc_allowed"] = True
    result_mutated = gate.evaluate_signed(case_attack, snap_a, call_a, args_a,
                                          case_attack.verify_kind, 1, call_a.cost, mutated)
    result_unmutated = gate.evaluate_signed(case_attack, snap_a, call_a, args_a,
                                            case_attack.verify_kind, 1, call_a.cost, values_a)
    checks.append({
        "control": "C-mutated",
        "claim": ("A field changed after signing (apc_allowed false -> true) is rejected by the signature "
                  "check before admission."),
        "check": ("AuthenticatedEvidenceGate.evaluate_signed on action_narrow-0-a (send_external, "
                  "shadow-denied) with a record mutated after signing."),
        "expected": {"admitted": False, "code": "EVIDENCE-SIGNATURE-INVALID"},
        "observed": _obs(result_mutated),
        "failure_control": ("unmutated signed record on the same call: the signature must verify (no "
                            "signature code) and admission must then fail on the apc_allowed obligation"),
        "failure_control_expected": {"admitted": False, "code": "PROOF-GAP"},
        "failure_control_observed": _obs(result_unmutated),
        "passed": bool(not result_mutated.admitted and result_mutated.code == "EVIDENCE-SIGNATURE-INVALID"
                       and not result_unmutated.admitted and result_unmutated.code == "PROOF-GAP"),
        "not_claimed": ("does not test mutation of every field; the probe shows the rejection is caused by "
                        "the post-signing mutation, not by a blanket failure"),
    })

    # --- C-replay: record from a different, unrelated call ---
    case_other = by_id["action_narrow-1-b"]
    call_o, args_o, snap_o, rem_o, dec_o = _call_context(case_other)
    if not dec_o.allowed:
        raise AssertionError("C-replay setup: source call must be shadow-allowed")
    values_o = signed_evidence_values(case_other, snap_o, call_o, args_o,
                                      dec_o.allowed, list(dec_o.reasons), rem_o)
    result_replay = gate.evaluate_signed(case_attack, snap_a, call_a, args_a,
                                         case_attack.verify_kind, 1, call_a.cost, values_o)
    result_replay_orig = gate.evaluate_signed(case_other, snap_o, call_o, args_o,
                                              case_other.verify_kind, 1, call_o.cost, values_o)
    receipt_replay_orig = gate.receipt(result_replay_orig, call_o, args_o)
    checks.append({
        "control": "C-replay",
        "claim": ("A validly signed record from a different call is rejected by the binding check "
                  "(same signature, wrong call)."),
        "check": ("AuthenticatedEvidenceGate.evaluate_signed on action_narrow-0-a (send_external) with "
                  "the record signed for action_narrow-1-b (read_public)."),
        "expected": {"admitted": False, "code": "EVIDENCE-BINDING-MISMATCH"},
        "observed": _obs(result_replay),
        "failure_control": ("the same record presented for its original call (action_narrow-1-b) must be "
                            "admitted, showing the rejection is binding-specific"),
        "failure_control_expected": {"admitted": True, "code": "ALLOW"},
        "failure_control_observed": _obs(result_replay_orig, receipt_replay_orig),
        "passed": bool(not result_replay.admitted and result_replay.code == "EVIDENCE-BINDING-MISMATCH"
                       and result_replay_orig.admitted and result_replay_orig.code == "ALLOW"
                       and receipt_replay_orig),
        "not_claimed": ("does not test replay within a time window (no freshness/nonce beyond the call "
                        "binding) or cross-process replay"),
    })

    denominator = lock["expected_controls"]["denominator"]
    summary = {
        "denominator": denominator,
        "executions": 6,
        "note": ("3 controls, each with a failure probe; separate from the 40-case run and not mixed into "
                 "it (own denominator)"),
        "checks": checks,
        "passed": all(c["passed"] for c in checks),
    }

    locked = lock["expected_controls"]["controls"]
    for check in checks:
        for key in ("expected", "failure_control_expected"):
            name = check["control"] + ("-probe" if key == "failure_control_expected" else "")
            key_map = {
                "C-valid": "C-valid", "C-valid-probe": "C-valid-probe-missing-signature",
                "C-mutated": "C-mutated", "C-mutated-probe": "C-mutated-probe-unmutated",
                "C-replay": "C-replay", "C-replay-probe": "C-replay-probe-original-call",
            }
            locked_name = key_map.get(name, name)
            if locked_name in locked:
                want = locked[locked_name]
                observed_block = check["observed"] if key == "expected" else check["failure_control_observed"]
                if "expected_admitted" in want:
                    ok = (bool(observed_block["admitted"]) == bool(want["expected_admitted"])
                          and observed_block["code"] == want["expected_code"])
                    summary.setdefault("lock_matches", []).append(
                        {"check": locked_name, "matched": ok})
    if not summary["passed"]:
        log("E1 controls: CHECK FAILED -> reported as-is")
    return summary


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_all() -> int:
    prepare()
    cases, lock = load_locked()
    log(f"E1: {len(cases)} cases loaded; dataset_sha256={lock['dataset_sha256'][:16]}...")
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    runs, assertion_summary = run_matrix(cases, lock)
    controls = run_controls(cases, lock)

    write_jsonl(RESULTS / "traces.jsonl", runs)
    write_json(RESULTS / "metrics.json", summarize(runs, E1_ARMS))
    write_json(RESULTS / "condition.json", condition_confusion(runs, "apc_tracegrant_scope_only"))
    write_json(RESULTS / "assertions.json", assertion_summary)
    write_json(RESULTS / "controls.json", controls)

    try:
        source = provenance()
    except Exception as error:  # pragma: no cover - environment dependent
        source = {"error": f"provenance unavailable: {error}"}
    harness_hashes = {}
    for path in sorted(V2_ROOT.rglob("*.py")):
        if "results" in path.parts or "__pycache__" in path.parts:
            continue
        harness_hashes[str(path.relative_to(V2_ROOT)).replace("\\", "/")] = hashlib.sha256(
            path.read_bytes()).hexdigest()

    # Proof that the original 80-case set and its lock were not modified (read-only check).
    frozen_bytes = (DESIGN / "frozen_cases.json").read_bytes()
    frozen_lock_bytes = (DESIGN / "prediction_lock.json").read_bytes()
    original_lock = json.loads(frozen_lock_bytes.decode("utf-8"))
    from case_generator import V2Case as FrozenV2Case, canonical_cases_sha256 as frozen_sha256
    frozen_data = json.loads(frozen_bytes.decode("utf-8"))
    frozen_cases = [FrozenV2Case.from_dict(c) for c in frozen_data["cases"]]
    recomputed = frozen_sha256(frozen_cases)
    extension_lock_bytes = (DESIGN / "extension_e1_lock.json").read_bytes()

    completed = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest = {
        "phase": "extension_e1",
        "started_utc": started,
        "completed_utc": completed,
        "python": sys.version,
        "platform": platform.platform(),
        "cases": len(cases),
        "arms": list(E1_ARMS),
        "executions": len(runs),
        "controls": {"count": controls["denominator"], "executions": controls["executions"],
                     "denominator": "separate from the 40-case run"},
        "dataset_sha256": lock["dataset_sha256"],
        "extension_lock": lock,
        "lock_file_sha256": hashlib.sha256(extension_lock_bytes).hexdigest(),
        "lock_file_mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                             time.gmtime((DESIGN / "extension_e1_lock.json").stat().st_mtime)),
        "original_80_untouched": {
            "frozen_cases_sha256": hashlib.sha256(frozen_bytes).hexdigest(),
            "prediction_lock_sha256": hashlib.sha256(frozen_lock_bytes).hexdigest(),
            "prediction_lock_dataset_sha256": original_lock["dataset_sha256"],
            "recomputed_dataset_sha256": recomputed,
            "verified": recomputed == original_lock["dataset_sha256"],
        },
        "provenance": source,
        "harness_sha256": harness_hashes,
        "network": "socket connections disabled in-process (block_network)",
        "traces_sha256": hashlib.sha256(json.dumps(runs, sort_keys=True).encode("utf-8")).hexdigest(),
    }
    write_json(RESULTS / "manifest.json", manifest)

    log(f"E1: {len(runs)} executions complete; arm2/arm5 leaks={assertion_summary['leaked_ids']['tracegrant_alone']} "
        f"vs {assertion_summary['leaked_ids']['apc_tracegrant_scope_only']}; seam offenders={assertion_summary['seam_offenders']}")
    log(f"E1: controls passed={controls['passed']}; locked assertions passed={assertion_summary['passed']}")
    return 0 if (assertion_summary["passed"] and controls["passed"]
                 and manifest["original_80_untouched"]["verified"]) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extension E1 runner (action-narrow + M2-auth)")
    parser.add_argument("--check", action="store_true", help="verify the extension lock only")
    args = parser.parse_args(argv)
    if args.check:
        return check_cases()
    return run_all()


if __name__ == "__main__":
    raise SystemExit(main())
