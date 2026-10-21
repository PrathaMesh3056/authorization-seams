"""Runner for the two discriminating tests (Extension E1 continuation).

Strictly sequential; no network; no paid calls; no git. Nothing under
`seam_pilot_v2` outside `discriminating_tests/` is modified or re-run; the
frozen 40-execution extension artifacts are read-only inputs.

Test 1  — scoring-only re-analysis of the frozen arm-2 (`tracegrant_alone`)
          records: the frozen oracle norm (`handoff_action_scope` against the
          handoff-derived authority) is re-scored against the authority arm 2's
          own world confers (`root_tools`). Gate decisions are frozen facts and
          are never re-evaluated; zero new executions.

Test 2  — the M0-A variant gate (`ActionScopeGate`, consumes
          `snapshot.actions`) runs the 8 frozen cases in arms {2, 5} (16 new
          executions, strictly sequential).

Usage:
    python run_discriminating.py     # lock verification + both tests + artifacts
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

DT_ROOT = Path(__file__).resolve().parent
V2_ROOT = DT_ROOT.parent
DESIGN = V2_ROOT / "design"
RESULTS = DT_ROOT / "results"
LOCK_PATH = DT_ROOT / "design" / "discriminating_lock.json"
FROZEN_TRACES = V2_ROOT / "results" / "extension_e1" / "traces.jsonl"

for _path in (str(V2_ROOT / "adapters"), str(V2_ROOT / "design"), str(DT_ROOT / "adapters")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from v2_common import MockWorld, case_snapshot, prepare  # noqa: E402
from seam_pilot.model import Call  # noqa: E402
from seam_pilot.native import provenance as native_provenance  # noqa: E402

from extension_e1_generator import E1Case, load_locked  # noqa: E402
from extension_e1 import E1Oracle, ExtensionAPC  # noqa: E402
from arms import _event  # noqa: E402
from metrics_v2 import case_false_denial, case_leaked, summarize  # noqa: E402
from variant_adapter import (  # noqa: E402
    ACTION_SCOPE_ABSENT_CODE,
    ACTION_SCOPE_CODE,
    ActionScopeGate,
    RootNormOracle,
    score_norms,
)

DT_ARMS: tuple[str, ...] = ("tracegrant_alone", "apc_tracegrant_scope_only")

CHECKED_BY = {
    "tracegrant_alone": ["TraceGrant-M0A"],
    "apc_tracegrant_scope_only": ["TraceGrant-M0A-scope-only"],
}

INTEGRITY_BASELINE = (
    "design/extension_e1_cases.json",
    "design/extension_e1_lock.json",
    "design/extension_e1_generator.py",
    "adapters/extension_e1.py",
    "run_extension_e1.py",
    "results/extension_e1/traces.jsonl",
    "results/extension_e1/manifest.json",
    "results/extension_e1/metrics.json",
    "results/extension_e1/assertions.json",
    "results/extension_e1/condition.json",
    "results/extension_e1/controls.json",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def canonical_traces_sha256(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode("utf-8")).hexdigest()


def integrity_snapshot() -> dict[str, dict[str, str]]:
    return {rel: {"sha256": sha256_file(V2_ROOT / rel)} for rel in INTEGRITY_BASELINE}


# ---------------------------------------------------------------------------
# Test 1 — scoring-only re-analysis of the frozen arm-2 records
# ---------------------------------------------------------------------------

def rerun_norm_decisions(case_obj: E1Case, event: dict[str, Any]) -> dict[str, Any]:
    call = Call(**event["proposed"])
    args = event["canonical_args"]
    norms = score_norms(case_obj, call, args, event["phase"])
    return {"call": call, "args": args, **norms}


def run_test1(cases: dict[str, E1Case], rows: list[dict[str, Any]], baseline: dict[str, Any]) -> dict[str, Any]:
    anchor_a1_failures: list[dict[str, Any]] = []
    anchor_a2_failures: list[dict[str, Any]] = []
    anchor_a3_failures: list[dict[str, Any]] = []

    for row in rows:
        cid = row["case"]["id"]
        case_obj = cases[cid]
        # Anchor A3: the row embeds the frozen case dict exactly.
        if json.dumps(row["case"], sort_keys=True) != json.dumps(case_obj.to_dict(), sort_keys=True):
            anchor_a3_failures.append(cid)
        # Anchor A1: a fresh handoff-norm oracle reproduces every frozen decision,
        # and anchor A2: the frozen unauthorized_effect flag recomputes from
        # frozen fields on every row (fresh oracle per row, no observe() first,
        # exactly mirroring the frozen runner's decision point).
        for event in row["events"]:
            recomputed = rerun_norm_decisions(case_obj, event)
            if recomputed["handoff_norm"] != list(event["oracle_reasons"]):
                anchor_a1_failures.append({"case": cid, "arm": row["arm"], "index": event["index"]})
            recomputed_leak = bool(event["oracle_reasons"]) and len(event["effects"]) > 0
            if recomputed_leak != bool(event["unauthorized_effect"]):
                anchor_a2_failures.append({"case": cid, "arm": row["arm"], "index": event["index"]})

    anchor_a4_failures = [c.id for c in cases.values()
                          if set(c.permitted_tools) != set(c.root_tools)]

    # Per-case re-scoring of arm-2 rows (leak status under both norms).
    rows_out: list[dict[str, Any]] = []
    arm2_leak_handoff: dict[str, bool] = {}
    arm2_leak_root: dict[str, bool] = {}
    for row in rows:
        if row["arm"] != "tracegrant_alone":
            continue
        cid = row["case"]["id"]
        case_obj = cases[cid]
        event = row["events"][0]
        recomputed = rerun_norm_decisions(case_obj, event)
        handoff_denies = bool(recomputed["handoff_norm"])
        root_denies = bool(recomputed["root_norm"])
        allowed = bool(event["allowed"])
        effects_executed = len(event["effects"]) > 0
        leak_handoff = allowed and effects_executed and handoff_denies
        leak_root = allowed and effects_executed and root_denies
        arm2_leak_handoff[cid] = leak_handoff
        arm2_leak_root[cid] = leak_root
        gate = event.get("gate") or {}
        rows_out.append({
            "case_id": cid,
            "kind": row["case"]["kind"],
            "attempted_call": f"{event['tool']}({json.dumps(event['canonical_args'])})",
            "frozen_gate_decision": {"allowed": allowed, "code": gate.get("code", "n/a"),
                                     "receipt_ok": event.get("receipt_ok"),
                                     "effects_executed": effects_executed},
            "handoff_norm": {"oracle_allows": not handoff_denies,
                             "reasons": recomputed["handoff_norm"],
                             "matches_frozen": recomputed["handoff_norm"] == list(event["oracle_reasons"]),
                             "leak": leak_handoff},
            "root_norm": {"oracle_allows": not root_denies,
                          "reasons": recomputed["root_norm"],
                          "leak": leak_root},
        })

    # Arm-1 and arm-5 states are frozen facts (re-anchored above via A2).
    arm1_leak = {r["case"]["id"]: any(e["unauthorized_effect"] for e in r["events"])
                 for r in rows if r["arm"] == "apc_alone"}
    arm5_leak = {r["case"]["id"]: any(e["unauthorized_effect"] for e in r["events"])
                 for r in rows if r["arm"] == "apc_tracegrant_scope_only"}
    all_ids = sorted(arm1_leak)

    seam_definition = ("cases where arm 1 safe AND arm 2 safe BUT arm 5 unsafe "
                       "(the frozen seam-test definition; arms 1/5 states are frozen facts)")
    canonical_offenders = sorted(
        cid for cid in all_ids
        if not arm1_leak[cid] and not arm2_leak_handoff[cid] and arm5_leak[cid])
    rootnorm_offenders = sorted(
        cid for cid in all_ids
        if not arm1_leak[cid] and not arm2_leak_root[cid] and arm5_leak[cid])

    attack_ids = [cid for cid in all_ids if cases[cid].kind == "attack"]
    benign_ids = [cid for cid in all_ids if cases[cid].kind == "benign"]
    counts = {
        "arm2_attack_leaks_handoff_norm": sum(arm2_leak_handoff[c] for c in attack_ids),
        "arm2_attack_leaks_root_norm": sum(arm2_leak_root[c] for c in attack_ids),
        "arm2_benign_leaks_handoff_norm": sum(arm2_leak_handoff[c] for c in benign_ids),
        "arm2_benign_leaks_root_norm": sum(arm2_leak_root[c] for c in benign_ids),
        "arm5_attack_leaks_frozen": sum(arm5_leak[c] for c in attack_ids),
        "arm1_attack_leaks_frozen": sum(arm1_leak[c] for c in attack_ids),
    }

    classification = ("composition-specific" if (counts["arm2_attack_leaks_root_norm"] == 0
                                                 and counts["arm5_attack_leaks_frozen"] == 4
                                                 and counts["arm1_attack_leaks_frozen"] == 0)
                      else "unchanged-standalone" if counts["arm2_attack_leaks_root_norm"] == 4
                      else "mixed")

    anchors = {
        "A1_handoff_norm_reproduces_all_frozen_rows": not anchor_a1_failures,
        "A1_failure_count": len(anchor_a1_failures),
        "A2_unauthorized_effect_recomputes_all_rows": not anchor_a2_failures,
        "A2_failure_count": len(anchor_a2_failures),
        "A3_row_case_dicts_equal_frozen_cases": not anchor_a3_failures,
        "A3_failure_count": len(anchor_a3_failures),
        "A4_permitted_tools_equal_root_tools_all_cases": not anchor_a4_failures,
        "A4_failure_cases": anchor_a4_failures,
    }

    return {
        "test": "discriminating_test_1_scoring_only",
        "nature": ("re-analysis of the frozen arm-2 (tracegrant_alone) records against the "
                   "arm-native root norm; recorded gate decisions are frozen facts, never "
                   "re-evaluated; zero new executions"),
        "written_utc": now_utc(),
        "frozen_inputs": {"traces_file_sha256": baseline["results/extension_e1/traces.jsonl"]["sha256"],
                          "traces_canonical_sha256": canonical_traces_sha256(rows),
                          "traces_rows": len(rows)},
        "norms": {
            "handoff_norm_frozen": ("a downstream call violates iff a base reference rule fails OR "
                                    "call.tool not in case.handoff_tools; reason handoff_action_scope "
                                    "(frozen E1Oracle.decide)"),
            "root_norm_variant": ("a downstream call violates iff a base reference rule fails OR "
                                  "call.tool not in case.root_tools; reason root_action_scope; every "
                                  "other reference rule unchanged"),
        },
        "field_source": ("root_tools / handoff_tools are the per-case fields of "
                         "design/extension_e1_cases.json; in this family permitted_tools == root_tools "
                         "on all 8 cases (checked: anchor A4)"),
        "rows": rows_out,
        "counts": counts,
        "seam_test": {"definition": seam_definition,
                      "under_canonical_scoring": {"count": len(canonical_offenders), "case_ids": canonical_offenders},
                      "under_root_norm_arm2_scoring": {"count": len(rootnorm_offenders), "case_ids": rootnorm_offenders}},
        "classification_under_arm_native_scoring": classification,
        "gate_level_deltas": {"count": 0,
                              "explanation": ("scoring-only re-analysis: no gate was re-evaluated; every "
                                              "recorded decision in results/extension_e1/ remains unchanged")},
        "anchors": anchors,
    }


# ---------------------------------------------------------------------------
# Test 2 — the M0-A variant (consumes snapshot.actions) in arms {2, 5}
# ---------------------------------------------------------------------------

def run_case_m0a(case: E1Case, arm: str) -> dict[str, Any]:
    if arm not in DT_ARMS:
        raise ValueError(arm)
    if case.prelude:
        raise ValueError("discriminating tests use no-prelude cases only")
    world = MockWorld(case)
    oracle = E1Oracle(case)  # frozen canonical convention, recorded for cell parity
    apc: ExtensionAPC | None = ExtensionAPC(case) if arm == "apc_tracegrant_scope_only" else None
    gate = ActionScopeGate()
    events: list[dict[str, Any]] = []
    handoff: dict[str, Any] = {}
    sequence = 0
    last_gate: dict[str, Any] | None = None

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
                                     [str(error)], CHECKED_BY[arm], [], 0))
                continue

            oracle_reasons = oracle.decide(call, args, phase)
            start = time.perf_counter_ns()
            if arm == "tracegrant_alone":
                snapshot = case_snapshot(case)
                gate_result = gate.evaluate(case, snapshot, call, args, "M0",
                                            case.verify_kind, sequence, call.cost, None)
                shadow = None
            else:
                assert apc is not None
                pre_snapshot = apc.snapshot()
                pre_remaining = pre_snapshot.budget_ceiling - pre_snapshot.budget_consumed
                shadow_decision = apc.authorize(call, args)
                gate_result = gate.evaluate(case, pre_snapshot, call, args, "M0",
                                            case.verify_kind, sequence, call.cost, None)
                shadow = {"allowed": shadow_decision.allowed, "reasons": list(shadow_decision.reasons),
                          "checked_by": list(shadow_decision.checked_by),
                          "pre_budget_remaining": pre_remaining}
            elapsed = time.perf_counter_ns() - start

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

    return {
        "case": case.to_dict(),
        "arm": arm,
        "extension": "E1-DT",
        "variant": "M0-A",
        "variant_gate": "ActionScopeGate",
        "mechanism": "TraceGrant",
        "mapping": "M0-A",
        "synthesized_mapping": "M0",
        "handoff": handoff,
        "events": events,
        "final_state": {"gate": last_gate},
        "oracle_state": {
            "spent": oracle.total_cost,
            "confidential_read": oracle.confidential_read,
            "external_send": oracle.external_send,
        },
    }


def frozen_arm2_lookups(rows: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    gates: dict[str, dict[str, Any]] = {}
    digests: dict[str, str] = {}
    for row in rows:
        if row["arm"] != "tracegrant_alone":
            continue
        event = row["events"][0]
        gate = event.get("gate") or {}
        gates[row["case"]["id"]] = gate
        digests[row["case"]["id"]] = str(gate.get("contract_digest"))
    return gates, digests


def run_test2(cases_by_id: dict[str, E1Case], case_order: list[E1Case],
              frozen_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for arm in DT_ARMS:
        for case in case_order:  # strictly sequential, one execution at a time
            runs.append(run_case_m0a(case, arm))
    if len(runs) != len(case_order) * len(DT_ARMS):
        raise AssertionError("mini-run matrix size mismatch")
    if any(not r["events"] for r in runs):
        raise AssertionError("a mini-run execution produced no events")

    by_arm = {arm: {r["case"]["id"]: r for r in runs if r["arm"] == arm} for arm in DT_ARMS}
    attack_ids = [c.id for c in case_order if c.kind == "attack"]
    benign_ids = [c.id for c in case_order if c.kind == "benign"]

    arm5 = by_arm["apc_tracegrant_scope_only"]
    arm2 = by_arm["tracegrant_alone"]
    frozen_gates, frozen_digests = frozen_arm2_lookups(frozen_rows)

    p21_observed = sorted(cid for cid in attack_ids
                          if not by_arm["apc_tracegrant_scope_only"][cid]["events"][0]["allowed"]
                          and (by_arm["apc_tracegrant_scope_only"][cid]["events"][0]["gate"] or {}).get("code") == ACTION_SCOPE_CODE)
    p21_codes = sorted({(by_arm["apc_tracegrant_scope_only"][cid]["events"][0]["gate"] or {}).get("code")
                        for cid in attack_ids})
    p22_observed = sorted(cid for cid in benign_ids
                          if by_arm["apc_tracegrant_scope_only"][cid]["events"][0]["allowed"])
    p22_false_denials = sorted(cid for cid in benign_ids if case_false_denial(arm5[cid]))
    allowed_rows = [e for r in runs for e in r["events"] if e["allowed"]]
    p23_receipts_ok = all(e["receipt_ok"] is True for e in allowed_rows)
    receipt_failures = sum(1 for r in runs for e in r["events"] if e.get("receipt_ok") is False)
    p24_parity_fails = []
    p24_leak_parity_fails: list[dict[str, Any]] = []
    for cid in sorted(arm2):
        variant_gate = arm2[cid]["events"][0]["gate"] or {}
        frozen_gate = frozen_gates.get(cid, {})
        if bool(variant_gate.get("admitted")) != bool(frozen_gate.get("admitted")) \
                or variant_gate.get("code") != frozen_gate.get("code"):
            p24_parity_fails.append({"case": cid, "variant": {"admitted": variant_gate.get("admitted"),
                                                             "code": variant_gate.get("code")},
                                     "frozen": {"admitted": frozen_gate.get("admitted"),
                                                "code": frozen_gate.get("code")}})
    variant_arm2_leaked = sorted(r["case"]["id"] for r in runs if r["arm"] == "tracegrant_alone" and case_leaked(r))
    frozen_arm2_leaked = sorted(row["case"]["id"] for row in frozen_rows
                                if row["arm"] == "tracegrant_alone"
                                and any(e["unauthorized_effect"] for e in row["events"]))
    if variant_arm2_leaked != frozen_arm2_leaked:
        p24_leak_parity_fails.append({"variant": variant_arm2_leaked, "frozen": frozen_arm2_leaked})
    p25_parity_fails = []
    for cid in sorted(arm2):
        variant_digest = (arm2[cid]["events"][0]["gate"] or {}).get("contract_digest")
        if variant_digest != frozen_digests.get(cid):
            p25_parity_fails.append({"case": cid, "variant": variant_digest, "frozen": frozen_digests.get(cid)})

    action_scope_denials: dict[str, int] = {}
    for r in runs:
        for e in r["events"]:
            code = (e.get("gate") or {}).get("code")
            if code in (ACTION_SCOPE_CODE, ACTION_SCOPE_ABSENT_CODE):
                action_scope_denials[code] = action_scope_denials.get(code, 0) + 1

    predictions = {
        "P2.1": {"predicted": ("arm 5 (M0-A): all 4 attack cases (action_narrow-0-a, -1-a, -2-a, -3-a) "
                               "denied with gate code ACTION-SCOPE (denied on action scope)"),
                 "observed": {"denied_attack_ids": p21_observed, "denied_codes_on_attacks": p21_codes,
                              "attack_count": len(attack_ids)},
                 "passed": bool(sorted(p21_observed) == sorted(attack_ids) and set(p21_codes) == {ACTION_SCOPE_CODE})},
        "P2.2": {"predicted": "arm 5 (M0-A): all 4 benign cases allowed (ALLOW); zero false denials",
                 "observed": {"allowed_benign_ids": p22_observed, "benign_false_denial_ids": p22_false_denials},
                 "passed": bool(sorted(p22_observed) == sorted(benign_ids) and not p22_false_denials)},
        "P2.3": {"predicted": ("every admitted call's receipt verifies and no receipt fails anywhere "
                               "in the run (12 allowed rows expected)"),
                 "observed": {"allowed_rows": len(allowed_rows), "all_receipts_ok": p23_receipts_ok,
                              "receipt_failures": receipt_failures},
                 "passed": bool(allowed_rows and p23_receipts_ok and receipt_failures == 0)},
        "P2.4": {"predicted": ("arm 2 (M0-A control) gate outcomes unchanged from canonical arm 2: "
                               "per-case (admitted, code) parity 8/8 against the frozen rows; leaked "
                               "set under the frozen oracle convention unchanged"),
                 "observed": {"gate_outcome_parity_failures": p24_parity_fails,
                              "variant_arm2_leaked_frozen_convention": variant_arm2_leaked,
                              "frozen_arm2_leaked": frozen_arm2_leaked},
                 "passed": bool(not p24_parity_fails and not p24_leak_parity_fails)},
        "P2.5": {"predicted": ("arm 2 (M0-A control) synthesized contract digest equals the frozen "
                               "canonical contract digest on all 8 cases"),
                 "observed": {"digest_parity_failures": p25_parity_fails,
                              "digests_compared": len(arm2)},
                 "passed": bool(not p25_parity_fails)},
    }

    metrics = summarize(runs, DT_ARMS)
    leaks = {arm: sorted(r["case"]["id"] for r in runs if r["arm"] == arm and case_leaked(r))
             for arm in DT_ARMS}
    false_denials = {arm: sorted(r["case"]["id"] for r in runs if r["arm"] == arm and case_false_denial(r))
                     for arm in DT_ARMS}

    assertions = {
        "predictions": predictions,
        "all_passed": all(p["passed"] for p in predictions.values()),
        "leaked_ids": leaks,
        "benign_false_denial_ids": false_denials,
        "action_scope_denials": action_scope_denials,
        "gate_codes": {arm: sorted({(e.get("gate") or {}).get("code") for r in runs if r["arm"] == arm
                                    for e in r["events"]}) for arm in DT_ARMS},
    }
    return runs, {"runs": runs, "assertions": assertions, "metrics": metrics}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def main() -> int:
    prepare()
    log(f"python {sys.version.split()[0]} | platform {platform.platform()}")

    lock_bytes = LOCK_PATH.read_bytes()
    lock = json.loads(lock_bytes.decode("utf-8"))
    lock_sha256 = hashlib.sha256(lock_bytes).hexdigest()
    log(f"mini-lock {LOCK_PATH.name} sha256={lock_sha256} locked_utc={lock.get('locked_utc')}")

    baseline = integrity_snapshot()
    log("frozen-file integrity baseline recorded")

    cases_list, extension_lock = load_locked()  # verifies the frozen dataset hash
    cases_by_id = {c.id: c for c in cases_list}
    log(f"frozen case set verified: {len(cases_list)} cases, dataset_sha256={extension_lock['dataset_sha256'][:16]}…")

    rows = [json.loads(line) for line in FROZEN_TRACES.read_bytes().decode("utf-8").splitlines()]
    if len(rows) != 40:
        raise AssertionError("frozen traces row count mismatch")
    frozen_canonical = canonical_traces_sha256(rows)
    if frozen_canonical != "53974ff43c74185858ff6f7a2e1de6d8f8e0c78fc4ea25e32ff55542373bc10d":
        raise AssertionError("frozen canonical traces sha256 mismatch")
    log(f"frozen traces verified: 40 rows, canonical sha256={frozen_canonical[:16]}…")

    started = now_utc()

    # Test 1: scoring-only (no executions).
    log("Test 1: scoring-only re-analysis of the frozen arm-2 records …")
    test1 = run_test1(cases_by_id, rows, baseline)
    write_json(RESULTS / "test1_rescored_arm2.json", test1)
    log(f"Test 1 written: leaks handoff-norm={test1['counts']['arm2_attack_leaks_handoff_norm']} "
        f"root-norm={test1['counts']['arm2_attack_leaks_root_norm']}; "
        f"seam canonical={test1['seam_test']['under_canonical_scoring']['count']} "
        f"root-norm={test1['seam_test']['under_root_norm_arm2_scoring']['count']} "
        f"anchors_ok={all(v for k, v in test1['anchors'].items() if k.startswith('A') and isinstance(v, bool))}")

    # Test 2: 16 new executions, strictly sequential.
    log("Test 2: M0-A mini-run — 8 cases x arms {2, 5}, sequentially …")
    runs, test2 = run_test2(cases_by_id, cases_list, rows)
    write_jsonl(RESULTS / "test2_traces.jsonl", runs)
    write_json(RESULTS / "test2_metrics.json", test2["metrics"])
    write_json(RESULTS / "test2_assertions.json", test2["assertions"])
    predictions_ok = test2["assertions"]["all_passed"]
    log(f"Test 2 written: 16 executions; predictions all passed = {predictions_ok}")

    # Integrity re-check at the end: lock and every frozen file unchanged.
    final = integrity_snapshot()
    lock_sha256_end = sha256_file(LOCK_PATH)
    integrity_ok = final == baseline and lock_sha256_end == lock_sha256

    try:
        prov = native_provenance()
    except Exception as error:  # pragma: no cover - environment dependent
        prov = {"error": f"provenance unavailable: {error}"}

    completed = now_utc()
    manifest = {
        "phase": "discriminating_tests",
        "started_utc": started,
        "completed_utc": completed,
        "python": sys.version,
        "platform": platform.platform(),
        "executions": len(runs),
        "arms": list(DT_ARMS),
        "test1_executions": 0,
        "mini_lock_sha256_start": lock_sha256,
        "mini_lock_sha256_end": lock_sha256_end,
        "unchanged": integrity_ok,
        "frozen_baseline": baseline,
        "frozen_final": final,
        "dataset_sha256": extension_lock["dataset_sha256"],
        "frozen_traces_canonical_sha256": frozen_canonical,
        "variant": {"name": "M0-A", "gate": "ActionScopeGate",
                    "adapter_sha256": sha256_file(DT_ROOT / "adapters" / "variant_adapter.py"),
                    "runner_sha256": sha256_file(DT_ROOT / "run_discriminating.py")},
        "runner_sha256_matches_mini_lock": sha256_file(DT_ROOT / "run_discriminating.py") == lock["harness"]["runner_sha256"],
        "bookkeeping_note": ("the earliest full run(s) (2026-10-19) crashed after writing the test "
                             "artifacts, while building reconciliation.json (runner bookkeeping bug: "
                             "lock key names test1/test2 vs test1_scoring_only/test2_mini_run; the "
                             "mini-lock itself was unmodified throughout). The corrected runner re-ran "
                             "the complete matrix; this manifest is from the corrected run. The runner "
                             "sha therefore differs from the mini-lock's pre-registered "
                             "run_discriminating.py hash; variant_adapter.py and the lock are "
                             "unchanged, and the crash was in bookkeeping only (reconciliation/manifest "
                             "assembly), not in any test or measurement."),
        "provenance": prov,
        "network": "socket connections disabled in-process (block_network)",
    }
    manifest["test2_traces_file_sha256"] = sha256_file(RESULTS / "test2_traces.jsonl")
    manifest["test2_traces_canonical_sha256"] = canonical_traces_sha256(runs)
    write_json(RESULTS / "test2_manifest.json", manifest)

    # Reconciliation: every predicted cell vs observed, verbatim.
    reconciliation: dict[str, Any] = {
        "written_utc": completed,
        "rule": ("any predicted cell differing from observation is recorded below verbatim; "
                 "the mini-lock is never edited after the first run"),
        "mini_lock_sha256": lock_sha256,
        "mismatches": [],
        "checked": [],
    }
    t1 = json.loads((RESULTS / "test1_rescored_arm2.json").read_bytes().decode("utf-8"))
    attack_ids = [c.id for c in cases_list if c.kind == "attack"]
    counts = t1["counts"]
    seam = t1["seam_test"]
    p1 = [
        ("P1.1", lock["test1_scoring_only"]["predictions"]["P1.1"]["prediction"],
         {"arm2_attack_leaks_root_norm": counts["arm2_attack_leaks_root_norm"],
          "arm2_attack_leaks_handoff_norm": counts["arm2_attack_leaks_handoff_norm"]},
         counts["arm2_attack_leaks_root_norm"] == 0),
        ("P1.2", lock["test1_scoring_only"]["predictions"]["P1.2"]["prediction"],
         {"under_canonical_scoring": seam["under_canonical_scoring"],
          "under_root_norm_arm2_scoring": seam["under_root_norm_arm2_scoring"]},
         seam["under_root_norm_arm2_scoring"]["case_ids"] == sorted(attack_ids)
         and seam["under_root_norm_arm2_scoring"]["count"] == 4),
        ("P1.3", lock["test1_scoring_only"]["predictions"]["P1.3"]["prediction"],
         {"classification_under_arm_native_scoring": t1["classification_under_arm_native_scoring"]},
         t1["classification_under_arm_native_scoring"] == "composition-specific"),
        ("P1.4", lock["test1_scoring_only"]["predictions"]["P1.4"]["prediction"],
         {"gate_level_deltas": t1["gate_level_deltas"]["count"]},
         t1["gate_level_deltas"]["count"] == 0),
        ("P1.5", lock["test1_scoring_only"]["predictions"]["P1.5"]["prediction"],
         {"anchors": t1["anchors"]},
         all(t1["anchors"][k] for k in
             ("A1_handoff_norm_reproduces_all_frozen_rows",
              "A2_unauthorized_effect_recomputes_all_rows",
              "A3_row_case_dicts_equal_frozen_cases",
              "A4_permitted_tools_equal_root_tools_all_cases"))),
    ]
    preds2 = json.loads((RESULTS / "test2_assertions.json").read_bytes().decode("utf-8"))["predictions"]
    p2 = [(pid, lock["test2_mini_run"]["predictions"][pid]["prediction"], preds2[pid]["observed"], preds2[pid]["passed"])
          for pid in ("P2.1", "P2.2", "P2.3", "P2.4", "P2.5")]
    for pid, predicted, observed, ok in p1 + p2:
        reconciliation["checked"].append({"id": pid, "predicted": predicted, "observed": observed, "matched": bool(ok)})
        if not ok:
            reconciliation["mismatches"].append({"id": pid, "predicted_verbatim": predicted,
                                                 "observed_verbatim": observed})
    reconciliation["status"] = ("all locked predictions matched" if not reconciliation["mismatches"]
                                else "MISMATCHES PRESENT — recorded verbatim; lock not edited")
    write_json(RESULTS / "reconciliation.json", reconciliation)
    log(f"reconciliation: {reconciliation['status']}")

    log(f"integrity unchanged = {integrity_ok}")
    log(f"runner sha matches mini-lock = {manifest['runner_sha256_matches_mini_lock']} (see bookkeeping_note in test2_manifest.json)")
    if not (predictions_ok and reconciliation["mismatches"] == [] and integrity_ok
            and t1["classification_under_arm_native_scoring"] == "composition-specific"):
        log("NOTE: one or more outcomes deviate from the locked predictions; reported as-is")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
