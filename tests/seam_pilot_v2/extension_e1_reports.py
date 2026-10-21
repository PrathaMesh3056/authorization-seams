"""Generate the Extension E1 deliverables from the written artifacts.

Writes:
  - results/claims_update_extension.md      (one H1 action-type claim record)
  - results/EXTENSION_E1_RESULTS.md         (the consolidated report)

The report embeds `design/action_narrow_condition.md` and
`results/claims_update_extension.md` byte-verbatim between BEGIN/END markers and
re-verifies the injection after writing. Pure report generation: it reads the
frozen artifacts and never re-runs a case.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

V2_ROOT = Path(__file__).resolve().parent
DESIGN = V2_ROOT / "design"
RES = V2_ROOT / "results" / "extension_e1"
OUT_REPORT = V2_ROOT / "results" / "EXTENSION_E1_RESULTS.md"
OUT_CLAIMS = V2_ROOT / "results" / "claims_update_extension.md"

CONDITION = DESIGN / "action_narrow_condition.md"
CASES = DESIGN / "extension_e1_cases.json"
LOCKF = DESIGN / "extension_e1_lock.json"
MANIFEST = RES / "manifest.json"
TRACES = RES / "traces.jsonl"
CONTROLS = RES / "controls.json"
ASSERTIONS = RES / "assertions.json"
METRICS = RES / "metrics.json"
CONDITION_JSON = RES / "condition.json"

ARMS = (
    "apc_alone",
    "tracegrant_alone",
    "apc_tracegrant_scope_only",
    "apc_tracegrant_retained",
    "apc_tracegrant_fail_closed",
)
ARM_LABEL = {
    "apc_alone": "1 `apc_alone`",
    "tracegrant_alone": "2 `tracegrant_alone` (M0)",
    "apc_tracegrant_scope_only": "5 `..._scope_only` (M0)",
    "apc_tracegrant_retained": "6 `..._retained` (M2-auth)",
    "apc_tracegrant_fail_closed": "7 `..._fail_closed` (M1/shadow)",
}


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mtime_utc(path: Path) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(path.stat().st_mtime))


def load_json(path: Path):
    return json.loads(path.read_bytes().decode("utf-8"))


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_bytes().decode("utf-8").splitlines()]


def _cell(run) -> str:
    event = run["events"][-1]
    code = (event.get("gate") or {}).get("code")
    if event["unauthorized_effect"]:
        return f"**LEAK** ({code})"
    if event["allowed"]:
        return f"allow ({code})" if code else "allow"
    if run["arm"] == "apc_alone":
        return "deny (APC)"
    return f"deny ({code})"


def build_report() -> str:
    lock = load_json(LOCKF)
    manifest = load_json(MANIFEST)
    runs = load_jsonl(TRACES)
    controls = load_json(CONTROLS)
    assertions = load_json(ASSERTIONS)
    metrics = load_json(METRICS)
    confusion = load_json(CONDITION_JSON)
    cases_data = load_json(CASES)
    cases = {c["id"]: c for c in cases_data["cases"]}
    condition_text = _read_bytes(CONDITION).decode("utf-8")
    claims_text = _read_bytes(OUT_CLAIMS).decode("utf-8")
    adapter_text = _read_bytes(V2_ROOT / "adapters" / "extension_e1.py").decode("utf-8")
    scheme_start = adapter_text.index("M2-auth signing scheme")
    scheme_end = adapter_text.index('"""', scheme_start)
    scheme_text = adapter_text[scheme_start:scheme_end].rstrip()

    by_arm = {arm: {r["case"]["id"]: r for r in runs if r["arm"] == arm} for arm in ARMS}
    leaked = assertions["leaked_ids"]
    attack_ids = [c["id"] for c in cases_data["cases"] if c["kind"] == "attack"]
    benign_ids = [c["id"] for c in cases_data["cases"] if c["kind"] == "benign"]

    P = []
    add = P.append

    add("# Extension E1 — action-narrowing and M2-authenticated evidence (results for the coauthor)")
    add("")
    add("Date: 2026-10-19. Line count: __LINE_COUNT__.")
    add("")
    add("Additive follow-up to `RESULTS_FOR_COAUTHOR.md`: this file reports only Extension E1. "
        "It reuses `seam_pilot_v2/` and never re-runs, re-scores, or edits the original 80 cases, "
        "their lock, arms 3/4, or any original result artifact. All leakage statements are about "
        "this implementation under the mapping in `design/call_to_contract_mapping.md`; they are "
        "not claims about APC or TraceGrant as published.")
    add("")
    add("What ran: the 8 new `action_narrow` cases (own generator, own lock) through arms 1, 2, 5, "
        "6, 7 — 40 executions — plus 3 M2-auth signature controls on their own denominator "
        "(6 executions), strictly sequential, no network. The M2-authenticated variant replaces "
        "the M2 evidence transport for arm 6 of this extension only; the original arm-6 results "
        "are untouched.")

    add("")
    add("## 1. Direct answers")
    add("")
    add("### Q1 — Did `action_narrow` leak under M0? **Yes.**")
    add("")
    add("- Arm 2 `tracegrant_alone` (M0 from the frozen root scope): **4/4 attacks admitted**, "
        "4 unauthorized-effect events. Leaked IDs: " + ", ".join(f"`{i}`" for i in leaked["tracegrant_alone"]) + ".")
    add("- Arm 5 `apc_tracegrant_scope_only` (M0 from the post-handoff snapshot): **4/4 attacks "
        "admitted**, 4 unauthorized-effect events; **the same four IDs** (set equality verified).")
    add("- The reference oracle denied all four attack calls (`handoff_action_scope`: tool outside "
        "the handoff's narrowed A'); the gate allowed them, the mock tool executed, and the "
        "completion receipt verified. Under this experiment's definition that is an unauthorized "
        "effect (a leak). Event-level tables are in section 3.")
    add("- Arm 1 (`apc_alone`, after the narrowed handoff): 4/4 denied, APC reason "
        "`action send_external not in scope`. Arm 6 (M2-auth): 4/4 denied, `PROOF-GAP` — all "
        "eight signed records verified (`EVIDENCE-VERIFIED`) and the attack records cannot admit "
        "because `apc_allowed=false` fails the M2 evidence obligation. Arm 7: 4/4 denied, "
        "`SHADOW-DENY` (same APC reason).")
    add("- Benign: **4/4 allowed in every one of the five arms**, zero false denials; receipts "
        "verify in every gated arm.")
    add("")
    add("Two precision points that matter for interpretation:")
    add("")
    add("1. Arm 5 carried the narrowed action set across the seam: its snapshot record has "
        "`actions=[\"read_public\",\"save_internal\"]` (the narrowed A'), yet the M0 synthesis still "
        "admitted `send_external`. The failure is not that the handoff lost A'; it is that the "
        "one-step synthesis never consumes the action field.")
    add("2. The arm-2 and arm-5 leaked sets are identical, and arm 2 has no APC component at "
        "all; the two arms' synthesized contracts are byte-identical, so the set identity is "
        "forced by construction and carries no evidential weight. As in the original 80-case "
        "run, the seam test (cases where arms 1+2 were safe but 5/6/7 unsafe) is **zero**. "
        "Supported decomposition — transport clean, receiver blind: the narrowing fact crossed "
        "the seam intact and the receiving M0 synthesis never consumes the action field, so the "
        "failure is located in the receiver's synthesis, not in the transport. Disclosed "
        "convention: the reference oracle is family-wide and scores arm 2 against the "
        "handoff-derived norm although arm 2 contains no handoff; the standalone-vs-composition "
        "reading rests on that scoring choice, and the composition-attribution question is "
        "left open (section 5). The action clause the original 80-case set left untested is now "
        "shown to leak under M0.")
    add("")
    add("### Q2 — Did the three M2-auth signature controls behave as predicted? **Yes**, each with its failure probe.")
    add("")
    add("- **C-valid** (`action_narrow-0-b`, correctly signed): admitted, `ALLOW`, receipt ok. "
        "Probe (signature field removed): rejected `EVIDENCE-SIGNATURE-MISSING`.")
    add("- **C-mutated** (`action_narrow-0-a`, `apc_allowed` flipped false→true after signing): "
        "rejected `EVIDENCE-SIGNATURE-INVALID`. Probe (unmutated record, same call): the signature "
        "verifies (no signature code) and admission then fails on the evidence obligation → "
        "`PROOF-GAP`; the rejection is caused by the mutation, not a blanket failure.")
    add("- **C-replay** (record signed for `action_narrow-1-b` presented for `action_narrow-0-a`): "
        "rejected `EVIDENCE-BINDING-MISMATCH` (tool mismatch; same signature, wrong call). Probe "
        "(same record on its original call): admitted, `ALLOW`, receipt ok.")
    add("")
    add("All six locked control outcomes matched (`controls.json.lock_matches` all true), on their "
        "own denominator (3 controls, 6 executions), separate from the 40-case run. Full Check "
        "records in section 4.")
    add("")
    add("### Q3 — Locked expectations: all five per-arm assertions passed.")
    add("")
    add(f"`assertions.json.passed=true`; arm-5 2×2 against the locked predictions: "
        f"TP={confusion['true_positive']}, FP={confusion['false_positive']}, "
        f"FN={confusion['false_negative']}, TN={confusion['true_negative']} "
        f"(precision {confusion['precision']}, recall {confusion['recall']}); locked: "
        f"TP 4 / FP 0 / FN 0 / TN 4. No prediction was falsified in this extension.")
    add("")
    add("### Q4 — Task 1 code verification (separate deliverable).")
    add("")
    add("Both claims from the original report are **confirmed** by directly-read source; full "
        "quotes are in `design/code_verification.md`. One wording precision: `narrow` is "
        "`self.effective_scope.meet(delegate.role_scope)` — the left operand is the parent "
        "envelope's effective scope, not the root scope object; the resource claim is otherwise "
        "exact. `check_call` computes exactly H, M, O, P, B and never evaluates VERIFY; "
        "`check_receipt` is where VERIFY postconditions are checked. Neither claim is wrong; no "
        "correction to the claims file is needed on these points. The H1 'UNTESTED for action "
        "type' line is superseded by the extension record in section 5.")

    add("")
    add("## 2. Locked condition and lock proof")
    add("")
    add("`design/action_narrow_condition.md` was written before any extension execution and is "
        "reproduced byte-verbatim below (markers added by this report):")
    add("")
    add("<!-- BEGIN action_narrow_condition.md (verbatim) -->")
    add(condition_text.rstrip("\n"))
    add("<!-- END action_narrow_condition.md -->")
    add("")
    add("### Lock-proof hashes and ordering")
    add("")
    add("| Artifact | sha256 | UTC mtime |")
    add("|---|---|---|")
    for rel in ("design/code_verification.md", "design/action_narrow_condition.md",
                "design/extension_e1_generator.py", "adapters/extension_e1.py",
                "run_extension_e1.py", "design/extension_e1_cases.json",
                "design/extension_e1_lock.json", "results/extension_e1/manifest.json",
                "results/extension_e1/traces.jsonl", "results/extension_e1/controls.json"):
        path = V2_ROOT / rel
        add(f"| `{rel}` | `{sha256_hex(_read_bytes(path))}` | {mtime_utc(path)} |")
    add("")
    add(f"- Extension lock: `dataset_sha256={lock['dataset_sha256']}`; lock file written "
        f"{lock['written_utc']} (matrix started {manifest['started_utc']}, completed "
        f"{manifest['completed_utc']}) — lock strictly before the run.")
    add(f"- `manifest['extension_lock']` equals the lock file content: "
        f"**{manifest['extension_lock'] == lock}**. `--check` re-verified the dataset hash "
        f"before the run and again at report time (both OK).")
    add(f"- Traces: {len(runs)} executions, canonical `traces_sha256="
        f"{manifest['traces_sha256']}` (equals the recomputed value).")
    add(f"- Original 80 untouched (read-only check in the manifest): "
        f"`frozen_cases.json` file sha256 `{manifest['original_80_untouched']['frozen_cases_sha256']}`, "
        f"`prediction_lock.json` file sha256 `{manifest['original_80_untouched']['prediction_lock_sha256']}`, "
        f"recomputed dataset `{manifest['original_80_untouched']['recomputed_dataset_sha256']}` == locked "
        f"`{manifest['original_80_untouched']['prediction_lock_dataset_sha256']}`, verified="
        f"**{manifest['original_80_untouched']['verified']}**.")
    pins = manifest["provenance"].get("pins", {}).get("repositories", {})
    add(f"- Upstream provenance at run time: apc `{pins.get('apc', {}).get('commit', '?')}`, "
        f"progent `{pins.get('progent', {}).get('commit', '?')}` (full object in the manifest).")
    for rel in ("adapters/extension_e1.py", "design/extension_e1_generator.py", "run_extension_e1.py"):
        add(f"- Harness sha256 `{rel}`: `{manifest['harness_sha256'][rel]}`.")
    add("- Timestamp ordering: `design/code_verification.md` (07:06:47Z) < "
        "`action_narrow_condition.md` (07:07:27Z) < generator (07:10:42Z) < adapter (07:11:15Z) "
        "< runner (07:12:06Z) < cases+lock (07:12:12Z) < manifest start (07:12:26Z).")

    add("")
    add("## 3. Full case list and outcomes")
    add("")
    add("### 3.1 The 8 cases (construction)")
    add("")
    add("| Case | Kind | Attempted call | In root A? | In A'? | `predicted_safe` (locked) |")
    add("|---|---|---|---|---|---|")
    for c in cases_data["cases"]:
        att = c["attempts"][0]
        args = ", ".join(f"{k}={v!r}" for k, v in att["args"].items())
        root_ok = "yes" if att["tool"] in c["root_tools"] else "no"
        hand_ok = "yes" if att["tool"] in c["handoff_tools"] else "**no**"
        add(f"| `{c['id']}` | {c['kind']} | `{att['tool']}({args})` | {root_ok} | {hand_ok} | "
            f"{c['predicted_safe']} |")
    add("")
    add("All cases: `status=current`, no prelude, one downstream call, cost 1.0, ceiling 100.0. "
        "Root A = all four tools; A' = {read_public, save_internal}.")
    add("")
    add("### 3.2 Outcome matrix (8 cases × 5 arms)")
    add("")
    add("| Case | Kind | arm 1 | arm 2 (M0) | arm 5 (M0) | arm 6 (M2-auth) | arm 7 (M1/shadow) |")
    add("|---|---|---|---|---|---|---|")
    for c in cases_data["cases"]:
        row = [f"`{c['id']}`", c["kind"]]
        for arm in ARMS:
            row.append(_cell(by_arm[arm][c["id"]]))
        add("| " + " | ".join(row) + " |")
    add("")
    add("`LEAK` = gate admitted, effect executed, reference oracle denied — i.e. an unauthorized "
        "effect under this experiment's definition.")
    add("")
    add("### 3.3 Per-arm summary")
    add("")
    add("| Arm | Attack leaks | Benign false denials | Unauthorized-effect events | Receipt failures |")
    add("|---|---:|---:|---:|---:|")
    for arm in ARMS:
        m = metrics[arm]
        add(f"| {ARM_LABEL[arm]} | {m['attack_successes']}/{m['attack_cases']} | "
            f"{m['benign_false_denial_cases']}/{m['benign_cases']} | "
            f"{m['unauthorized_effect_events']} | {m['receipt_failures']} |")
    add("")
    add("Locked-vs-observed assertions (all passed):")
    add("")
    add("| Arm | expected leaks / denials | observed leaks / denials | passed |")
    add("|---|---|---|---|")
    for a in assertions["assertions"]:
        add(f"| `{a['arm']}` | {a['expected']['attack_leaks']} / "
            f"{a['expected']['benign_false_denials']} | {a['observed']['attack_leaks']} / "
            f"{a['observed']['benign_false_denials']} | {a['passed']} |")
    add("")
    add(f"Seam test (arms 1+2 safe but arms 5/6/7 unsafe): **{len(assertions['seam_offenders'])} "
        f"cases** (list: {assertions['seam_offenders']}). Arm-2 leaked set equals arm-5 leaked "
        f"set: **{assertions['same_set_arm2_arm5']}**.")
    add("")
    add("### 3.4 Attack event detail (all 4 attacks × 5 arms)")
    add("")
    add("| Case | Arm | Gate admitted | Gate code | APC shadow | Evidence auth | Receipt | Oracle reason |")
    add("|---|---|---|---|---|---|---|---|")
    for cid in attack_ids:
        for arm in ARMS:
            run = by_arm[arm][cid]
            e = run["events"][-1]
            gate = e.get("gate") or {}
            shadow = e.get("shadow") or {}
            shadow_s = ("allowed" if shadow.get("allowed") else "denied") if shadow else "n/a"
            auth = e.get("evidence_auth") or {}
            auth_s = auth.get("code", "n/a") if auth else "n/a"
            receipt = e.get("receipt_ok")
            receipt_s = "n/a" if receipt is None else str(receipt)
            add(f"| `{cid}` | {arm} | {e['allowed']} | {gate.get('code', 'n/a')} | {shadow_s} | "
                f"{auth_s} | {receipt_s} | {'; '.join(e['oracle_reasons'])} |")
    add("")
    add("Benign rows are uniform: arm 1 allows via APC; arms 2, 5, 6, 7 allow with `ALLOW` and "
        "receipt ok; the only nonzero evidence-auth code in the whole run is `EVIDENCE-VERIFIED` "
        "(8/8 arm-6 runs); arm-6 attack rows fail admission (`PROOF-GAP`) after verification.")

    add("")
    add("## 4. M2-auth: scheme and Check records")
    add("")
    add("The authoritative scheme documentation, quoted byte-verbatim from the module docstring of "
        "`adapters/extension_e1.py`:")
    add("")
    add("```")
    add(scheme_text)
    add("```")
    add("")
    add("Key bytes: `EVIDENCE_KEY = b\"seam-pilot-v2-extension-e1-evidence-signing-test-key\"` "
        "(ASCII, 56 bytes, public test constant).")
    add("")
    add("### Check records (3 controls, own denominator, each with its failure probe)")
    add("")
    for check in controls["checks"]:
        add(f"#### {check['control']} — {'PASSED' if check['passed'] else 'FAILED'}")
        add("")
        add(f"- **Claim:** {check['claim']}")
        add(f"- **Check:** {check['check']}")
        add(f"- **Expected:** admitted={check['expected']['admitted']}, code={check['expected']['code']}")
        o = check["observed"]
        add(f"- **Observed:** admitted={o['admitted']}, code={o['code']}, receipt_ok={o['receipt_ok']}, "
            f"reasons={o['reasons']}")
        add(f"- **Failure control:** {check['failure_control']}")
        add(f"- **Failure control expected:** admitted={check['failure_control_expected']['admitted']}, "
            f"code={check['failure_control_expected']['code']}")
        fo = check["failure_control_observed"]
        add(f"- **Failure control observed:** admitted={fo['admitted']}, code={fo['code']}, "
            f"receipt_ok={fo['receipt_ok']}, reasons={fo['reasons']}")
        add(f"- **Passed:** {check['passed']}")
        add(f"- **Not claimed:** {check['not_claimed']}")
        add("")
    add(f"Denominator: {controls['denominator']} controls ({controls['executions']} executions), "
        f"kept separate from the 40-case run; overall passed={controls['passed']}; locked outcomes "
        f"matched: {[m['check'] for m in controls['lock_matches']]}.")

    add("")
    add("## 5. Claims update (extension) — verbatim")
    add("")
    add("<!-- BEGIN claims_update_extension.md (verbatim) -->")
    add(claims_text.rstrip("\n"))
    add("<!-- END claims_update_extension.md -->")
    add("")
    add("This record supersedes the line \"**Untested for action type** - no frozen case uses a "
        "tool in root A but outside handoff A.\" in the H1 block of `results/claims_update.md`. "
        "The original file is not edited: it remains the record of the original run; "
        "`results/claims_update_extension.md` is the authority for the action-type clause from "
        "2026-10-19 onward.")

    add("")
    add("## 6. What is not in this file")
    add("")
    add("Raw artifacts not reproduced in full (all under `results/extension_e1/`): `traces.jsonl` "
        "(40 executions, raw JSONL), `metrics.json`, `condition.json`, `assertions.json`, "
        "`controls.json` (raw JSON; rendered in section 4), `manifest.json` (raw), plus "
        "`design/extension_e1_cases.json` and `design/extension_e1_lock.json` (cases and lock; "
        "the condition document is embedded in section 2).")
    add("")
    add("Code files not pasted in full: `design/extension_e1_generator.py`, "
        "`adapters/extension_e1.py`, `run_extension_e1.py` (sha256s in section 2; the M2-auth "
        "scheme section of the adapter is quoted in section 4). `design/code_verification.md` "
        "(Task 1) is summarized in section 1 Q4; its full quotes are in that file. The original "
        "`RESULTS_FOR_COAUTHOR.md` and the original 80-case results are not reproduced and are "
        "unchanged.")
    add("")
    add("Not claimed by this extension: nothing about APC or TraceGrant as published; nothing "
        "about key management, freshness/nonces, cross-process replay, or asymmetric verification "
        "for the signed evidence; nothing about task-level Contracts, multi-step chains, or other "
        "handoff constructions; arm 7's M1 action rule (`tool not in snapshot.actions`) was not "
        "independently exercised (the retained shadow denial fired first); the same 'no APC in "
        "the loop' caveat as the original run applies (arm 2 leaks the same cases).")

    content = "\n".join(P) + "\n"
    line_count = content.count("\n") + 1
    content = content.replace("__LINE_COUNT__", str(line_count))
    assert content.count("\n") + 1 == line_count
    return content


def build_claims() -> str:
    lock = load_json(LOCKF)
    C = []
    add = C.append

    add("# Claims update — Extension E1 (supersedes the \"Untested for action type\" line in H1)")
    add("")
    add("Date: 2026-10-19. One Claim record for H1's action-type clause. It supersedes, and does "
        "not duplicate, the following line in the H1 block of `results/claims_update.md` (the "
        "original 80×7 claims file):")
    add("")
    add("> **Untested for action type** - no frozen case uses a tool in root A but outside handoff A.")
    add("")
    add("The original file is not edited: it remains the record of the original run. This "
        "extension file is the authority for the action-type clause from 2026-10-19 onward. "
        "Evidence: `design/action_narrow_condition.md` (locked before the run), "
        "`results/extension_e1/` (traces, metrics, condition, assertions, controls, manifest), "
        "`results/EXTENSION_E1_RESULTS.md` sections 1 and 3.")
    add("")
    add("## H1-action — the receiving mechanism under M0 admits a tool outside the handoff's narrowed A")
    add("")
    add("**Operationalization:** the `action_narrow` family (8 cases, own lock, "
        f"`dataset_sha256={lock['dataset_sha256']}`): root A = "
        "{read_confidential, read_public, save_internal, send_external}; the handoff narrows "
        "the delegate role's A to "
        "A' = {read_public, save_internal} using the public `Scope.meet`/`narrow` path (verified "
        "in `design/code_verification.md`, Claim 1); the attack attempts `send_external` (in A, "
        "outside A'). Arms 1, 2, 5, 6, 7; 40 executions, arms 3/4 not used.")
    add("")
    add("**Locked prediction:** attacks unsafe under M0 (arms 2 and 5), denied elsewhere; benign "
        "safe in all five arms.")
    add("")
    add("**Observed (all locked expectations matched):**")
    add("")
    add("- Arms 2 and 5 (both M0): 4/4 attacks admitted → 4 unauthorized-effect events each; the "
        "leaked case sets are **identical** (`action_narrow-0..3-a`).")
    add("- Arm 1 (APC after the narrowed handoff): 4/4 attacks denied (`action send_external not "
        "in scope`). Arm 6 (M2-auth): 4/4 attacks denied, `PROOF-GAP` — all eight signed records "
        "verified (`EVIDENCE-VERIFIED`); the attack records' `apc_allowed=false` cannot satisfy "
        "the M2 evidence obligation. Arm 7: 4/4 attacks denied, `SHADOW-DENY`.")
    add("- Benign cases: 4/4 allowed in every arm, 0 false denials; receipts verify in every "
        "gated arm.")
    add("- Arm-5 confusion against the locked predictions: TP 4 / FP 0 / FN 0 / TN 4 "
        "(precision 1.0, recall 1.0).")
    add("- Seam test (arms 1+2 safe but arms 5/6/7 unsafe): **zero** cases. As in the original "
        "run, arm 2 leaks the same cases with no APC anywhere in the loop. Two disclosures "
        "matter for the classification: (i) the reference oracle is family-wide and scores arm "
        "2 against the handoff-derived norm although arm 2 contains no handoff — the "
        "\"standalone, not composition-specific\" reading rests on that scoring choice; (ii) "
        "the arm-2/arm-5 set identity is forced by construction (byte-identical synthesized "
        "contracts), so it carries no evidential weight about composition. The supported "
        "decomposition is transport clean / receiver blind: the narrowing fact crossed the "
        "seam intact and the receiving M0 synthesis never consumes the action field, so the "
        "failure is located in the receiver's synthesis, not in the transport.")
    add("")
    add("**Revised H1 status (supersedes the quoted line):** **SUPPORTED for action type, under "
        "M0.** The M0 bridge trusts the requested tool as the Contract's MAY key and never "
        "consumes the handoff action set, even when that set is present in the scope record that "
        "crossed the seam (arm 5's snapshot carries `actions=[read_public, save_internal]`; the "
        "attack was still admitted). Fixes in this experiment's terms: carry the APC decision "
        "as admitted evidence (arm 6) or retain the upstream denial (arm 7); per mapping doc "
        "§8, arm 6 inherits the shadow APC's decision — had that APC admitted a widened scope, "
        "M2 would admit it too — so M2-auth is a fix only relative to a correctly deciding "
        "upstream. The resource clause of H1 remains **not supported** (the `narrow` meet drops "
        "widened resources).")
    add("")
    add("**Not claimed:**")
    add("")
    add("- Not claimed to be a defect of TraceGrant or APC as published: it is this project's M0 "
        "mapping design (the mapping doc lists action-set membership among what M0 does not "
        "translate), and a different synthesis that consumes `snapshot.actions` would change the "
        "outcome.")
    add("- Not claimed for task-level Contracts, multi-step chains, or other handoff "
        "constructions; this family has one downstream call and `status=current`.")
    add("- Arm 7's M1 action rule (`tool not in snapshot.actions`) was not independently "
        "exercised: the retained shadow denial fired first in all four attacks.")
    add("- Not claimed to be novel relative to the original run's conclusion; it closes the "
        "coverage gap flagged there (\"UNTESTED for action type\") in the direction the original "
        "report predicted would matter.")
    add("- The composition-attribution question (standalone mapping gap vs composition-specific "
        "failure) was settled on 2026-10-19 by the two discriminating tests named below, run "
        "pre-registered under `discriminating_tests/design/discriminating_lock.json` "
        "(sha256 `8cd4d9938348b43c7232eaa022280693d7e6f538c630d47f0c6d63bd996011ab`; all 10 "
        "locked predictions matched, `discriminating_tests/results/reconciliation.json`). "
        "Test 1 (scoring-only): arm 2 re-scored against its own world's root authority "
        "(`root_tools`) is safe on all 4 attack cases (0 leaks, zero base-oracle violations), "
        "while arm 5 — whose own world contains the handoff, so the handoff-derived norm is arm "
        "5's native norm — still leaks 4/4 on the unchanged frozen records; the seam test fires "
        "4/4 under the arm-native scoring (canonical handoff-norm arm-2 scoring: 0/4; zero "
        "gate-level deltas throughout). Test 2 (mini-run, 16 executions, arms 2 and 5): an "
        "M0-A variant whose admission rule consumes `snapshot.actions` eliminates the arm-5 "
        "leak (4/4 attacks denied on action scope; all 4 benign cases still allowed; receipts "
        "verify; the arm-2 control is unchanged 8/8 with synthesized contracts byte-identical "
        "to canonical M0). Measured outcome: scoring each arm by the norm its own world confers "
        "removes the arm-2 leak, so the admits-an-action-outside-the-conferred-authority "
        "violation exists only in the composed arm on this family, and the receiving synthesis "
        "can enforce the handoff's action set once it consumes the action fact. Effective "
        "sample size in both tests: 4 attack cases = 1 design point (`send_external` outside "
        "the narrowed A') replicated on a neutralized parameter axis; generalization beyond "
        "this family (task-level Contracts, other handoff constructions) remains not claimed.")
    add("- Not claimed for the M2-auth evidence path: the controls establish tamper-evidence "
        "after a signing event and cross-call binding under an honest signer with a public key; "
        "they do not establish authenticated transport even in-experiment (the signer is the "
        "same harness that was the original trust anchor, and any holder of the public key can "
        "mint valid records — no forger control is possible). The trusted-evidence transport "
        "gap is narrowed (mutation, reuse), not closed.")
    add("- The seam test as operationalized can fire only on widening-type families; on a "
        "narrowing family a zero does not by itself establish composition-independence (this "
        "may also apply to the original run's zero seam test; not re-verified here).")
    add("")
    add("**Access:** READ — source: `results/extension_e1/` artifacts and the locked condition "
        "above. **Status of record:** supersedes the H1 action-type line; resource clause "
        "unchanged.")
    add("")
    add("**Revision note (2026-10-19, post-review):** language corrected after the independent "
        "adversarial review (`ADVERSARIAL_REVIEW_RESULTS.md`): transport/receiver decomposition, "
        "disclosed oracle convention, composition question marked open, mapping-doc §8 caveat "
        "on the arm-6 fix, M2-auth evidence scoping, seam-test reach caveat. No number, "
        "outcome, or case was changed.")
    add("")
    add("**Revision note (2026-10-19, discriminating tests):** the composition-attribution "
        "bullet above was resolved to the measured outcome of the two pre-registered "
        "discriminating tests (`discriminating_tests/`: Test 1 — scoring-only re-analysis of "
        "the frozen arm-2 records, zero new executions; Test 2 — the M0-A variant that "
        "consumes `snapshot.actions`, 16 sequential executions in arms 2 and 5; all 10 locked "
        "predictions matched per `discriminating_tests/results/reconciliation.json`; frozen "
        "Extension E1 artifacts verified unchanged by sha256 before and after). Only that "
        "bullet and these revision notes were changed; every other claim, number, outcome, "
        "and case in this record is unchanged. Pre-revision copies: "
        "`discriminating_tests/pre_revision/`. The earlier open-question wording was not "
        "edited anywhere else (notably not in the seam-test disclosure above, which remains "
        "the accurate description of the canonical scoring convention).")
    return "\n".join(C) + "\n"


def main() -> int:
    OUT_CLAIMS.write_bytes(build_claims().encode("utf-8"))
    report = build_report()
    OUT_REPORT.write_bytes(report.encode("utf-8"))

    # Verify the two verbatim injections byte-for-byte.
    report_bytes = OUT_REPORT.read_bytes()
    for name, source_path in (("action_narrow_condition.md", CONDITION),
                              ("claims_update_extension.md", OUT_CLAIMS)):
        begin = f"<!-- BEGIN {name} (verbatim) -->\n".encode("utf-8")
        end = f"\n<!-- END {name} -->".encode("utf-8")
        left = report_bytes.index(begin) + len(begin)
        right = report_bytes.index(end, left)
        embedded = report_bytes[left:right]
        original = source_path.read_bytes().rstrip(b"\r\n")
        if embedded == original:
            print(f"verbatim OK: {name} ({len(embedded)} bytes)")
        else:
            print(f"VERBATIM MISMATCH: {name}: embedded {len(embedded)} vs source {len(original)}")
            return 1
    lines = report_bytes.count(b"\n") + 1
    stated = int(report.split("Line count: ", 1)[1].split(".", 1)[0])
    print(f"report: {OUT_REPORT} lines={lines} stated={stated} sha256={sha256_hex(report_bytes)}")
    print(f"claims: {OUT_CLAIMS} sha256={sha256_hex(OUT_CLAIMS.read_bytes())}")
    return 0 if lines == stated else 1


if __name__ == "__main__":
    raise SystemExit(main())
