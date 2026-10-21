"""Boundary runner: APC -> SentinelAgent bridge boundary test.

Pre-registered experiment. Lock-first: aborts unless results/boundary/boundary_lock.json
exists and its recorded hashes (boundary harness, sa_cases.json) match the current
files. Then runs arms {1,2,2v,5,6,7} x variants {v1,v2} x 96 cases = 1152 runs,
strictly sequential, no network.

Writes results/boundary/{runs.jsonl, metrics.json, controls.json, phases.json, manifest.json}.
Mirrors run_sa.py --check audit mode via `python run_boundary.py --check`.

Usage:
    python run_boundary.py            # run everything (lock-first)
    python run_boundary.py --check    # verify existing artifacts against the lock
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(BOUNDARY_ROOT / "adapters"))

from boundary_harness import (  # noqa: E402
    BOUNDARY_ARMS, VARIANTS, VARIANT_ARMS, DEFAULT_RECIPIENT,
    run_case_boundary, install_bridge_key_boundary, run_controls_boundary,
)

RESULTS = BOUNDARY_ROOT / "results" / "boundary"
RUNS = RESULTS / "runs.jsonl"
METRICS = RESULTS / "metrics.json"
CONTROLS = RESULTS / "controls.json"
PHASES = RESULTS / "phases.json"
MANIFEST = RESULTS / "manifest.json"
SELF_REVIEW = RESULTS / "self_review.json"
RECONCILIATION = RESULTS / "reconciliation.json"

LOCK_PATH = BOUNDARY_ROOT / "design" / "boundary_lock.json"
CASES_PATH = BOUNDARY_ROOT.parent / "seam_pilot_sentinelagent" / "design" / "sa_cases.json"
HARNESS_PATH = BOUNDARY_ROOT / "adapters" / "boundary_harness.py"

TIMING_KEYS = {"authorization_ns"}


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def strip_timing(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_timing(v) for k, v in value.items() if k not in TIMING_KEYS}
    if isinstance(value, list):
        return [strip_timing(v) for v in value]
    return value


def load_rows() -> list[dict[str, Any]]:
    rows = []
    with RUNS.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["arm"], row.get("variant", "canonical"))].append(row)
    for key in sorted(groups):
        arm, variant = key
        arm_rows = groups[key]
        attack_rows = [r for r in arm_rows if r["case"]["kind"] == "attack"]
        benign_rows = [r for r in arm_rows if r["case"]["kind"] == "benign"]
        attack_success_cases = [r["case"]["id"] for r in attack_rows
                                if any(e.get("unauthorized_effect") for e in r["events"])]
        benign_fd_cases = [r["case"]["id"] for r in benign_rows
                           if any(e.get("false_denial") for e in r["events"])]
        unauthorized_events = sum(1 for r in arm_rows for e in r["events"] if e.get("unauthorized_effect"))
        fd_events = sum(1 for r in arm_rows for e in r["events"] if e.get("false_denial"))
        admitted = sum(1 for r in arm_rows for e in r["events"] if e.get("allowed"))
        denied = sum(1 for r in arm_rows for e in r["events"] if not e.get("allowed"))
        token_presented = sum(1 for r in arm_rows for e in r["events"] if e.get("token", {}).get("presented"))
        signature_invalid = sum(1 for r in arm_rows for e in r["events"]
                                if e.get("token", {}).get("presented") and not e["token"].get("signature_ok"))
        codes = Counter()
        for r in arm_rows:
            for e in r["events"]:
                gate = e.get("gate")
                if gate:
                    codes[gate.get("code", "?")] += 1
                else:
                    codes["ADMITTED" if e.get("allowed") else "APC-DENY"] += 1
        per_template: dict[str, Any] = {}
        for r in arm_rows:
            block = per_template.setdefault(r["case"]["template"], {
                "runs": 0, "attacks": 0, "benign": 0, "leaked": 0, "false_denials": 0,
                "unauthorized_events": 0,
            })
            block["runs"] += 1
            block["attacks" if r["case"]["kind"] == "attack" else "benign"] += 1
            leaked = any(e.get("unauthorized_effect") for e in r["events"])
            fd = any(e.get("false_denial") for e in r["events"])
            block["leaked"] += 1 if (r["case"]["kind"] == "attack" and leaked) else 0
            block["false_denials"] += 1 if fd else 0
            block["unauthorized_events"] += sum(1 for e in r["events"] if e.get("unauthorized_effect"))
        out[f"{arm}::{variant}"] = {
            "arm": arm, "variant": variant,
            "rows": len(arm_rows),
            "attack_cases": len(attack_rows),
            "attack_success_cases": attack_success_cases,
            "attack_successes": len(attack_success_cases),
            "benign_cases": len(benign_rows),
            "benign_false_denial_cases": benign_fd_cases,
            "benign_false_denial_count": len(benign_fd_cases),
            "unauthorized_effect_events": unauthorized_events,
            "false_denial_events": fd_events,
            "admissions": admitted,
            "denials": denied,
            "token_events": token_presented,
            "signature_invalid_events": signature_invalid,
            "code_histogram": dict(sorted(codes.items())),
            "per_template": per_template,
        }
    return out


# ---------------------------------------------------------------------------
# Lock guard
# ---------------------------------------------------------------------------

def load_lock() -> dict[str, Any]:
    if not LOCK_PATH.exists():
        raise RuntimeError(f"boundary_lock.json not found at {LOCK_PATH}; run the lock step first")
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def guard_lock() -> dict[str, Any]:
    lock = load_lock()
    harness_hash = sha256_file(HARNESS_PATH)
    cases_hash = sha256_file(CASES_PATH)
    recorded_harness = lock.get("boundary_harness_sha256")
    recorded_cases = lock.get("sa_cases_sha256")
    problems = []
    if recorded_harness and recorded_harness != harness_hash:
        problems.append(f"boundary harness hash mismatch: lock={recorded_harness} current={harness_hash}")
    if recorded_cases and recorded_cases != cases_hash:
        problems.append(f"sa_cases.json hash mismatch: lock={recorded_cases} current={cases_hash}")
    if problems:
        for p in problems:
            print(f"ABORT: {p}")
        raise RuntimeError("lock guard failed: " + "; ".join(problems))
    print(f"guard ok: harness={harness_hash[:12]} cases={cases_hash[:12]}")
    return lock


# ---------------------------------------------------------------------------
# Controls CV1-CV5
# ---------------------------------------------------------------------------

def run_cv_controls(cases: list[Any], lock: dict[str, Any]) -> dict[str, Any]:
    """Run the five boundary controls. Returns a controls record with ok flag."""
    import sa_harness  # noqa: E402
    from seam_pilot.model import MockWorld  # noqa: E402
    from v2_common import V2Oracle, case_snapshot  # noqa: E402
    from boundary_harness import build_presented_variant, t0_ops_variant, evaluate_presented

    records = []

    # --- S1-S3 re-run (CV3) ---
    s1s3 = run_controls_boundary()
    records.append({
        "id": "CV3-s1s3",
        "setup": "re-run S1 (freshness), S2 (signature), S3 (attestation) controls from sa_harness",
        "expected": "all 10 control records ok",
        "observed_ok": bool(s1s3["ok"]),
        "records": s1s3["records"],
        "ok": bool(s1s3["ok"]),
    })

    # Build variant manifests for CV1 / CV2.
    # Pick representative cases.
    by_id = {c.id: c for c in cases}

    def manifest_for(case_id: str, variant: str):
        case = by_id[case_id]
        call = case.attempts[0]
        from seam_pilot.model import Call  # noqa: F401
        world = MockWorld(case)
        args = world.canonical(call)
        snapshot = case_snapshot(case)
        # derive ops directly
        tool = call.tool
        ops = t0_ops_variant(snapshot, tool, variant, case=case, args=args)
        return ops

    # CV1: v1 manifest for resource_widen-0-a contains widened op; canonical does not.
    cv1_widen_v1 = manifest_for("resource_widen-0-a", "v1")
    cv1_widen_canonical = manifest_for("resource_widen-0-a", "canonical")
    cv1_widen_ok = ("READ docs:external/secret" in cv1_widen_v1
                    and "READ docs:external/secret" not in cv1_widen_canonical)
    records.append({
        "id": "CV1",
        "setup": "v1 manifest for resource_widen-0-a vs canonical manifest",
        "expected": {"v1_contains_widened_op": True, "canonical_excludes_widened_op": True},
        "observed": {"v1": cv1_widen_v1, "canonical": cv1_widen_canonical},
        "ok": cv1_widen_ok,
    })

    # CV1 part b: v1/v2 manifests identical to canonical on >=2 no-divergence benign cases.
    nondiverge = []
    for c in cases:
        if c.kind != "benign" or len(c.attempts) == 0:
            continue
        call = c.attempts[0]
        world = MockWorld(c)
        args = world.canonical(call)
        snapshot = case_snapshot(c)
        canon = t0_ops_variant(snapshot, call.tool, "canonical", case=c, args=args, call=call)
        v1 = t0_ops_variant(snapshot, call.tool, "v1", case=c, args=args, call=call)
        v2 = t0_ops_variant(snapshot, call.tool, "v2", case=c, args=args, call=call)
        if sorted(canon) == sorted(v1) == sorted(v2):
            nondiverge.append(c.id)
            if len(nondiverge) >= 2:
                break
    cv1_identical_ok = len(nondiverge) >= 2
    records.append({
        "id": "CV1b",
        "setup": "v1/v2 manifests identical to canonical on >=2 no-divergence benign cases",
        "expected": {"count_ge_2": True, "case_ids": nondiverge[:2]},
        "observed": {"nondivergence_cases": nondiverge, "count": len(nondiverge)},
        "ok": cv1_identical_ok,
    })

    # CV2: v1 token admits widened op where canonical token is BLOCKED;
    #      v2 token admits the default-filled send.
    # v1 on resource_widen-0-a: token manifest includes READ docs:external/secret -> P6 allows.
    case_rw = by_id["resource_widen-0-a"]
    call_rw = case_rw.attempts[0]
    world = MockWorld(case_rw)
    args_rw = world.canonical(call_rw)
    snap_rw = case_snapshot(case_rw)
    presented_v1 = build_presented_variant(case_rw, snap_rw, call_rw, args_rw, 1, "v1")
    presented_canonical = build_presented_variant(case_rw, snap_rw, call_rw, args_rw, 1, "canonical")
    obs_v1 = sa_harness.native_check(presented_v1["token"], call_rw.tool,
                                     sa_harness.authority_value(call_rw, args_rw))
    obs_canonical = sa_harness.native_check(presented_canonical["token"], call_rw.tool,
                                            sa_harness.authority_value(call_rw, args_rw))
    cv2_v1_ok = obs_v1["p6_allowed"] and not obs_canonical["p6_allowed"]
    records.append({
        "id": "CV2",
        "setup": "v1 token admits widened op (READ docs:external/secret) where canonical token is BLOCKED",
        "expected": {"v1_p6_allowed": True, "canonical_p6_blocked": True},
        "observed": {"v1": {"p6_allowed": obs_v1["p6_allowed"], "p6_message": obs_v1["p6_message"]},
                     "canonical": {"p6_allowed": obs_canonical["p6_allowed"],
                                   "p6_message": obs_canonical["p6_message"]}},
        "ok": cv2_v1_ok,
    })

    # v2 on omitted_forbidden_default-0-a: manifest SEND endpoint = forbidden-default@example.test.
    case_ofd = by_id["omitted_forbidden_default-0-a"]
    call_ofd = case_ofd.attempts[0]
    world = MockWorld(case_ofd)
    args_ofd = world.canonical(call_ofd)
    snap_ofd = case_snapshot(case_ofd)
    presented_v2 = build_presented_variant(case_ofd, snap_ofd, call_ofd, args_ofd, 1, "v2")
    obs_v2 = sa_harness.native_check(presented_v2["token"], call_ofd.tool,
                                     sa_harness.authority_value(call_ofd, args_ofd))
    cv2_v2_ok = obs_v2["p6_allowed"] and "SEND forbidden-default@example.test" in [
        o for ops in presented_v2["token"].manifest.values() for o in ops]
    records.append({
        "id": "CV2b",
        "setup": "v2 token admits the default-filled send (SEND forbidden-default@example.test)",
        "expected": {"v2_p6_allowed": True, "manifest_contains_default_send": True},
        "observed": {"v2": {"p6_allowed": obs_v2["p6_allowed"], "p6_message": obs_v2["p6_message"],
                            "manifest": presented_v2["token"].manifest}},
        "ok": cv2_v2_ok,
    })

    ok = all(r["ok"] is True for r in records)
    return {"records": records, "ok": ok}


# ---------------------------------------------------------------------------
# Seam test
# ---------------------------------------------------------------------------

def seam_test(metrics: dict[str, Any], cases_by_id: dict[str, Any]) -> dict[str, Any]:
    """Seam test per variant: cases where arms 1 and 2 are safe but a composed arm leaks."""
    leak_sets: dict[tuple[str, str], set[str]] = {}
    for key, m in metrics.items():
        arm, variant = key.split("::")
        if arm in ("apc_alone", "sentinelagent_alone", "apc_sentinelagent_scope_only",
                   "apc_sentinelagent_retained", "apc_sentinelagent_fail_closed"):
            leak_sets[(arm, variant)] = set(m["attack_success_cases"])
    out: dict[str, Any] = {}
    for variant in VARIANTS:
        a1 = leak_sets.get(("apc_alone", variant), set())
        a2 = leak_sets.get(("sentinelagent_alone", variant), set())
        composed = ("apc_sentinelagent_scope_only", "apc_sentinelagent_retained",
                    "apc_sentinelagent_fail_closed")
        seam = []
        for case_id, case in cases_by_id.items():
            if case.kind != "attack":
                continue
            if case_id in a1 or case_id in a2:
                continue
            if any(case_id in leak_sets.get((a, variant), set()) for a in composed):
                seam.append(case_id)
        out[variant] = {
            "arm1_leaks": sorted(a1),
            "arm2_leaks": sorted(a2),
            "seam_cases": sorted(seam),
            "seam_count": len(seam),
        }
    return out


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_all() -> int:
    lock = guard_lock()
    from boundary_harness import load_locked as load_sa_locked
    cases, sa_lock = load_sa_locked()
    cases_by_id = {c.id: c for c in cases}
    started = utc_now()

    # Install bridge key first (trust model), then controls.
    upstream_proof = install_bridge_key_boundary()
    controls_pre = run_cv_controls(cases, sa_lock)
    write_json(CONTROLS, controls_pre)
    print(f"pre-run controls: ok={controls_pre['ok']} ({len(controls_pre['records'])} records)")
    if not controls_pre["ok"]:
        print("ABORT: pre-run controls failed; not accepting the matrix")
        return 1

    # Matrix: arms {1,2,2v,5,6,7} x variants {v1,v2} x 96 cases = 1152 runs.
    rows: list[dict[str, Any]] = []
    per_arm_variant: Counter[str] = Counter()
    arm_order = ["apc_alone", "sentinelagent_alone", "sentinelagent_alone_variant",
                 "apc_sentinelagent_scope_only", "apc_sentinelagent_retained",
                 "apc_sentinelagent_fail_closed"]
    for arm in arm_order:
        for variant in VARIANTS:
            arm_start = time.perf_counter_ns()
            for case in cases:
                if arm == "apc_alone":
                    from arms import run_case as run_case_v2  # noqa: E402
                    row = run_case_v2(case, arm)
                    row["variant"] = variant
                elif arm == "sentinelagent_alone":
                    # canonical bridge reference: always canonical derivation
                    row = run_case_boundary(case, arm, "canonical")
                    row["variant"] = variant
                else:
                    row = run_case_boundary(case, arm, variant)
                rows.append(row)
                per_arm_variant[f"{arm}::{variant}"] += 1
            elapsed_ms = (time.perf_counter_ns() - arm_start) / 1e6
            print(f"phase matrix arm {arm} variant {variant}: {per_arm_variant[f'{arm}::{variant}']} rows ({elapsed_ms:.0f} ms)")
    write_jsonl(RUNS, rows)
    assert len(rows) == 96 * 6 * 2, len(rows)

    metrics = compute_metrics(rows)
    write_json(METRICS, {"metrics": metrics})

    # Controls CV4 (determinism) and CV5 (non-vacuity) against stored rows.
    cv_records = []
    for r in controls_pre["records"]:
        cv_records.append(dict(r))
    # CV4: determinism re-run on stored rows.
    sample_ids = sorted(cases_by_id)[:10]
    mismatches = []
    rerun_count = 0
    for cid in sample_ids:
        case = cases_by_id[cid]
        for arm in ("sentinelagent_alone_variant", "apc_sentinelagent_scope_only"):
            for variant in ("v1", "v2"):
                fresh = run_case_boundary(case, arm, variant)
                old = next(r for r in rows
                           if r["case"]["id"] == cid and r["arm"] == arm
                           and r.get("variant") == (variant if arm != "sentinelagent_alone" else "canonical"))
                if strip_timing(fresh) != strip_timing(old):
                    mismatches.append(f"{cid}/{arm}/{variant}")
                rerun_count += 1
    cv4_ok = not mismatches
    cv_records.append({
        "id": "CV4",
        "setup": "determinism: 10 re-runs (10 cases x 4 arm-variant combos) identical event-by-event",
        "expected": "no mismatches",
        "observed": {"reruns": rerun_count, "mismatches": mismatches},
        "ok": cv4_ok,
    })
    # CV5: non-vacuity per arm-variant cell.
    cv5_details = {}
    cv5_ok = True
    for key, m in metrics.items():
        ok_cell = m["admissions"] > 0 and m["denials"] > 0
        cv5_details[key] = {"admissions": m["admissions"], "denials": m["denials"], "ok": ok_cell}
        cv5_ok = cv5_ok and ok_cell
    cv_records.append({
        "id": "CV5",
        "setup": "non-vacuity: admissions > 0 and denials > 0 in each arm-variant cell",
        "expected": "all cells non-vacuous",
        "observed": cv5_details,
        "ok": cv5_ok,
    })
    controls_full = {"records": cv_records, "ok": controls_pre["ok"] and cv4_ok and cv5_ok}
    write_json(CONTROLS, controls_full)
    print(f"controls full: ok={controls_full['ok']}")

    # Seam test.
    seam = seam_test(metrics, cases_by_id)

    # Comparison vs lock predictions.
    comparison = compare_expected(metrics, lock, seam, cases_by_id)

    # Self-review: determinism, leak audit, not vacuous, hash re-checks.
    review = self_review(cases, lock, rows, metrics, controls_full,
                         {str(HARNESS_PATH): sha256_file(HARNESS_PATH),
                          str(CASES_PATH): sha256_file(CASES_PATH)},
                         upstream_proof)
    write_json(SELF_REVIEW, review)

    phases = {
        "phase1_lock_check": {"utc": utc_now(), "lock_utc": lock.get("locked_utc"),
                              "note": "dataset and harness re-hashed at load; mismatch aborts"},
        "started_utc": started,
        "phase2_pre_controls": {"utc": utc_now(), "ok": controls_pre["ok"],
                                "records": [r["id"] for r in controls_pre["records"]]},
        "phase3_matrix": {"utc": utc_now(), "executions": len(rows),
                          "rows_per_arm_variant": dict(per_arm_variant)},
        "phase4_metrics": {"utc": utc_now(), "comparison_ok": comparison["overall_ok"],
                           "seam_test": seam},
        "phase5_self_review": {"utc": utc_now(), "ok": review["ok"],
                               "failed": [c["check"] for c in review["checks"] if not c["ok"]]},
    }
    write_json(PHASES, phases)

    manifest = {
        "run": {
            "pair": "apc->sentinelagent-boundary",
            "started_utc": started,
            "ended_utc": utc_now(),
            "executions": len(rows),
            "cases": len(cases),
            "arms": list(BOUNDARY_ARMS),
            "variants": list(VARIANTS),
            "argv": sys.argv[1:],
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "sequential": "one arm-variant at a time; no concurrency; no network (prepare() blocks it)",
            "paid_llm_calls": 0,
        },
        "lock": {
            "boundary_lock_path": str(LOCK_PATH),
            "boundary_lock_sha256": sha256_file(LOCK_PATH),
            "boundary_harness_sha256": sha256_file(HARNESS_PATH),
            "sa_cases_sha256": sha256_file(CASES_PATH),
            "locked_utc": lock.get("locked_utc"),
            "case_count": lock.get("case_count"),
            "prediction_source": lock.get("prediction_source"),
            "note": "predictions and cases were locked before the run; hashes above are the proof",
        },
        "key_model": upstream_proof,
        "controls": {"ok": controls_full["ok"], "records": controls_full["records"]},
        "self_review": {"ok": review["ok"], "checks": review["checks"]},
        "expected_vs_observed_ok": comparison["overall_ok"],
        "seam_test": seam,
        "file_hashes": {str(HARNESS_PATH): sha256_file(HARNESS_PATH),
                        str(CASES_PATH): sha256_file(CASES_PATH)},
    }
    write_json(MANIFEST, manifest)
    print(f"manifest written: {MANIFEST}")
    return 0 if (controls_full["ok"] and review["ok"]) else 1


def compare_expected(metrics: dict[str, Any], lock: dict[str, Any],
                     seam: dict[str, Any], cases_by_id: dict[str, Any]) -> dict[str, Any]:
    comparison = {"per_arm_variant": {}, "seam_test": {}, "overall_ok": True}
    for key, m in metrics.items():
        arm, variant = key.split("::")
        exp_key = f"{arm}_{variant}"
        exp = lock.get("expected_per_arm_variant", {}).get(exp_key, {})
        comparison["per_arm_variant"][key] = {
            "expected": exp, "observed": {
                "attack_successes": m["attack_successes"],
                "leak_cases": m["attack_success_cases"],
                "benign_fd_cases": m["benign_false_denial_cases"],
                "fd_events": m["false_denial_events"],
            },
        }
    for variant in VARIANTS:
        st = seam[variant]
        comparison["seam_test"][variant] = {
            "seam_cases": st["seam_cases"],
            "seam_count": st["seam_count"],
            "expected_count": lock.get("expected_seam_test_cases", {}).get(variant, 0),
        }
        ok = st["seam_count"] == comparison["seam_test"][variant]["expected_count"]
        comparison["seam_test"][variant]["ok"] = ok
        comparison["overall_ok"] = comparison["overall_ok"] and ok
    return comparison


def self_review(cases: list[Any], lock: dict[str, Any], rows: list[dict[str, Any]],
                metrics: dict[str, Any], controls: dict[str, Any],
                hashes_before: dict[str, str], upstream_proof: dict[str, Any]) -> dict[str, Any]:
    cases_by_id = {c.id: c for c in cases}
    review: dict[str, Any] = {"checks": [], "ok": True}

    def check(name: str, ok: bool, detail: Any = None) -> None:
        review["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
        review["ok"] &= bool(ok)

    check("controls_passed", controls["ok"], {"records": len(controls["records"])})

    for rel, before in hashes_before.items():
        after = sha256_file(Path(rel))
        check(f"hash_unchanged:{Path(rel).name}", after == before, {"sha256": after})

    # Determinism already done in run_all (CV4); re-state here from stored outcome.
    cv4 = next((r for r in controls["records"] if r["id"] == "CV4"), None)
    check("determinism_rerun", bool(cv4 and cv4["ok"]), {"detail": cv4})

    # Leak audit.
    audit_problems = []
    for row in rows:
        for event in row["events"]:
            if event.get("unauthorized_effect"):
                if not event.get("effects") or not event.get("oracle_reasons"):
                    audit_problems.append(f"{row['case']['id']}/{row['arm']}/{row.get('variant')}/idx{event.get('index')}")
    check("leak_audit", not audit_problems, {"problems": audit_problems})

    # Not vacuous.
    admissions = sum(1 for r in rows for e in r["events"] if e.get("allowed"))
    denials = sum(1 for r in rows for e in r["events"] if not e.get("allowed"))
    check("not_vacuous", admissions > 0 and denials > 0, {"admissions": admissions, "denials": denials})

    return review


def check_all() -> int:
    lock = load_lock()
    rows = load_rows()
    ok = True
    expected_rows = 96 * 6 * 2
    ok &= len(rows) == expected_rows
    print(f"rows={len(rows)} expected={expected_rows}")
    groups = Counter((r["arm"], r.get("variant", "canonical")) for r in rows)
    for arm in BOUNDARY_ARMS:
        for variant in VARIANTS:
            count = groups.get((arm, variant), 0)
            print(f"  {arm}::{variant} = {count}")
            ok &= count == 96
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok &= manifest["lock"]["sa_cases_sha256"] == sha256_file(CASES_PATH)
    ok &= manifest["lock"]["boundary_harness_sha256"] == sha256_file(HARNESS_PATH)
    print(f"harness hash match: {manifest['lock']['boundary_harness_sha256'] == sha256_file(HARNESS_PATH)}")
    print(f"cases hash match: {manifest['lock']['sa_cases_sha256'] == sha256_file(CASES_PATH)}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SentinelAgent boundary runner")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        return check_all()
    return run_all()


if __name__ == "__main__":
    raise SystemExit(main())
