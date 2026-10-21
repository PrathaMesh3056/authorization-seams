"""Adversarial review, mechanical pass 1 (read-only over frozen artifacts).

Disclosed temp output: results/review_tmp/adv_stats.json (+ stdout).
Commands: python review_tmp/adv_mech.py  (cwd = tests/seam_pilot_sentinelagent)
No frozen file is modified. No network. No paid calls.
"""
import json
import sys
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

SA = Path(__file__).resolve().parents[2]         # .../results/review_tmp -> tests/seam_pilot_sentinelagent
RESULTS = SA / "results"
sys.path.insert(0, str(SA / "design"))

RUNS = RESULTS / "sa" / "runs.jsonl"
rows = []
with RUNS.open(encoding="utf-8") as fh:
    for line in fh:
        if line.strip():
            rows.append(json.loads(line))

print(f"rows={len(rows)}")

ARMS = ("apc_alone", "sentinelagent_alone", "apc_apc_preserved", "apc_apc_reset",
        "apc_sentinelagent_scope_only", "apc_sentinelagent_retained",
        "apc_sentinelagent_fail_closed")
TOKEN_ARMS = ("sentinelagent_alone", "apc_sentinelagent_scope_only",
              "apc_sentinelagent_retained", "apc_sentinelagent_fail_closed")

# --- A. structure ------------------------------------------------------------
arms_counter = Counter(r["arm"] for r in rows)
ids_by_arm = defaultdict(list)
kinds_by_arm = defaultdict(Counter)
for r in rows:
    ids_by_arm[r["arm"]].append(r["case"]["id"])
    kinds_by_arm[r["arm"]][r["case"]["kind"]] += 1
structure = {
    "rows": len(rows),
    "rows_per_arm": dict(arms_counter),
    "dup_ids_per_arm": {a: [k for k, v in Counter(ids_by_arm[a]).items() if v > 1] for a in ARMS},
    "missing_ids_per_arm": {},
    "kinds_per_arm": {a: dict(kinds_by_arm[a]) for a in ARMS},
}
case_ids = set(ids_by_arm["apc_alone"])
for a in ARMS:
    diff = case_ids ^ set(ids_by_arm[a])
    if diff:
        structure["missing_ids_per_arm"][a] = sorted(diff)

# --- B. frozen 80 reuse ------------------------------------------------------
sa_cases_doc = json.loads((SA / "design" / "sa_cases.json").read_text(encoding="utf-8"))
sa_cases = sa_cases_doc["cases"]
frozen_doc = json.loads((SA.parent / "seam_pilot_v2" / "design" / "frozen_cases.json").read_text(encoding="utf-8"))
frozen_by_id = {c["id"]: c for c in frozen_doc["cases"]}
sa_by_id = {c["id"]: c for c in sa_cases}
SA_ONLY_KEYS = {"token_provenance", "presented_resource"}
first80 = [c["id"] for c in sa_cases[:80]]
reuse_diff = []
override_ids = set()
for cid in first80:
    f = frozen_by_id[cid]
    s = sa_by_id[cid]
    s_core = {k: v for k, v in s.items() if k not in SA_ONLY_KEYS}
    if s_core != f:
        changed = [k for k in f if k in s_core and s_core[k] != f[k]]
        added = [k for k in s_core if k not in f]
        removed = [k for k in f if k not in s_core]
        reuse_diff.append({"id": cid, "changed": changed, "added": added, "removed": removed,
                           "pred_frozen": f.get("predicted_safe"), "pred_sa": s_core.get("predicted_safe")})
override_detail = [c for c in first80 if c in reuse_diff]
new16 = [c["id"] for c in sa_cases[80:]]
sig_counts = Counter("attack" if sa_by_id[c]["kind"] == "attack" else "benign" for c in new16)
variants = {}
for c in new16:
    d = sa_by_id[c]
    variants.setdefault((d["template"], d["kind"]), 0)
    variants[(d["template"], d["kind"])] += 1

# --- C. flag re-derivation ---------------------------------------------------
flag_exceptions = Counter()
sig_clause_fires = 0
for r in rows:
    arm = r["arm"]
    if arm in TOKEN_ARMS:
        for e in r["events"]:
            tok = e.get("token") or {}
            presented = bool(tok.get("presented"))
            sig_ok = tok.get("signature_ok")
            derived_unauth = bool(e["oracle_reasons"] and e["effects"]) or bool(e["allowed"] and presented and sig_ok is False)
            derived_fd = bool((not e["oracle_reasons"]) and (not e["allowed"]) and not (presented and sig_ok is False))
            if e.get("unauthorized_effect") != derived_unauth:
                flag_exceptions["unauth"] += 1
            if e.get("false_denial") != derived_fd:
                flag_exceptions["fd"] += 1
            if e["allowed"] and presented and sig_ok is False:
                sig_clause_fires += 1
    else:
        for e in r["events"]:
            if e.get("unauthorized_effect") != bool(e["oracle_reasons"] and e["effects"]):
                flag_exceptions["unauth_v2"] += 1
            if e.get("false_denial") != bool((not e["oracle_reasons"]) and (not e["allowed"])):
                flag_exceptions["fd_v2"] += 1
            if e.get("unauthorized_effect") and not (e["effects"] and e["oracle_reasons"]):
                flag_exceptions["leak_without_effect"] += 1

# --- D. per-arm recomputation ------------------------------------------------
per_arm = {}
for a in ARMS:
    arows = [r for r in rows if r["arm"] == a]
    leak_cases = sorted(r["case"]["id"] for r in arows
                        if r["case"]["kind"] == "attack"
                        and any(e.get("unauthorized_effect") for e in r["events"]))
    leak_events = sum(1 for r in arows for e in r["events"] if e.get("unauthorized_effect"))
    fd_cases = sorted(r["case"]["id"] for r in arows
                      if r["case"]["kind"] == "benign"
                      and any(e.get("false_denial") for e in r["events"]))
    fd_events_total = sum(1 for r in arows for e in r["events"] if e.get("false_denial"))
    fd_events_attack = sum(1 for r in arows for e in r["events"]
                           if e.get("false_denial") and r["case"]["kind"] == "attack")
    marker_ext = sum(1 for r in arows for e in r["events"] for eff in e.get("effects", [])
                     if eff.get("type") == "external_send" and eff.get("contains_confidential_marker"))
    codes = Counter()
    admissions = 0
    token_events = 0
    token_denials = 0
    native_denials = 0
    present_events = 0
    for r in arows:
        for e in r["events"]:
            gate = e.get("gate")
            if gate:
                codes[gate.get("code", "?")] += 1
            else:
                codes["ADMITTED" if e.get("allowed") else "APC-DENY"] += 1
            if e.get("allowed"):
                admissions += 1
            tok = e.get("token")
            if isinstance(tok, dict) and "presented" in tok:
                if tok.get("presented"):
                    token_events += 1
                    present_events += 1
                if not e.get("allowed"):
                    token_denials += 1
                    if tok.get("presented"):
                        native_denials += 1
    leak_examples = []
    for r in arows:
        if r["case"]["id"] in leak_cases:
            for e in r["events"]:
                if e.get("unauthorized_effect"):
                    leak_examples.append({
                        "case": r["case"]["id"], "phase": e["phase"], "index": e["index"],
                        "tool": e["tool"], "oracle_reasons": e["oracle_reasons"],
                        "gate": (e.get("gate") or {}).get("code"),
                        "effect_types": [x.get("type") for x in e["effects"]],
                    })
    per_arm[a] = {
        "rows": len(arows), "leak_cases": leak_cases, "n_leak_cases": len(leak_cases),
        "leak_events": leak_events, "fd_cases": fd_cases, "n_fd_cases": len(fd_cases),
        "fd_events_total": fd_events_total, "fd_events_attack": fd_events_attack,
        "marker_external": marker_ext,
        "codes": dict(codes), "admissions": admissions,
        "token_events_presented": token_events, "token_denials_incl_prepresent": token_denials,
        "denials_with_presented_token": native_denials,
        "leak_examples": leak_examples,
    }

arm2 = set(per_arm["sentinelagent_alone"]["leak_cases"])
arm5 = set(per_arm["apc_sentinelagent_scope_only"]["leak_cases"])
seam = sorted(set(per_arm["apc_sentinelagent_scope_only"]["leak_cases"])
              | set(per_arm["apc_sentinelagent_retained"]["leak_cases"])
              | set(per_arm["apc_sentinelagent_fail_closed"]["leak_cases"]))
seam = [c for c in seam
        if c not in arm2 and c not in set(per_arm["apc_alone"]["leak_cases"])]

# --- E. leak-class split / repeated events -----------------------------------
template_of = {c["id"]: c["template"] for c in sa_cases}
leak_templates = Counter(template_of[c] for c in arm2)

# --- F. arm2 vs arm5 contract comparison (presented tokens, downstream) -------
contract_diff = []
for cid in sorted(case_ids):
    r2 = next(r for r in rows if r["arm"] == "sentinelagent_alone" and r["case"]["id"] == cid)
    r5 = next(r for r in rows if r["arm"] == "apc_sentinelagent_scope_only" and r["case"]["id"] == cid)
    ev2 = [e for e in r2["events"] if e["phase"] == "downstream"]
    ev5 = [e for e in r5["events"] if e["phase"] == "downstream"]
    if len(ev2) != len(ev5):
        contract_diff.append({"id": cid, "issue": f"event count {len(ev2)} vs {len(ev5)}"})
        continue
    for a, b in zip(ev2, ev5):
        t2 = (a.get("token") or {}).get("manifest")
        t5 = (b.get("token") or {}).get("manifest")
        s2 = (a.get("token") or {}).get("scope")
        s5 = (b.get("token") or {}).get("scope")
        x2 = (a.get("token") or {}).get("output_schema")
        x5 = (b.get("token") or {}).get("output_schema")
        e2 = (a.get("token") or {}).get("expiry")
        e5 = (b.get("token") or {}).get("expiry")
        if t2 != t5 or s2 != s5 or x2 != x5 or e2 != e5:
            contract_diff.append({"id": cid, "idx": a["index"], "manifest2": t2, "manifest5": t5,
                                  "scope2": s2, "scope5": s5, "schema2": x2, "schema5": x5,
                                  "expiry2": e2, "expiry5": e5})
    # code comparison
    c2 = [(e["index"], (e.get("gate") or {}).get("code")) for e in ev2]
    c5 = [(e["index"], (e.get("gate") or {}).get("code")) for e in ev5]
    if c2 != c5:
        contract_diff.append({"id": cid, "issue": "gate codes differ", "arm2": c2, "arm5": c5})

# --- G. lock expectations vs observed ----------------------------------------
lock = json.loads((SA / "design" / "sa_lock.json").read_text(encoding="utf-8"))
expected = lock["expected_per_arm"]
lock_obs = {}
for a in ARMS:
    exp = expected[a]
    obs = per_arm[a]
    lock_obs[a] = {
        "leak_cases": {"exp": exp["leak_cases"], "obs": obs["n_leak_cases"]},
        "leak_events": {"exp": exp["leak_events"], "obs": obs["leak_events"]},
        "benign_fd_cases": {"exp": exp["benign_fd_cases"], "obs": obs["n_fd_cases"]},
        "fd_events": {"exp": exp["fd_events"], "obs": obs["fd_events_total"]},
    }
exp_leak_set = set(lock["expected_leak_cases_arms_2_and_5"])
lock_obs["arm2_arm5_expected_set_match"] = {
    "exp_n": len(exp_leak_set), "obs_arm2": sorted(arm2 - exp_leak_set),
    "missing_arm2": sorted(exp_leak_set - arm2), "obs_arm5": sorted(arm5 - exp_leak_set),
    "missing_arm5": sorted(exp_leak_set - arm5)}

# --- H. arm 6 closure deep check ---------------------------------------------
a6rows = [r for r in rows if r["arm"] == "apc_sentinelagent_retained"]
a6_by_case = {r["case"]["id"]: r for r in a6rows}
att_missing = []
apcdeny_payload = []
native_after_att = 0
for cid, r in a6_by_case.items():
    for e in r["events"]:
        if e["phase"] != "downstream":
            continue
        att = e.get("attestation")
        if att is None:
            att_missing.append(f"{cid}/idx{e['index']}")
            continue
        payload = json.loads(att["intent_text"])
        code = (e.get("gate") or {}).get("code")
        if code == "APC-DENY":
            apcdeny_payload.append({"case": cid, "apc_allowed": payload.get("apc_allowed"),
                                    "sig_ok": att.get("signature_ok"),
                                    "reasons": (e.get("gate") or {}).get("reasons")})
        if payload.get("apc_allowed") and isinstance(e.get("gate", {}).get("checks", {}).get("native"), dict):
            native_after_att += 1
unsat_a6 = a6_by_case.get("unsatisfiable_verify-0-a")
unsat_effects = []
if unsat_a6:
    for e in unsat_a6["events"]:
        if e["phase"] == "downstream":
            unsat_effects.append({"tool": e["tool"], "allowed": e["allowed"],
                                  "effects": [x.get("type") for x in e["effects"]]})

# --- I. arm 7 FD breakdown ----------------------------------------------------
a7rows = [r for r in rows if r["arm"] == "apc_sentinelagent_fail_closed"]
fd_event_detail = []
for r in a7rows:
    for e in r["events"]:
        if e.get("false_denial"):
            fd_event_detail.append({
                "case": r["case"]["id"], "kind": r["case"]["kind"], "idx": e["index"],
                "tool": e["tool"], "code": (e.get("gate") or {}).get("code"),
                "oracle": e["oracle_reasons"],
            })
fd_by_template = Counter(template_of[d["case"]] for d in fd_event_detail)
a6_admitted_benign = {cid for cid, r in a6_by_case.items()
                      if r["case"]["kind"] == "benign"
                      and any(e.get("allowed") for e in r["events"] if e["phase"] == "downstream")}
a7_fd_set = set(d["cases"] if False else d["case"] for d in fd_event_detail if d["kind"] == "benign")
overlap_fd_safe_in_a6 = sorted(a7_fd_set & a6_admitted_benign)

# --- J. not-vacuous + keyholder grid -----------------------------------------
keyholder = {}
for tmpl in ("foreign_key_signed", "trusted_key_signed", "keyholder_widen", "keyholder_plain"):
    ids = [c["id"] for c in sa_cases if template_of[c["id"]] == tmpl] if False else \
          [c["id"] for c in sa_cases if c["template"] == tmpl]
    for a in TOKEN_ARMS:
        grid = []
        for cid in ids:
            r = next(rr for rr in rows if rr["arm"] == a and rr["case"]["id"] == cid)
            for e in r["events"]:
                if e["phase"] == "downstream":
                    grid.append({"code": (e.get("gate") or {}).get("code") or ("ADMITTED" if e.get("allowed") else "APC-DENY"),
                                 "presented": bool((e.get("token") or {}).get("presented")),
                                 "sig_ok": (e.get("token") or {}).get("signature_ok")})
        keyholder[f"{tmpl}|{a}"] = grid

stats = {
    "structure": structure,
    "reuse_diff": reuse_diff,
    "override_cases_found": [d["id"] for d in reuse_diff],
    "new16": new16, "new16_split": dict(sig_counts), "new16_by_template_kind": {f"{k[0]}|{k[1]}": v for k, v in variants.items()},
    "flag_exceptions": dict(flag_exceptions),
    "sig_clause_fires": sig_clause_fires,
    "per_arm": {a: {k: v for k, v in d.items() if k != "leak_examples"} for a, d in per_arm.items()},
    "leak_examples_sentinelagent_alone": per_arm["sentinelagent_alone"]["leak_examples"],
    "leak_events_delta_30": {a: [x for x in per_arm[a]["leak_examples"] if a in ("sentinelagent_alone",)] for a in ("sentinelagent_alone",)},
    "leak_template_split_arm2": dict(leak_templates),
    "seam_cases": seam,
    "arm5_code_equals_arm2": not any("issue" in d or "manifest2" in d or "gate codes" in json.dumps(d) for d in contract_diff),
    "contract_diff": contract_diff[:40],
    "lock_vs_obs": lock_obs,
    "a6": {"att_missing_downstream": att_missing, "apcdeny_payload_dump": apcdeny_payload[:8],
           "native_checks_after_attestation_ok": native_after_att,
           "unsat_a6_events": unsat_effects},
    "a7": {"fd_events": fd_event_detail, "fd_template_counts": dict(fd_by_template),
           "fd_benign_all_in_arm6_admitted": overlap_fd_safe_in_a6,
           "fd_benign_n": len(a7_fd_set)},
    "keyholder_grid": keyholder,
}
out = RESULTS / "review_tmp" / "adv_stats.json"
out.write_text(json.dumps(stats, indent=1, ensure_ascii=False)[:200000] + "\n", encoding="utf-8")
print(f"contract_diff_n={len(contract_diff)}")
print(json.dumps({k: v for k, v in stats.items() if k in
                  ("structure", "override_cases_found", "new16_split", "flag_exceptions",
                   "sig_clause_fires", "seam_cases", "leak_template_split_arm2",
                   "a6", "a7", "lock_vs_obs")}, indent=1, default=str)[:12000])
print("WROTE", out)
