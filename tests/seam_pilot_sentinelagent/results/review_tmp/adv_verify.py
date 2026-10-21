"""Adversarial review, mechanical pass 2 (disclosed re-executions; writes nothing frozen).

Commands: python review_tmp/adv_verify.py  (cwd = tests/seam_pilot_sentinelagent)
1. Independent determinism re-execution: 10 cases x arms 2/5, event-by-event vs
   runs.jsonl with timing keys stripped (same predicate as the run's self-review).
2. Independent cryptographic re-verification of every arm-6 attestation signature:
   reconstruct the DelegationToken from the recorded fields, recompute HMAC under
   BRIDGE_KEY and under REAL_DAS_KEY, compare with the recorded signature.
3. Frozen-reference consistency: SA arms 1/3/4 restricted to the shared 80 vs the
   frozen v2 raw_metrics aggregates.
4. SA raw_metrics.json vs metrics.json 'metrics' block equality.
No network. No paid calls. No frozen file touched.
"""
import hashlib
import hmac
import json
import sys
from pathlib import Path

SA = Path(__file__).resolve().parents[2]
RESULTS = SA / "results"
sys.path.insert(0, str(SA / "adapters"))
sys.path.insert(0, str(SA / "design"))

import sa_harness  # noqa: E402  (module import only; no side effects beyond sys.path)
from sa_case_generator import SACase  # noqa: E402

INSTALL_PROOF = sa_harness.install_bridge_key()
print("installed key model:", json.dumps(INSTALL_PROOF)[:220])

rows = []
with (RESULTS / "sa" / "runs.jsonl").open(encoding="utf-8") as fh:
    for line in fh:
        if line.strip():
            rows.append(json.loads(line))

# --- 1. determinism ----------------------------------------------------------
TIMING_KEYS = {"authorization_ns", "envelope_id"}

def strip(value):
    if isinstance(value, dict):
        return {k: strip(v) for k, v in value.items() if k not in TIMING_KEYS}
    if isinstance(value, list):
        return [strip(v) for v in value]
    return value

cases_doc = json.loads((SA / "design" / "sa_cases.json").read_text(encoding="utf-8"))["cases"]
by_id = {c["id"]: c for c in cases_doc}
sample = sorted(by_id)[:10]
mismatches = []
diff_paths = []

def first_diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            va, vb = a.get(k), b.get(k)
            d = first_diff(va, vb, f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f"{path}: len {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{path}: {a!r} vs {b!r}"

for cid in sample:
    case = SACase.from_dict(by_id[cid])
    for arm in ("sentinelagent_alone", "apc_sentinelagent_scope_only"):
        old = next(r for r in rows if r["arm"] == arm and r["case"]["id"] == cid)
        fresh = sa_harness.run_case_sa(case, arm)
        fresh = json.loads(json.dumps(fresh, ensure_ascii=False, default=str))
        old = json.loads(json.dumps(old, ensure_ascii=False, default=str))
        if strip(fresh) != strip(old):
            mismatches.append(cid + "/" + arm)
            if len(diff_paths) < 4 and cid == "budget_preserved-0-b":
                diff_paths.append((cid + "/" + arm, first_diff(strip(fresh), strip(old))))
print(f"determinism independent rerun: sample={len(sample) * 2} mismatches={len(mismatches)}")
for p in diff_paths:
    print("first diff:", p)

# --- 2. attestation signatures ----------------------------------------------
arm6 = [r for r in rows if r["arm"] == "apc_sentinelagent_retained"]
BRIDGE = sa_harness.BRIDGE_KEY
REAL = sa_harness.REAL_DAS_KEY
bad_bridge = 0
ok_real = 0
count = 0
sig_by_id = {}
for r in arm6:
    for e in r["events"]:
        att = e.get("attestation")
        if not att:
            continue
        count += 1
        token = sa_harness.sa_native.DelegationToken(
            token_id=att["token_id"], src=att["src"], dst=att["dst"],
            scope=set(att["scope"]), manifest={k: list(v) for k, v in att["manifest"].items()},
            output_schema={}, policy=set(), parent_hash="ROOT",
            expiry=att["expiry"], intent_text=att["intent_text"])
        token.signature = att["signature"]
        canon = token._canonical()
        mac_bridge = hmac.new(BRIDGE, canon.encode("utf-8"), hashlib.sha256).hexdigest()
        mac_real = hmac.new(REAL, canon.encode("utf-8"), hashlib.sha256).hexdigest()
        native_ok = token.verify_signature()
        if att["signature"] != mac_bridge or not native_ok:
            bad_bridge += 1
            sig_by_id.setdefault("bad", []).append(att["token_id"])
        if att["signature"] == mac_real:
            ok_real += 1
print(f"attestations total={count} bridge-key_mismatch={bad_bridge} signed_with_real_das_key={ok_real}")

# --- 3. frozen reference consistency -----------------------------------------
v2raw = json.loads((SA.parent / "seam_pilot_v2" / "results" / "raw_metrics.json").read_text(encoding="utf-8"))
frozen_ids = set(by_id)  # SA set; shared = those in frozen_cases.json
frozen_cases = json.loads((SA.parent / "seam_pilot_v2" / "design" / "frozen_cases.json").read_text(encoding="utf-8"))
frozen_ids = {c["id"] for c in frozen_cases["cases"]}
shared = frozen_ids & set(by_id)
ref = {}
for arm in ("apc_alone", "apc_apc_reset"):
    srows = [r for r in rows if r["arm"] == arm and r["case"]["id"] in shared]
    leaked = sum(1 for r in srows if r["case"]["kind"] == "attack"
                 and any(e.get("unauthorized_effect") for e in r["events"]))
    fd = sum(1 for r in srows if r["case"]["kind"] == "benign"
             and any(e.get("false_denial") for e in r["events"]))
    r = v2raw[arm]
    ref[arm] = {
        "shared_n": len(shared),
        "obs_leaks": leaked, "ref_leaks": r["attack_successes"],
        "obs_fd": fd, "ref_fd": len(r["benign_false_denial_cases"]) if isinstance(r.get("benign_false_denial_cases"), list) else r.get("benign_false_denial_cases"),
        "match": leaked == r["attack_successes"] and fd == r["benign_false_denial_cases"],
        "leaked_ids": sorted({x["case"]["id"] for x in ({ "case": s["case"]} for s in srows
                           if any(e.get("unauthorized_effect") for e in s["events"]))}),
    }
print("frozen reference consistency:", json.dumps(ref, indent=1))

# --- 4. raw vs metrics -------------------------------------------------------
raw = json.loads((RESULTS / "sa" / "raw_metrics.json").read_text(encoding="utf-8"))
met = json.loads((RESULTS / "sa" / "metrics.json").read_text(encoding="utf-8"))["metrics"]
print("raw_metrics == metrics metrics-block:", raw == met)
print("WROTE nothing to frozen tree")
