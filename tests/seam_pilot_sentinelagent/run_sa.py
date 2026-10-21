"""Third seam pilot runner: APC -> SentinelAgent (96 cases x 7 arms).

Strictly sequential: one arm at a time, no concurrency. Phases:
  1. lock check (dataset hash, frozen-set proof)
  2. controls S1 (freshness) / S2 (signature) / S3 (attestation)
  3. full matrix: 96 cases x 7 arms = 672 executions
  4. metrics: per-arm, per-template, expected-vs-observed, seam test
  5. adversarial self-review (determinism re-run, hash re-checks, leak-audit)
  6. manifest with the lock hash embedded
Writes artifacts under results/sa/. Does not modify seam_pilot_v2 or the
sentinelagent_audit_20261014 tree (read-only reuse; hashes recorded).

Usage:
    python run_sa.py            # run everything
    python run_sa.py --check    # verify existing artifacts against the lock
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

SA_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SA_ROOT / "adapters"))
sys.path.insert(0, str(SA_ROOT / "design"))

from sa_harness import (  # noqa: E402
    SA_ARMS,
    SA_NEW_ARMS,
    UPSTREAM_FILE,
    V2_ROOT,
    install_bridge_key,
    load_locked,
    run_case_sa,
    run_controls_sa,
)
from v2_common import prepare  # noqa: E402
from arms import run_case as run_case_v2  # noqa: E402

RESULTS = SA_ROOT / "results" / "sa"
PHASES = RESULTS / "phases.json"
CONTROLS = RESULTS / "controls.json"
RUNS = RESULTS / "runs.jsonl"
RAW_METRICS = RESULTS / "raw_metrics.json"
METRICS = RESULTS / "metrics.json"
SELF_REVIEW = RESULTS / "self_review.json"
MANIFEST = RESULTS / "manifest.json"

V2_DESIGN = V2_ROOT / "design"
V2_RESULTS = V2_ROOT / "results"
TIMING_KEYS = {"authorization_ns", "envelope_id"}


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
    arms = defaultdict(list)
    for row in rows:
        arms[row["arm"]].append(row)
    for arm in SA_ARMS:
        arm_rows = arms.get(arm, [])
        attack_rows = [r for r in arm_rows if r["case"]["kind"] == "attack"]
        benign_rows = [r for r in arm_rows if r["case"]["kind"] == "benign"]
        attack_success_cases = [r["case"]["id"] for r in attack_rows
                                if any(e.get("unauthorized_effect") for e in r["events"])]
        benign_fd_cases = [r["case"]["id"] for r in benign_rows
                           if any(e.get("false_denial") for e in r["events"])]
        unauthorized_events = sum(1 for r in arm_rows for e in r["events"] if e.get("unauthorized_effect"))
        fd_events = sum(1 for r in arm_rows for e in r["events"] if e.get("false_denial"))
        confidential_external = sum(
            1 for r in arm_rows for e in r["events"] for eff in e.get("effects", [])
            if eff.get("type") == "external_send" and eff.get("contains_confidential_marker"))
        evaluated = sum(1 for r in arm_rows for e in r["events"] if "token" in e or "gate" in e)
        token_events = sum(1 for r in arm_rows for e in r["events"] if e.get("token", {}).get("presented"))
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
                "runs": 0, "attacks": 0, "benign": 0, "leaked": 0, "false_denials": 0, "unauthorized_events": 0,
            })
            block["runs"] += 1
            block["attacks" if r["case"]["kind"] == "attack" else "benign"] += 1
            leaked = any(e.get("unauthorized_effect") for e in r["events"])
            fd = any(e.get("false_denial") for e in r["events"])
            block["leaked"] += 1 if (r["case"]["kind"] == "attack" and leaked) else 0
            block["false_denials"] += 1 if fd else 0
            block["unauthorized_events"] += sum(1 for e in r["events"] if e.get("unauthorized_effect"))
        out[arm] = {
            "rows": len(arm_rows),
            "attack_cases": len(attack_rows),
            "attack_success_cases": attack_success_cases,
            "attack_successes": len(attack_success_cases),
            "benign_cases": len(benign_rows),
            "benign_false_denial_cases": benign_fd_cases,
            "benign_false_denial_count": len(benign_fd_cases),
            "unauthorized_effect_events": unauthorized_events,
            "false_denial_events": fd_events,
            "confidential_marker_external_effects": confidential_external,
            "evaluated_events": evaluated,
            "token_events": token_events,
            "signature_invalid_events": signature_invalid,
            "code_histogram": dict(sorted(codes.items())),
            "per_template": per_template,
        }
    return out


def compare_expected(metrics: dict[str, Any], lock: dict[str, Any],
                     cases_by_id: dict[str, Any]) -> dict[str, Any]:
    expected = lock["expected_per_arm"]
    comparison: dict[str, Any] = {"per_arm": {}, "leak_sets": {}, "seam_test": {}, "overall_ok": True}
    for arm in SA_ARMS:
        exp = expected[arm]
        obs = metrics[arm]
        checks = {
            "leak_cases": obs["attack_successes"] == exp["leak_cases"],
            "leak_events": obs["unauthorized_effect_events"] == exp["leak_events"],
            "benign_fd_cases": obs["benign_false_denial_count"] == exp["benign_fd_cases"],
            "fd_events": obs["false_denial_events"] == exp["fd_events"],
        }
        comparison["per_arm"][arm] = {
            "expected": exp,
            "observed": {
                "leak_cases": obs["attack_successes"],
                "leak_events": obs["unauthorized_effect_events"],
                "benign_fd_cases": obs["benign_false_denial_count"],
                "fd_events": obs["false_denial_events"],
            },
            "checks": checks,
            "ok": all(checks.values()),
        }
        comparison["overall_ok"] &= all(checks.values())

    exp_leaks = set(lock["expected_leak_cases_arms_2_and_5"])
    for arm in ("sentinelagent_alone", "apc_sentinelagent_scope_only"):
        obs_leaks = set(metrics[arm]["attack_success_cases"])
        comparison["leak_sets"][arm] = {
            "expected": sorted(exp_leaks),
            "observed": sorted(obs_leaks),
            "missing": sorted(exp_leaks - obs_leaks),
            "unexpected": sorted(obs_leaks - exp_leaks),
            "set_ok": exp_leaks == obs_leaks,
        }
        comparison["overall_ok"] &= exp_leaks == obs_leaks
    comparison["leak_sets"]["arm2_equals_arm5"] = (
        set(metrics["sentinelagent_alone"]["attack_success_cases"])
        == set(metrics["apc_sentinelagent_scope_only"]["attack_success_cases"]))

    # Seam test: arms 1 and 2 safe, any of 5/6/7 leaking.
    leak_sets = {arm: set(metrics[arm]["attack_success_cases"]) for arm in SA_ARMS}
    seam_cases = []
    for case_id, case in cases_by_id.items():
        if case.kind != "attack":
            continue
        if case_id in leak_sets["apc_alone"] or case_id in leak_sets["sentinelagent_alone"]:
            continue
        if any(case_id in leak_sets[a] for a in ("apc_sentinelagent_scope_only",
                                                 "apc_sentinelagent_retained",
                                                 "apc_sentinelagent_fail_closed")):
            seam_cases.append(case_id)
    comparison["seam_test"] = {
        "cases": sorted(seam_cases),
        "count": len(seam_cases),
        "expected_count": lock["expected_seam_test_cases"],
        "ok": len(seam_cases) == lock["expected_seam_test_cases"],
    }
    comparison["overall_ok"] &= len(seam_cases) == lock["expected_seam_test_cases"]

    # Confusion matrix for arm 5 against the locked predictions.
    arm5 = leak_sets["apc_sentinelagent_scope_only"]
    tp = fp = fn = tn = 0
    fp_cases: list[str] = []
    fn_cases: list[str] = []
    for case_id, case in cases_by_id.items():
        if case.kind != "attack":
            continue
        predicted_unsafe = not case.predicted_safe
        leaked = case_id in arm5
        if predicted_unsafe and leaked:
            tp += 1
        elif predicted_unsafe and not leaked:
            fp += 1
            fp_cases.append(case_id)
        elif (not predicted_unsafe) and leaked:
            fn += 1
            fn_cases.append(case_id)
        else:
            tn += 1
    expected_conf = lock["expected_arm5_confusion"]
    observed_conf = {"true_positive": tp, "false_positive": fp, "false_negative": fn, "true_negative": tn}
    comparison["arm5_confusion"] = {
        "expected": expected_conf,
        "observed": observed_conf,
        "false_positive_cases": sorted(fp_cases),
        "false_negative_cases": sorted(fn_cases),
        "ok": (tp == expected_conf["true_positive"] and fp == expected_conf["false_positive"]
               and fn == expected_conf["false_negative"] and tn == expected_conf["true_negative"]),
    }
    comparison["overall_ok"] &= comparison["arm5_confusion"]["ok"]

    # Same-mechanism control consistency against the frozen run (shared 80 cases).
    frozen_ref = json.loads((V2_RESULTS / "raw_metrics.json").read_text(encoding="utf-8"))
    shared_ids = {c_id for c_id, c in cases_by_id.items() if c_id in _frozen_ids()}
    shared_comp: dict[str, Any] = {}
    for arm in ("apc_alone", "apc_apc_preserved", "apc_apc_reset"):
        if arm not in frozen_ref:
            continue
        shared_rows = [r for r in load_rows() if r["arm"] == arm and r["case"]["id"] in shared_ids]
        leaked = sum(1 for r in shared_rows if r["case"]["kind"] == "attack"
                     and any(e.get("unauthorized_effect") for e in r["events"]))
        fd = sum(1 for r in shared_rows if r["case"]["kind"] == "benign"
                 and any(e.get("false_denial") for e in r["events"]))
        ref = frozen_ref[arm]
        shared_comp[arm] = {
            "frozen_reference": {"attack_successes": ref["attack_successes"],
                                 "benign_false_denial_cases": ref["benign_false_denial_cases"]},
            "observed_on_shared_80": {"attack_successes": leaked, "benign_false_denial_cases": fd},
            "ok": leaked == ref["attack_successes"] and fd == ref["benign_false_denial_cases"],
        }
        comparison["overall_ok"] &= shared_comp[arm]["ok"]
    comparison["frozen_reference_consistency"] = shared_comp
    return comparison


_FROZEN_IDS_CACHE: set[str] | None = None


def _frozen_ids() -> set[str]:
    global _FROZEN_IDS_CACHE
    if _FROZEN_IDS_CACHE is None:
        from v2_common import load_frozen_cases

        cases, _lock = load_frozen_cases()
        _FROZEN_IDS_CACHE = {c.id for c in cases}
    return _FROZEN_IDS_CACHE


# ---------------------------------------------------------------------------
# Self-review (phase 5.5 equivalent)
# ---------------------------------------------------------------------------

def self_review(cases: list[Any], lock: dict[str, Any], rows: list[dict[str, Any]],
                metrics: dict[str, Any], controls: dict[str, Any],
                hashes_before: dict[str, str], upstream_proof: dict[str, Any]) -> dict[str, Any]:
    cases_by_id = {c.id: c for c in cases}
    review: dict[str, Any] = {"checks": [], "ok": True}

    def check(name: str, ok: bool, detail: Any = None) -> None:
        review["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
        review["ok"] &= bool(ok)

    # 1. Controls passed inside this process.
    check("controls_passed", controls["ok"], {"records": len(controls["records"])})

    # 2. Hash re-checks: nothing in the reused trees changed during the run.
    for rel, before in hashes_before.items():
        after = sha256_file(Path(rel))
        check(f"hash_unchanged:{Path(rel).name}", after == before, {"sha256": after})

    # 3. Determinism: re-run a fixed sample (10 cases x arms 2,5) and compare
    #    event-by-event with timing fields stripped.
    sample = sorted(cases_by_id)[:10]
    mismatches = []
    for case_id in sample:
        case = cases_by_id[case_id]
        for arm in ("sentinelagent_alone", "apc_sentinelagent_scope_only"):
            fresh = run_case_sa(case, arm)
            old = next(r for r in rows if r["case"]["id"] == case_id and r["arm"] == arm)
            if strip_timing(fresh) != strip_timing(old):
                mismatches.append(f"{case_id}/{arm}")
    check("determinism_rerun", not mismatches, {"sample": len(sample) * 2, "mismatches": mismatches})
    review["reruns"] = len(sample) * 2

    # 4. Leak audit: every leaked event has real effects and oracle reasons; no
    #    unauthorized_effect is claimed without effects.
    audit_problems = []
    for row in rows:
        for event in row["events"]:
            if event.get("unauthorized_effect"):
                if not event.get("effects") or not event.get("oracle_reasons"):
                    audit_problems.append(f"{row['case']['id']}/{row['arm']}/idx{event.get('index')}")
    check("leak_audit", not audit_problems, {"problems": audit_problems})

    # 5. Arm 2 and arm 5 leak sets (the pair's standalone gap) are identical.
    a2 = set(metrics["sentinelagent_alone"]["attack_success_cases"])
    a5 = set(metrics["apc_sentinelagent_scope_only"]["attack_success_cases"])
    check("arm2_arm5_identical_leak_sets", a2 == a5, {"symmetric_difference": sorted(a2 ^ a5)})

    # 6. Not vacuous: the matrix contains both admissions and native denials.
    admissions = sum(1 for r in rows for e in r["events"] if e.get("allowed"))
    denials = sum(1 for r in rows for e in r["events"]
                  if "token" in e and not e.get("allowed"))
    check("not_vacuous", admissions > 0 and denials > 0, {"admissions": admissions, "token_denials": denials})

    # 7. Arm snapshots have the right sources.
    sources_ok = True
    for row in rows:
        snap = (row.get("handoff") or {}).get("snapshot") or {}
        source = snap.get("source")
        if row["arm"] == "sentinelagent_alone" and source != "case-root":
            sources_ok = False
        if row["arm"] in ("apc_sentinelagent_scope_only", "apc_sentinelagent_retained",
                          "apc_sentinelagent_fail_closed") and source not in ("apc-post-handoff", None):
            sources_ok = False
    check("snapshot_sources", sources_ok, None)
    return review


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_all() -> int:
    prepare()
    RESULTS.mkdir(parents=True, exist_ok=True)
    cases, lock = load_locked()
    cases_by_id = {c.id: c for c in cases}
    started = utc_now()

    hashes_before = {
        str(UPSTREAM_FILE): sha256_file(UPSTREAM_FILE),
        str(V2_DESIGN / "frozen_cases.json"): sha256_file(V2_DESIGN / "frozen_cases.json"),
        str(V2_DESIGN / "prediction_lock.json"): sha256_file(V2_DESIGN / "prediction_lock.json"),
        str(V2_ROOT / "results" / "raw_metrics.json"): sha256_file(V2_ROOT / "results" / "raw_metrics.json"),
        str(SA_ROOT / "design" / "sa_cases.json"): sha256_file(SA_ROOT / "design" / "sa_cases.json"),
        str(SA_ROOT / "design" / "sa_lock.json"): sha256_file(SA_ROOT / "design" / "sa_lock.json"),
        str(SA_ROOT / "design" / "call_to_token_mapping.md"): sha256_file(SA_ROOT / "design" / "call_to_token_mapping.md"),
        str(SA_ROOT / "design" / "composition_condition_sentinelagent.md"): sha256_file(SA_ROOT / "design" / "composition_condition_sentinelagent.md"),
        str(SA_ROOT / "design" / "sa_case_generator.py"): sha256_file(SA_ROOT / "design" / "sa_case_generator.py"),
        str(SA_ROOT / "adapters" / "sa_harness.py"): sha256_file(SA_ROOT / "adapters" / "sa_harness.py"),
    }

    # Phase 1: the lock is already verified by load_locked(); record its proof.
    phases = {
        "phase1_lock_check": {
            "utc": utc_now(),
            "dataset_sha256": lock["dataset_sha256"],
            "case_count": lock["case_count"],
            "locked_utc": lock["locked_utc"],
            "expected_confusion": lock["expected_arm5_confusion"],
            "note": "dataset re-hashed at load; mismatch would have raised",
        },
        "started_utc": started,
    }

    # Phase 2: controls (with the bridge key installed first).
    upstream_proof = install_bridge_key()
    controls = run_controls_sa()
    write_json(CONTROLS, controls)
    phases["phase2_controls"] = {"utc": utc_now(), "ok": controls["ok"],
                                 "records": [r["id"] for r in controls["records"]]}
    print(f"phase 2 controls: ok={controls['ok']} ({len(controls['records'])} records)")

    # Phase 3: the matrix, strictly sequential (one arm at a time).
    rows: list[dict[str, Any]] = []
    per_arm_rows: Counter[str] = Counter()
    for arm in SA_ARMS:
        arm_start = time.perf_counter_ns()
        for case in cases:
            if arm in SA_NEW_ARMS:
                rows.append(run_case_sa(case, arm))
            else:
                rows.append(run_case_v2(case, arm))
            per_arm_rows[arm] += 1
        elapsed_ms = (time.perf_counter_ns() - arm_start) / 1e6
        print(f"phase 3 arm {arm}: {per_arm_rows[arm]} rows ({elapsed_ms:.0f} ms)")
    write_jsonl(RUNS, rows)
    phases["phase3_matrix"] = {"utc": utc_now(), "executions": len(rows),
                               "rows_per_arm": dict(per_arm_rows)}
    assert len(rows) == 96 * 7

    # Phase 4: metrics.
    metrics = compute_metrics(rows)
    write_json(RAW_METRICS, metrics)
    comparison = compare_expected(metrics, lock, cases_by_id)
    write_json(METRICS, {"metrics": metrics, "comparison": comparison})
    phases["phase4_metrics"] = {"utc": utc_now(), "expected_ok": comparison["overall_ok"],
                                "seam_test": comparison["seam_test"],
                                "arm5_confusion": comparison["arm5_confusion"]["observed"]}
    print(f"phase 4 metrics: expected_ok={comparison['overall_ok']} "
          f"seam={comparison['seam_test']['count']}")

    # Phase 5: adversarial self-review.
    review = self_review(cases, lock, rows, metrics, controls, hashes_before, upstream_proof)
    write_json(SELF_REVIEW, review)
    phases["phase5_self_review"] = {"utc": utc_now(), "ok": review["ok"],
                                    "failed": [c["check"] for c in review["checks"] if not c["ok"]]}
    print(f"phase 5 self-review: ok={review['ok']}")

    # Phase 6: manifest with the lock proof embedded.
    manifest = {
        "run": {
            "pair": "apc->sentinelagent",
            "started_utc": started,
            "ended_utc": utc_now(),
            "executions": len(rows),
            "cases": len(cases),
            "arms": list(SA_ARMS),
            "argv": sys.argv[1:],
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "sequential": "one arm at a time; no concurrency; no network (prepare() blocks it)",
            "paid_llm_calls": 0,
        },
        "lock": {
            "sa_lock_path": str(SA_ROOT / "design" / "sa_lock.json"),
            "sa_lock_sha256": hashes_before[str(SA_ROOT / "design" / "sa_lock.json")],
            "sa_cases_sha256": hashes_before[str(SA_ROOT / "design" / "sa_cases.json")],
            "dataset_sha256": lock["dataset_sha256"],
            "locked_utc": lock["locked_utc"],
            "case_count": lock["case_count"],
            "prediction_source": lock["prediction_source"],
            "note": "predictions and cases were locked before the run; hashes above are the proof",
        },
        "key_model": upstream_proof,
        "controls": {"ok": controls["ok"], "records": controls["records"]},
        "self_review": {"ok": review["ok"], "checks": review["checks"],
                        "reruns": review.get("reruns", 0)},
        "expected_vs_observed_ok": comparison["overall_ok"],
        "file_hashes": {str(Path(k)): v for k, v in hashes_before.items()},
        "frozen_proof": {
            "frozen_cases_sha256": hashes_before[str(V2_DESIGN / "frozen_cases.json")],
            "prediction_lock_sha256": hashes_before[str(V2_DESIGN / "prediction_lock.json")],
        },
    }
    write_json(MANIFEST, manifest)
    phases["phase6_manifest"] = {"utc": utc_now(), "manifest": str(MANIFEST)}
    write_json(PHASES, phases)
    print(f"phase 6 manifest written: {MANIFEST}")
    return 0 if (controls["ok"] and review["ok"]) else 1


def check_all() -> int:
    cases, lock = load_locked()
    ok = True
    rows = load_rows()
    expected_rows = 96 * 7
    ok &= len(rows) == expected_rows
    print(f"rows={len(rows)} expected={expected_rows}")
    arms = Counter(r["arm"] for r in rows)
    ok &= all(arms[a] == 96 for a in SA_ARMS)
    print(f"rows per arm: {dict(arms)}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok &= manifest["lock"]["dataset_sha256"] == lock["dataset_sha256"]
    print(f"manifest lock dataset: {manifest['lock']['dataset_sha256']}")
    upstream = sha256_file(UPSTREAM_FILE)
    ok &= upstream == manifest["key_model"]["upstream_sha256"]
    print(f"upstream sha256 match: {upstream == manifest['key_model']['upstream_sha256']}")
    frozen_lock_now = sha256_file(V2_DESIGN / "prediction_lock.json")
    ok &= frozen_lock_now == manifest["frozen_proof"]["prediction_lock_sha256"]
    print(f"frozen lock hash match: {frozen_lock_now == manifest['frozen_proof']['prediction_lock_sha256']}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="APC -> SentinelAgent seam pilot runner")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        return check_all()
    return run_all()


if __name__ == "__main__":
    raise SystemExit(main())
