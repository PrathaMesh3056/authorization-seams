"""Read-only audit of exported artifact completeness and cross-run semantic replay.

No native engine or runner import: validates exported counts/effects and hashes.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def audit(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
    metrics = json.loads((directory / "metrics.json").read_text(encoding="utf-8"))
    traces = read_jsonl(directory / "traces.jsonl")
    reductions = read_jsonl(directory / "counterexamples.jsonl")
    probes = read_jsonl(directory / "adaptive_probes.jsonl")
    latencies = json.loads((directory / "latency.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert len(cases) == 80 and len(traces) == 560
    identifiers = {c["id"] for c in cases}
    counts = Counter((t["arm"], t["case"]["id"]) for t in traces)
    assert len(counts) == 560 and set(counts.values()) == {1}
    assert all({t["case"]["id"] for t in traces if t["arm"] == a} == identifiers for a in manifest["arms"])
    expected_disagreements = set()
    for arm, m in metrics.items():
        rows = [t for t in traces if t["arm"] == arm]
        unsafe_attacks, benign_denials = 0, 0
        for t in rows:
            unsafe = denial = False
            for e in t["events"]:
                assert e["oracle_allowed"] == (not e["oracle_reasons"])
                assert bool(e["effects"]) == e["decision"]["allowed"]
                assert e["unauthorized_effect"] == (bool(e["effects"]) and not e["oracle_allowed"])
                assert e["false_denial"] == (e["oracle_allowed"] and not e["decision"]["allowed"])
                unsafe |= e["unauthorized_effect"]
                denial |= e["false_denial"]
            unsafe_attacks += t["case"]["kind"] == "attack" and unsafe
            benign_denials += t["case"]["kind"] == "benign" and denial
            if unsafe or denial:
                expected_disagreements.add((arm, t["case"]["id"]))
        assert unsafe_attacks == m["attack_successes"]
        assert benign_denials == m["benign_false_denial_cases"]
    actual_reductions = [(r["arm"], r["original_case"]) for r in reductions]
    assert set(actual_reductions) == expected_disagreements
    assert len(actual_reductions) == len(expected_disagreements)
    for reduced in reductions:
        events = reduced["reduced_run"]["events"]
        actual = [any(e["unauthorized_effect"] for e in events), any(e["false_denial"] for e in events),
                  any(effect.get("contains_confidential_marker", False) for e in events for effect in e["effects"])]
        assert actual == reduced["failure_signature"]
    assert len(probes) == len(manifest["arms"]) * 8 * manifest["parameters"]["adaptive_rounds"]
    assert all(not p["unauthorized_effect"] or not p["oracle_allowed"] for p in probes)
    assert len(latencies) == 7
    assert all(l["samples"] == manifest["parameters"]["samples"] for l in latencies)
    assert all(l["warmup"] == manifest["parameters"]["warmup"] for l in latencies)
    digest = hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()
    assert digest == manifest["dataset_sha256"]
    semantic = [{"arm": t["arm"], "id": t["case"]["id"], "outcomes":
                 [[e["decision"]["allowed"], e["oracle_reasons"], e["effects"]] for e in t["events"]]} for t in traces]
    outcome_digest = hashlib.sha256(json.dumps(semantic, sort_keys=True).encode()).hexdigest()
    assert outcome_digest == manifest["outcome_sha256"]
    for relative, expected in manifest.get("harness_sha256", {}).items():
        snapshot = directory / "harness_sources" / relative
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == expected
    return {"directory": str(directory.resolve()), "runs": len(traces), "cases": len(cases),
            "disagreements_reduced": len(reductions), "structured_feedback_probes": len(probes),
            "latency_samples": sum(l["samples"] for l in latencies), "dataset_sha256": digest,
            "outcome_sha256": outcome_digest, "passed": True}


def main():
    directories = [Path(arg) for arg in sys.argv[1:]]
    if not directories:
        raise SystemExit("Usage: python -m seam_pilot.audit RESULTS_DIR [REPLAY_RESULTS_DIR]")
    records = [audit(d) for d in directories]
    result = {"runs": records}
    if len(records) > 1:
        assert len({r["dataset_sha256"] for r in records}) == 1
        assert len({r["outcome_sha256"] for r in records}) == 1
        result["matrix_semantic_replay_matches"] = True
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
