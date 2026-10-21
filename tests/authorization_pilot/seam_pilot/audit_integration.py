"""Read-only independent replay of exported integration effects and oracle labels."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from .model import Call, Case, MockWorld, Oracle


def load_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def sig(row):
    return [any(e["unauthorized_effect"] for e in row["events"]),
            any(e["false_denial"] for e in row["events"]),
            any(f.get("contains_confidential_marker", False) for e in row["events"] for f in e["effects"])]


def replay(row):
    """Uses mock effects and independent root oracle; no native engines or runner."""
    case = Case.from_dict(row["case"])
    world, oracle = MockWorld(case), Oracle(case)
    downstream_commits = 0
    for event in row["events"]:
        call = Call(**event["proposed"])
        canonical = world.canonical(call)
        if row["allow_default"] and call.tool == "send_external" and "recipient" not in call.args:
            canonical["recipient"] = case.recipient
        assert canonical == event["canonical_args"]
        reasons = oracle.decide(call, canonical, event["phase"])
        assert reasons == event["oracle_reasons"]
        assert bool(event["effects"]) == event["allowed"]
        if event["effects"]:
            effects = world.execute(call, canonical)
            assert effects == event["effects"]
            oracle.observe(call, effects)
        assert event["unauthorized_effect"] == bool(reasons and event["effects"])
        assert event["false_denial"] == (not reasons and not event["allowed"])
        if event["phase"] == "downstream":
            if event["allowed"]:
                downstream_commits += 1
                assert event["state_after"]["spent"] == event["state_before"]["spent"] + call.cost
                assert event["state_after"]["history"] == event["state_before"]["history"] + [call.tool]
                assert event["state_after"]["commits"] == event["state_before"]["commits"] + 1
            else:
                assert event["state_before"] == event["state_after"]
                assert any(not g["allowed"] for g in event["predicate_evaluations"])
    assert row["final_state"]["spent"] == oracle.total_cost
    assert row["final_state"]["commits"] == downstream_commits


def audit(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
    traces = load_rows(directory / "traces.jsonl")
    metrics = json.loads((directory / "metrics.json").read_text(encoding="utf-8"))
    reductions = load_rows(directory / "counterexamples.jsonl")
    focused = load_rows(directory / "optional_argument_diagnostics.jsonl")
    controls = json.loads((directory / "homogeneous_controls.json").read_text(encoding="utf-8"))
    timings = json.loads((directory / "latency.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert len(cases) == 80 and len(traces) == 320 and len(focused) == 20 and len(controls) == 9
    assert digest(cases) == manifest["dataset_sha256"]
    counts = Counter((r["path"], r["case"]["id"]) for r in traces)
    assert len(counts) == 320 and set(counts.values()) == {1}
    for path in manifest["paths"]:
        assert {r["case"]["id"] for r in traces if r["path"] == path} == {c["id"] for c in cases}
        rows = [r for r in traces if r["path"] == path]
        m = metrics[path]
        assert m["runs"] == len(rows) == 80
        assert m["attack_cases"] == m["benign_cases"] == 40
        assert m["unauthorized_attack_cases"] == sum(r["case"]["kind"] == "attack" and sig(r)[0] for r in rows)
        assert m["benign_false_denial_cases"] == sum(r["case"]["kind"] == "benign" and sig(r)[1] for r in rows)
        assert m["marker_sends"] == sum(f.get("contains_confidential_marker", False)
                                         for r in rows for e in r["events"] for f in e["effects"])
    mismatches = {(r["path"], r["case"]["id"]) for r in traces if any(sig(r)[:2])}
    assert {(r["path"], r["original_case"]) for r in reductions} == mismatches
    assert len(reductions) == len(mismatches)
    for row in traces + focused + [r["reduced_run"] for r in reductions]:
        replay(row)
    for reduced in reductions:
        assert sig(reduced["reduced_run"]) == reduced["signature"]
    for control in controls:
        assert bool(control["effects"]) == control["allowed"]
        assert control["unauthorized_effect"] == any(f["recipient"] != "reviewer0@example.test" for f in control["effects"])
    assert len(timings) == 4 and all(t["warmup"] == manifest["warmup"] and t["samples"] == manifest["samples"] for t in timings)
    observations = [{"path": r["path"], "id": r["case"]["id"], "allow_default": r["allow_default"],
                     "events": [[e["allowed"], e["oracle_reasons"], e["effects"]] for e in r["events"]]} for r in traces]
    assert digest(observations) == manifest["outcome_sha256"]
    for relative, expected in manifest["harness_sha256"].items():
        actual = (directory / "harness_sources" / relative).read_bytes()
        assert hashlib.sha256(actual).hexdigest() == expected
    return {"directory": str(directory.resolve()), "passed": True, "runs": len(traces),
            "reduced_disagreements": len(reductions), "diagnostics": len(focused), "controls": len(controls),
            "dataset_sha256": manifest["dataset_sha256"], "outcome_sha256": manifest["outcome_sha256"]}


if __name__ == "__main__":
    audited = [audit(path) for path in sys.argv[1:]]
    if len(audited) == 2:
        assert audited[0]["dataset_sha256"] == audited[1]["dataset_sha256"]
        assert audited[0]["outcome_sha256"] == audited[1]["outcome_sha256"]
    print(json.dumps({"audits": audited, "replay_identical": len(audited) == 2}, indent=2))
