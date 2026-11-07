# Consolidated claim set — seam paper (item 4)

**Date:** 19 Oct 2026. **Status:** consolidated; QA corrections applied; independent second QA passed 19 Oct (`paper\consolidation_second_qa.md`, PASS WITH NOTES, two INFO citations — row 17 annotated report-only, rows 21–23 re-cited to `test1_rescored_arm2.json`); SA adversarial review merged 19 Oct (NON-BLOCKING; wording corrections applied at source). **FROZEN 19 Oct 2026 as the paper-facing claim set — see the freeze record below.** **Scope:** one defensible claim set (H1–H7, the cross-cutting ★ finding, and the formal core) drawn from the four experiment claim files and the formal-core draft. No new experiments, no re-scoring, no edits to frozen artifacts. Every number below is traced to its source artifact in §6 (source map: frozen input, run output, or report).

**Supersession:** this file supersedes the claim ladder in `paper\Paper_Claims_and_Takeaways.md` (kept as the pre-consolidation ladder). The experiment claim files remain the authority for their own runs; this file is the unified, consolidated authority for paper-facing language.

**Freeze record (19 Oct 2026).** The SA adversarial review (`tests\seam_pilot_sentinelagent\results\ADVERSARIAL_REVIEW.md`, GLM-5.3-Flash Free, NON-BLOCKING; 1 MAJOR wording + 4 MINOR + 4 INFO) is merged. The review's SA-1 correction plus the SA-3/SA-4/SA-9 presentational fixes were applied at the source (`tests\seam_pilot_sentinelagent\sa_reports.py`) and the SA pair reports regenerated — numbers unchanged; run-artifact hashes unchanged; 11/11 frozen inputs re-verified (pre-revision copies: `tests\seam_pilot_sentinelagent\review_revision_2026-10-19\`; details: `paper\consolidation_reconciliation.md` §H). **Revision 1 (19 Oct 2026):** the reviewer's JSON summary was delivered and validated — `tests\seam_pilot_sentinelagent\results\adversarial_review.json`, 30,531 bytes, sha256 `5db74a0c…`; parses; `ok: true`; 12 claims / 9 findings; `no_frozen_edits: true`; hashes 11/11 — the open record-keeping item is closed (§H, H3). After this merge the claim set is frozen; no text change without a new dated revision. No frozen artifact changed.

---

## 0. Conventions and reading rules (apply to every section below)

1. **Absolute + delta.** Whenever a count includes a pre-existing baseline, both are stated (e.g. boundary arm 5 = 32 leak cases / 34 unauthorized-effect events = 28 pre-existing canonical + 4 new).
2. **Effective sample size** is stated next to every witness set.
3. **Forced identities** are labeled *forced*, never evidence (SA arm 2 ≡ arm 5 leak sets by construction; boundary arm 2v ≡ arm 5 per variant by construction).
4. **Every classification names its scoring convention** (frozen family-wide; arm-native; boundary canonical/variant-manifest; SA arm-invariant).
5. **Conditional language only.** No "seams are safe", "seams fail generally", "always", "never" without a stated condition. The zero-seam result is **bridge-conditioned**: it holds for narrowing-preserving mappings (canonical T0) on the frozen case sets.
6. **Status vocabulary:** `SUPPORTED`, `REFINED`, `UNTESTED`, `NOT CLAIMED`, `REFUTED`. (The token `REFUNDED` in the boundary claims file is a typo; see `paper\consolidation_reconciliation.md` item B6.)

---

## 1. Evidence base

| # | Experiment | Scale (runs) | Effective witness structure | Artifact root |
|---|---|---|---|---|
| 1 | Pilot 1 — APC → TraceGrant (v2) | 80 cases × 7 arms = **560** executions; 40 attack cases | 10 templates × 8 runs (4 attack + 4 benign); **6 leak templates × 4 parameters = 24/40** leaks | `tests\seam_pilot_v2\results\` (`claims_update.md`, `raw_metrics.json`, `manifest.json`) |
| 2 | Extension E1 — action-narrowing + M2-auth | 8 cases × 5 arms = **40** executions + **6** control executions | 1 design point × 4 attack cases (`send_external` outside narrowed A′) replicated on a neutralized parameter axis | `tests\seam_pilot_v2\results\extension_e1\` + `EXTENSION_E1_RESULTS.md` |
| 3 | Discriminating tests (E1 composition attribution) | Test 1: 0 new executions (scoring-only); Test 2: **16** executions | 4 attack cases = 1 design point × 4; 10 locked predictions, all matched | `tests\seam_pilot_v2\discriminating_tests\results\` (`REPORT.md`, `reconciliation.json`) |
| 4 | SentinelAgent pair — APC → SentinelAgent | 96 cases × 7 arms = **672** executions; 48 attack cases | 12 templates × 8 runs; **7 leak templates × 4 parameters = 28/48** leaks | `tests\seam_pilot_sentinelagent\results\` (`SA_RESULTS.md`, `claims_update_sentinelagent.md`, `results\sa\`) |
| 5 | Boundary — V1/V2 manifest derivation | **1,152** runs = 6 arms × 2 variants × 96 cases; 96 rows per cell | V1: 1 design point × 4 cases (`resource_widen-0-a..3-a`); V2: 1 design point × 4 cases (`omitted_forbidden_default-0-a..3-a`); 2 design points total | `tests\seam_pilot_sa_boundary\results\boundary\` (`metrics.json`, `manifest.json`, `reconciliation.json`, `self_review.json`) |

Frozen inputs were hashed before and after this consolidation; see `paper\consolidation_self_review.json` (`no_frozen_edits`, nine inputs). The QA pass re-checked the item-3 hashes (discriminating lock, `REPORT.md`, `claims_update_extension.md`) and found them unchanged.

---

## 2. Claim ladder

### H1 — Trusted-request laundering / scope trust

**Claim (plain language).** At a cross-mechanism handoff the receiving mechanism re-derives scope, or trusts the already-authorized caller, in a way that can admit a call the upstream narrowing did not confer. The gap is not that the record is unfaithful but that a faithful scope record cannot carry, and the receiver cannot derive, an authorization decision.

**Operationalization.** (a) Pilot 1 scope-only handoff uses the attempted tool as the MAY key and derives resource choices from handoff scope; attacks widen action or resource. (b) E1 `action_narrow` family: root A = {read_confidential, read_public, save_internal, send_external}; handoff A′ = {read_public, save_internal}; attack attempts `send_external`. (c) Boundary V1/V2: bridge mints the token from a variant-derived manifest (role scope exceeding root R; default-filled SEND endpoint) and the receiver treats the signed manifest as authority.

**Observed.**
- Resources: all seven Pilot 1 arms deny the four `resource_widen` cases (`narrow` meets R); the resource clause of H1 is **not supported** (`tests\seam_pilot_v2\results\raw_metrics.json`: `per_template.resource_widen.leaked = 0` for `tracegrant_alone`).
- Action type: E1 arms 2 and 5 (both M0) admit **4/4** attacks each, **4 unauthorized-effect events** each, identical case sets (`action_narrow-0..3-a`); arm 1 (APC after narrowed handoff) denies 4/4 (`action send_external not in scope`); arm 6 (M2-auth) denies 4/4 (`PROOF-GAP`, all eight signed records `EVIDENCE-VERIFIED`); arm 7 denies 4/4 (`SHADOW-DENY`); benign 4/4 allowed in every arm, 0 false denials; arm-5 confusion TP 4 / FP 0 / FN 0 / TN 4 (precision 1.0, recall 1.0) (`tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.2–§3.3; `results\extension_e1\assertions.json`).
- Discriminating tests (E1): Test 1 re-scores arm 2 against its own world's root authority (`root_tools`) → **0/4** leaks; seam test fires **4/4** under arm-native scoring (0 under canonical). Test 2 (M0-A, 16 executions) denies the 4 attacks on action scope (`ACTION-SCOPE`), allows 4/4 benign, 12/12 receipts verify, arm-2 control parity 8/8, contract digests byte-identical 8/8 (`tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §§1–3; `reconciliation.json`, all 10 predictions matched).
- Bridge derivation: boundary V1 admits the widened resource `docs:external/secret` in arm 5 **and** standalone arm 2v (4 cases); V2 admits the default-filled send to `forbidden-default@example.test` in arm 5 **and** standalone arm 2v (4 cases); canonical arm 2 is safe on those 4; arms 6/7 suppress (APC-DENY / SHADOW-DENY ×4 per variant) (`tests\seam_pilot_sa_boundary\results\boundary\metrics.json`: `apc_sentinelagent_scope_only::*` `attack_successes = 32`; `sentinelagent_alone_variant::*` `attack_successes = 32`; `sentinelagent_alone::*` `attack_successes = 28`).

**Status:** `REFINED` — supported for the action clause under M0; not supported for the resource clause; extended to the bridge's manifest derivation (V1/V2).

**Conditions / conventions.** M0 is this project's one-step mapping, not a defect of APC or TraceGrant as published. The action clause holds under M0 and would change if the synthesis consumed `snapshot.actions` (measured by Test 2). The boundary clause holds for non-narrowing-preserving derivations; canonical T0 remains strict. Convention disclosure: the E1 reference oracle is family-wide and scores arm 2 against the handoff-derived norm although arm 2 contains no handoff; the standalone-vs-composition reading rests on that choice (discriminating Test 1 adopts the arm-native norm).

**Effective sample size.** E1: 1 design point × 4 cases; boundary: 1 design point × 4 cases per variant (2 design points total, 8 cases; not 8 independent); Pilot 1 resource clause: 4 cases (1 template × 4 parameters).

---

### H2 — Dynamic state, identity and freshness do not cross and leak

**Claim.** Principal/task identity, composition history, cumulative budget and replay, expiry, and revocation do not cross the seam and leak; the fix is carrying the upstream decision, not a check inside the receiver's vocabulary.

**Observed.**
- Pilot 1: arm 5 (M0) leaks **24/40** attack cases, **26 unauthorized-effect events**, 0 false denials. Classes: principal/task 4, composition history 4 (with marker-bearing external effects), repeated calls 4 cases / 6 events, budget 4, expiry 4, revocation 4. Arm 6 (M2 evidence) leaks 0/40 (`tests\seam_pilot_v2\results\raw_metrics.json`: `tracegrant_alone.attack_successes = 24`, `unauthorized_effect_events = 26`; `per_template` leaked counts; `claims_update.md` H2).
- SA pair: **24 of 28** leaks are this class (principal 4, composition 4, repeated 4 cases / 6 events, budget 4, expiry 4, revocation 4); arm 5 ≡ arm 2 (identical sets, forced by construction — same contract, not evidence); arm 6 closes all 28 with 0 leaks / 0 FD; arm 7 closes by refusing untranslatable cases (20 benign FD) (`tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §6 per-template table; `claims_update_sentinelagent.md` H2).
- Boundary: unchanged under V1/V2 — these classes leak in arms 2/2v/5 under both variants and are suppressed by arms 6/7. V1/V2 add **no new** dynamic-state leak class; their new leaks are scope/manifest derivation classes (`tests\seam_pilot_sa_boundary\results\boundary\claims_update_boundary.md` H2; `metrics.json`: `sentinelagent_alone::*` `attack_successes = 28`).

**Status:** `SUPPORTED` (second receiving mechanism; the boundary is a second bridge mapping of the same pair and adds no new class).

**Conditions / conventions.** Holds for the frozen case sets under the M0/T0 mappings. SA scoring is arm-invariant (`permitted &= role_resources`; `prohibited_composition` applied to arm 2); rescoping it would flip `composition_history_loss` arm 2 from leak to safe. This is disclosed, not hidden.

**Effective sample size.** Pilot 1: 6 leak templates × 4 parameters = 24 attack cases (of 40). SA/boundary: 7 leak templates × 4 parameters = 28 attack cases (of 48).

---

### H3 — Vocabulary mismatch is silence, not misparse

**Claim.** Mismatches between mechanism vocabularies manifest as *silence* (an unrepresentable field is never checked) rather than as a misparse, producing admitted calls with no effect-time detection.

**Observed.**
- Pilot 1: recipient-substitution and omitted-forbidden-default attacks are caught (0 leaks) by mapping-side canonicalization and BIND constraints; resource-widen is falsified by APC's scope meet; state/identity/freshness leaks persist under both root-scope and handoff-scope mappings; unsatisfiable-VERIFY is a completion-integrity boundary, not an unauthorized-effect leak (`tests\seam_pilot_v2\results\raw_metrics.json`: `per_template.recipient_substitution.leaked = 0`, `omitted_forbidden_default.leaked = 0`; `claims_update.md` H4 refinements).
- E1: transport clean / receiver blind — arm 5's snapshot carries `actions = [read_public, save_internal]` (the narrowed A′), yet M0 still admits `send_external`; the narrowing fact crossed intact and the synthesis never consumes the action field (`tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §1, precision point 1).
- Boundary: V1 mismatch is resource-scope (role scope exceeds root R); V2 mismatch is the SEND endpoint (default-filled recipient not the allowlisted snapshot recipient). Both are faithful to what the bridge wrote into the manifest (`tests\seam_pilot_sa_boundary\results\boundary\claims_update_boundary.md` H3; `metrics.json`: V1 `resource_widen` 4 leaked; V2 `omitted_forbidden_default` 4 leaked).

**Status:** `SUPPORTED` (structural; two pairs plus the E1 and boundary extensions; no shared vocabulary element for state or identity has appeared).

**Conditions / conventions.** "Silence" is defined relative to the receiver's read set (formal core §3): a fact that no decision reads constrains no decision. The boundary manifestations are bridge-design artifacts, not composition-specific failures.

**Effective sample size.** V1/V2: 1 design point × 4 cases each.

---

### H4 — No shared audit trail

**Claim.** There is no shared audit trail across mechanisms (SHA-256 evidence chain vs receipts vs hash-linked tokens).

**Observed.** Not tested in any pilot. SA tokens are one-hop (`parent_hash = ROOT`); no chain reconstruction or cross-mechanism trail interchange was exercised. Boundary: not tested (same as SA pilot).

**Status:** `UNTESTED`. Do not import adjacent findings into this claim.

**Conditions / conventions.** None yet; the next natural instrument is a case family that reconstructs authority from a token hash chain and compares it with the APC envelope's history.

**Effective sample size.** n/a (not tested).

---

### H5 — Verification gap / keyholder minting power

**Claim.** Integrity of a signed record is not the source of authority: a receiver that verifies a signature learns key possession and payload integrity, not who minted the record. Any keyholder is, to the receiver, equivalent to the issuer within the token vocabulary. The boundary experiment generalizes this to the bridge's own manifest derivation.

**Observed.**
- SA pair (first end-to-end test): a token signed with the prototype's published key constant instead of the trusted harness key is rejected `SIGNATURE_INVALID` in every token arm (foreign-key probes; controls S2-foreign, S1-failure, S2-mutated). Delegate-minted tokens are admitted exactly like bridge tokens where the prior authorization is not restored: `keyholder_plain` admitted 4/4 in all four token arms; `keyholder_widen` admitted 4/4 in arms 2/5. Control S2-two-minters returns identical codes for bridge- and delegate-attributed tokens (`tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §7 and §11; `results\sa\controls.json`, 10/10 passed).
- E1 M2-auth: signing the evidence record and verifying it before admission closes the tamper/reuse gap but not authenticated transport. Controls C-valid, C-mutated, C-replay all passed (6/6 locked outcomes) on their own denominator; the key is a public test constant and the signer is the same harness that was the original trust anchor (`tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §4; `results\extension_e1\controls.json`).
- Boundary: V1/V2 manifest derivation is enabled by the same keyholder property — a bridge holding the key can write a widened manifest (V1 role scope) or a default-filled SEND endpoint (V2) and the receiver admits it. H5 now explicitly covers keyholder minting power at the bridge/manifest-derivation layer, not only delegate-minted tokens (`tests\seam_pilot_sa_boundary\results\boundary\claims_update_boundary.md` H5).

**Status:** `REFINED` — confirmed for "cannot verify without the key"; refined for "what verification attests."

**Conditions / conventions.** One prototype, one key model, one case family. The "or a call to the DAS" alternative was not exercised end-to-end (no live DAS service in the prototype). M2-auth narrows (mutation, reuse) but does not close the transport gap.

**Effective sample size.** SA signature family: 2 pairs × 4 parameters = 8 cases (4 attack + 4 benign) × 4 token arms.

---

### H6 — Similar-pair vs dissimilar-pair failure shapes

**Claim.** APC↔SentinelAgent (chain narrowing) and APC↔TraceGrant (proof-carrying) fail differently in remediation mechanics, and composition does not add a new failure mode beyond what the receiver exhibits alone, with the measured exception of E1's action family under arm-native scoring; where the bridge is non-narrowing-preserving, the seam makes a pre-existing mapping-layer failure visible.

**Observed.**
- Pilot 1: M0 leaks 24/40 attack cases; M2 (evidence carriage) leaks 0/40; fail-closed leaks 0/40 with 20/40 benign denials. The comparison with Progent reference numbers (4/20 unauthorized effects) is directional only; denominators and mechanisms differ (`tests\seam_pilot_v2\results\claims_update.md` H6; `raw_metrics.json`).
- SA pair: leak shape nearly identical across the two pairs (dynamic state, identity, freshness dominate; arms 2/5 identical; 0 FD in standalone and scope-only arms). Pair differences appear in remediation mechanics (signed attestation vs evidence digest/receipt) and in one new standalone class, `keyholder_widen` (token-ecosystem property, not composition) (`tests\seam_pilot_sentinelagent\results\claims_update_sentinelagent.md` H6).
- Boundary: composition neither creates nor removes bridge-level failure. V1 and V2 are non-narrowing-preserving: arm 5 leaks the predicted 4 **new** cases per variant (32 total = 28 pre-existing + 4 new) while canonical arm 2 is safe on them and arms 6/7 suppress (0 leaks). Standalone arm 2v leaks the identical set per variant, so the failure is a bridge-design artifact, not composition-specific (`tests\seam_pilot_sa_boundary\results\boundary\claims_update_boundary.md` H6; `metrics.json` `sentinelagent_alone_variant::*` `attack_successes = 32`).
- E1 discriminating tests: under arm-native scoring on both arms the action-clause violation exists **only in the composed arm** (arm 1 denies, arm 2 safe after re-scoring, arm 5 leaks); the seam test fires 4/4; the mini-run eliminates the leak by making the receiver consume the fact. Under canonical (handoff-norm) scoring the same records give 0. The classification is therefore convention-dependent and is reported as measured, not fiat (`tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §§1, 4).

**Status:** `SUPPORTED` (refined by boundary and discriminating tests).

**Conditions / conventions.** "Composition-specific" is used only for E1's action family under arm-native scoring. Boundary is a "bridge-design artifact, not composition-specific" finding. Effective sample sizes as in H1.

**Effective sample size.** E1: 1 design point × 4 cases; boundary: 1 design point × 4 cases per variant.

---

### H7 — Intent layer (SentinelAgent P2)

**Claim.** The intent layer (SentinelAgent P2) may be gameable (benign-word override).

**Observed.** Not tested. P2 was out of scope in the SA pair (`intent_text` carried, never classified); E1 and boundary did not test it.

**Status:** `UNTESTED`.

**Conditions / conventions.** n/a.

**Effective sample size.** n/a (not tested).

---

### ★ — Cross-cutting finding: the seam is subtractive under narrowing-preserving mappings

**Claim (plain language).** Under narrowing-preserving mappings, the seam carries *less* context than the receiving mechanism's checks would need to detect standing authority violations on their own; composition creates no authorization failure that one of the mechanisms does not already exhibit standalone — with the measured exception of E1's action family under arm-native scoring, where the composed arm is the only one that admits. The seam generally changes which decisions are reachable; the measured exception is the case where the composed arm admits an effect the standalone receiver does not. The mechanism-specific failure faces are the receiver's vocabulary gaps (unrepresentable state: absolute and relative time, revocation, principal identity, composition history, cumulative budget, replay), and they repeat across receiving mechanisms.

**Observed.**
- Zero seam under narrowing-preserving mappings: Pilot 1 seam test 0; E1 canonical seam test 0; SA seam test 0 (`tests\seam_pilot_v2\results\raw_metrics.json` seam counts not separately stored but claims files record 0; `SA_RESULTS.md` §1: 0 seam cases; `EXTENSION_E1_RESULTS.md` §3.3: seam test 0).
- E1's action family is the one composition-specific exception *under arm-native scoring*: 4/4 (canonical scoring gives 0/4 on the same records) (`discriminating_tests\results\reconciliation.json`: P1.2 observed 4 under root-norm, 0 under canonical).
- Boundary: canonical seam test shows 4 new cases per variant (`resource_widen` / `omitted_forbidden_default`), but standalone arm 2v leaks the identical set, so these are bridge-design artifacts, not composition-specific failures (`manifest.json`: `seam_test.v1.seam_count = 4`, `seam_test.v2.seam_count = 4`; `metrics.json`: `sentinelagent_alone_variant::*` `attack_successes = 32`).
- Arm 2 ≡ arm 5 leak sets are forced by construction (SA: 28/28 identical; boundary: 32/32 identical per variant) and carry no evidential weight about composition; the informative contrasts are canonical arm 2 (safe on variant cases) vs composed variant arm 5 (leak), and arm 2v (leak) vs arm 2 (safe) for attribution.

**Status:** `SUPPORTED` (narrowing-preserving mappings; one measured arm-native exception disclosed).

**Conditions / conventions.** Holds for narrowing-preserving mappings (canonical T0) on the frozen case sets; E1's exception is convention-dependent (arm-native norms); boundary's 4 visible cases are bridge-design artifacts (arm 2v leaks identically). Effective sample sizes as in H1/H2/H6.

**Effective sample size.** E1: 1 design point × 4 cases; boundary: 1 design point × 4 cases per variant; Pilot 1/SA: case families as above (24 and 28 attack cases respectively, but seam counts are case-level, not independent design points).

---

## 3. Cross-cutting findings (detail)

1. **Zero-seam conditionality.** "Zero seam" is a property of narrowing-preserving mappings, now bounded rather than assumed. Canonical T0 preserves 0 seam on all frozen case sets; non-preserving bridges (V1/V2) leak with or without composition.
2. **E1's composition-specific exception.** On the action family, under arm-native scoring, the violation exists only in the composed arm (arm 1 denies, arm 2 safe, arm 5 leaks) and is eliminated by making the receiver consume the fact (4/4 denied, 0 false denials). Canonical scoring gives 0/4 on the same records; the difference is the scoring convention, disclosed.
3. **Boundary bridge-layer result.** A non-narrowing-preserving manifest derivation admits the widened calls standalone and composed; composition neither creates nor removes the failure. The fault is the bridge's manifest derivation; the receiver cannot recover a fact that was never narrowed.
4. **Repair patterns.** (a) Receiver side, when the fact crossed intact: carry the upstream decision as signed evidence (arm 6: 28→0 leaks in SA; E1 M2-auth 4/4 denied) or retain the upstream denial (arm 7: 0 leaks, 20 benign FD). (b) Derivation side, when the bridge widened: fix the manifest derivation at the bridge (narrowing-preserving meet). (c) Receiver-side enforcement requires consumption, not just carriage (E1 Test 2: `ACTION-SCOPE`).
5. **Keyholder finding.** Verification attests key possession and integrity, not source of authority. Any keyholder is equivalent to the issuer for the receiver; this holds for delegate-minted tokens (SA `keyholder_widen`) and for the bridge's own manifest derivation (V1/V2). Key distribution/trust is the seam's critical interface.

---

## 4. Formal core (integrated from `RPaper(user)\FORMAL_CORE_DRAFT.md`, with §4 measured)

### 4.1 Definitions
- **Call space** C: calls c = (tool, resource, arguments, …).
- **Mechanism** M = (V_M, admit_M). V_M is the vocabulary (fields M can represent and, structurally, read); admit_M(c, ρ) ∈ {allow, deny}.
- **Authority** A ⊆ C — the call set a principal confers. A sender **narrows**: A → A′ ⊆ A (scope meet ⊓).
- **Bridge (seam)** B: translation from the sender's narrowed decision + state to the receiver-side record ρ_R = B(A′, state).
- **Composition** (arms 2/5 semantics): admit_C(c) ≔ admit_R(c, B(A′)); **effective authority** A_C ≔ { c : admit_C(c) = allow }.
- **Read set** V_read ⊆ V_R: the fields the receiver's decision actually consults — not what the record *carries*, what the decision *reads*.

**Definition (narrowing-preserving, effective form).** B is narrowing-preserving on a family F iff A_C ⊆ A′ on F — the composition enforces at least the sender's narrowing. (Open definitional choice flagged, not hidden: transport-only vs effective; this draft uses the effective form, because E1 showed transport clean but effective composition not preserving.)

### 4.2 Seam-test predicate
seam(case) ≔ safe(arm 1) ∧ safe(arm 2) ∧ ¬safe(arm 5), with safe = no call outside the arm's own world's conferred authority executes. Scoring conventions are explicit per test (arm-native norms; disclosures in the artifacts). The historical "zero so far" was convention-dependent: under pre-registered arm-native norms the E1 action family fires **4/4**.

### 4.3 Blindness lemma (definitional; short proof)
**Lemma.** If admit_R depends on the call only through its read-set projection π_{V_read}(c) (state ρ included), and no value in V_read (or in ρ, as read) separates A′ from A \ A′ for a call pair, then no admission function over V_read can enforce A′ on that pair — the two sides are admitted identically.

*Proof sketch (dependency argument).* admit_R factors through π_{V_read}. Take c₁ ∈ A′, c₂ ∉ A′ with identical V_read-visible inputs. Then admit_R(c₁, ρ) = admit_R(c₂, ρ); on this pair no V_read-decision allows c₁ and denies c₂. ∎

**Corollary (the program's aphorism): carried but unread = uncarried (for decision purposes).** A fact that no decision reads constrains no decision — even when the transport was byte-perfect.

*Measured instances:* E1 action family (narrowed set crossed intact, synthesis never read it → 4/4 admitted; Test 2 made the receiver read it → 4/4 denied, 0 false denials). Pilot 1 (24/40) and SA (28 leaks): leaking classes are fields the receiver's vocabulary lacks (unrepresentable ⇒ unenforceable). Boundary (V1/V2): the widened manifest is admitted by the receiver standalone and composed — the bridge wrote the widened scope, so there is no consumption failure to repair at the receiver; the derivation is the fault.

### 4.4 Seam proposition (boundary clause now measured, not pending)
**Statement (post-boundary).** A composed-only leak requires a non-narrowing-preserving effective bridge **and** the receiver's decision to be the only thing standing between the widened call and execution. The consumption-side clause is measured (E1). The derivation-side clause is **not composition-specific**: a non-narrowing-preserving manifest derivation (V1 role-scope, V2 default-fill) makes the receiver admit the widened calls **with or without composition** — the identical set appears in standalone arm 2v. Composition neither creates nor removes the failure; it only makes it visible in the composed arms.

- **Measured — consumption side (E1):** canonical bridge not preserving on actions → composed-only witnesses; repair restored preservation → no witnesses.
- **Measured — derivation side (boundary, V1/V2):** the 4 new cases per variant leak in arm 5 **and identically in standalone arm 2v**; canonical arm 2 is safe on them; arms 6/7 suppress (APC-DENY / SHADOW-DENY ×4). Absolute counts: arm 5 = 32 cases (28 pre-existing + 4 new) / 34 events; arm 2 = 28 / 30. Effective n = 1 design point × 4 per variant. → No composition-specific failure; the fault is the bridge's manifest derivation.
- **Scope:** zero seam holds for narrowing-preserving mappings (canonical T0) on the frozen case sets; bounded, not universal. The informative contrast is canonical arm 2 (safe on variant cases) vs composed variant arm 5 (leak), with arm 2v as the attribution control.

### 4.5 Repair rule
Receiver side (when the fact crossed intact):
```
admit(call, snapshot):
    if snapshot.actions absent or empty:  deny  ACTION-SCOPE-ABSENT   # fail-closed
    if call.tool ∉ snapshot.actions:      deny  ACTION-SCOPE         # consume the narrowed fact
    return M0(call)                                                   # synthesis unchanged
```
Measured: 4/4 attacks denied, 4/4 benign allowed, 0 false denials, arm-2 control byte-identical (`discriminating_tests\results\REPORT.md`, Test 2). General rule: make the sender's boundary readable at the receiver — and read it. Signed evidence carriage is the transport; consumption is the enforcement.

Derivation side (when the bridge itself widened, V1/V2): fix the widened manifest derivation at the bridge; a receiver cannot recover a fact that was never narrowed. Arms 6/7 suppress (0 leaks) but are not claimed production-safe.

### 4.6 Evaluation protocol
```
lock       freeze cases, arms, predictions, hashes — before any run
run        strictly sequential, offline, deterministic
audit      anchors: oracle reproduction, case-dict equality, field checks
reconcile  predicted≠observed recorded verbatim; never edited in
publish    every number generated from artifacts; byte-verbatim embeds
```

### 4.7 Position vs upstream formalisms
| System | Formal spine | Composition-claim scope |
|---|---|---|
| APC | scope algebra, meet ⊓, conditions C1–C6, Thm 4.8 | within APC (conditional on static X) |
| TraceGrant | POEC contracts, Eq. 2 / Algorithm 1 | soundness assumed (Eq. 10), not proven |
| SentinelAgent | token τ, P1–P7, TLA+ (2.7M states), Thm 4 | admits only both-chains-same-mechanism |
| **This draft** | narrowing-preservation + blindness lemma | cross-mechanism composition — the slot the others leave uncovered |

---

## 5. Threats to validity / not claimed

- Not claimed for bridges beyond V1/V2; V1/V2 may be mis-designs and are not asserted to be the only or most likely bridges.
- Not claimed: production safety of arms 6/7. Arm 6 assumes the attestation is verified under the trusted key; arm 7 accepts 20 benign false denials. Both are scoped design choices.
- Not claimed: H4 (no shared audit trail) and H7 (intent layer) — both `UNTESTED`.
- Not claimed: generalization beyond the frozen case sets. Effective sample sizes are 1 design point × 4 cases (E1; boundary per variant); Pilot 1 and SA families are constructed case sets, not benchmarks.
- Not claimed: any vulnerability in APC, TraceGrant, or SentinelAgent as published. Findings are properties of this implementation under the locked bridge mappings and key models.
- Not claimed: comparability with published benchmark numbers; case sets are constructed here and mechanisms' own evaluations are self-reported by their authors.
- Not claimed: that the zero seam test generalizes beyond these pilots' case families; it is a recorded property of every case built, not a theorem.
- Convention dependence: seam-test counts differ under frozen family-wide vs arm-native scoring (E1: 0 vs 4/4). The canonical disclosure is unchanged and remains accurate.
- SA scoring is arm-invariant; rescoping would flip `composition_history_loss` arm 2 from leak to safe.
- Boundary convention: arm 2 is always canonical regardless of the variant loop variable; variant arms use the variant manifest derivation. Arm 2v ≡ arm 5 per variant is forced by construction.
- M2-auth does not establish authenticated transport (public test key; signer is the same harness; no forger control).
- Arm 7's M1 action rule (`tool not in snapshot.actions`) was not independently exercised (the retained shadow denial fired first in all four E1 attacks).
- E1 seam-test caveat: as operationalized it can fire only on widening-type families; on a narrowing family a zero does not by itself establish composition-independence (may also apply to the original run's zero seam test; not re-verified here).
- Arm 2's authority assignment in E1 is a disclosed convention (own-world norm adopted in discriminating Test 1; under the alternative reading arm 2's admission locates a failure in the mapping's authority assignment, still not a mechanism-interaction effect).

---

## 6. Source map (every numeric claim → artifact path + field)

| # | Claim / number | Value | Artifact (relative to `RPaper\`) | Field / location |
|---|---|---|---|---|
| 1 | Pilot 1 scale | 80 cases × 7 arms = 560 executions; 40 attack cases | `tests\seam_pilot_v2\results\raw_metrics.json` | `*.runs = 80`, `*.attack_cases = 40` (7 arms) |
| 2 | Pilot 1 leak cases | 24/40 attack cases | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.attack_successes = 24` |
| 3 | Pilot 1 unauthorized-effect events | 26 | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.unauthorized_effect_events = 26` |
| 4 | Pilot 1 repeated_calls events | 6 | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.per_template.repeated_calls.unauthorized_events = 6` |
| 5 | Pilot 1 marker-bearing external effects | 4 | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.confidential_marker_external_effects = 4` |
| 6 | Pilot 1 resource_widen leaks | 0 | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.per_template.resource_widen.leaked = 0` |
| 7 | Pilot 1 recipient/omitted leaks | 0 | `tests\seam_pilot_v2\results\raw_metrics.json` | `per_template.recipient_substitution.leaked = 0`, `omitted_forbidden_default.leaked = 0` |
| 8 | Pilot 1 M2 leaks | 0/40 | `tests\seam_pilot_v2\results\raw_metrics.json` | `apc_tracegrant_retained.attack_successes = 0` |
| 9 | Pilot 1 fail-closed leaks / FD cases | 0 leaks; 20/40 benign FD | `tests\seam_pilot_v2\results\raw_metrics.json` | `apc_tracegrant_fail_closed.attack_successes = 0`, `benign_false_denial_cases = 20` |
| 10 | Pilot 1 fail-closed FD events | 28 | `tests\seam_pilot_v2\results\raw_metrics.json` | `apc_tracegrant_fail_closed.false_denial_events = 28` |
| 11 | Pilot 1 receipt failures (M0) | 4 | `tests\seam_pilot_v2\results\raw_metrics.json` | `tracegrant_alone.receipt_failures = 4` |
| 12 | E1 scale | 8 cases × 5 arms = 40 executions + 6 controls | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §1, §3.3 | tables; `results\extension_e1\manifest.json` |
| 13 | E1 M0 leaks | 4/4 each, 4 events each | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.2–§3.3 | outcome matrix; `results\extension_e1\metrics.json` |
| 14 | E1 arm 1 / 6 / 7 denials | 4/4 each | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.2 | outcome matrix |
| 15 | E1 benign | 4/4 allowed, 0 FD | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.3 | per-arm summary |
| 16 | E1 arm-5 confusion | TP 4 / FP 0 / FN 0 / TN 4 | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.3 | assertions table; `results\extension_e1\assertions.json` |
| 17 | E1 signed records verified | 8 (`EVIDENCE-VERIFIED`) | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §3.4 | attack event detail (report-only; raw `extension_e1\metrics.json` has no `evidence_verified` field) |
| 18 | E1 controls | 3 controls, 6 executions, all passed | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §4 | check records; `results\extension_e1\controls.json` (`lock_matches` all true) |
| 19 | E1 M2-auth scheme | HMAC-SHA256, 56-byte key, `canon(payload)` | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §4 | module docstring quote |
| 20 | E1 dataset hash | `1b7c6083…b2e264ba` | `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` §2 | lock proof; `design\extension_e1_lock.json` |
| 21 | Discriminating Test 1 arm-2 root-norm leaks | 0/4 | `tests\seam_pilot_v2\discriminating_tests\results\test1_rescored_arm2.json` | `counts.arm2_attack_leaks_root_norm = 0`, `counts.arm2_attack_leaks_handoff_norm = 4` (`REPORT.md` §1–§2, dual cite) |
| 22 | Discriminating seam test (canonical) | 0 | `tests\seam_pilot_v2\discriminating_tests\results\test1_rescored_arm2.json` | `seam_test.under_canonical_scoring.count = 0` (`REPORT.md` §2, dual cite) |
| 23 | Discriminating seam test (root norm) | 4/4 | `tests\seam_pilot_v2\discriminating_tests\results\test1_rescored_arm2.json` | `seam_test.under_root_norm_arm2_scoring.count = 4` (`REPORT.md` §2, dual cite) |
| 24 | Discriminating Test 2 arm-5 denials | 4/4 `ACTION-SCOPE` | `tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §3 | matrix; `results\test2_metrics.json` |
| 25 | Discriminating Test 2 benign allowed | 4/4 | `tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §3 | matrix |
| 26 | Discriminating Test 2 receipts | 12/12 | `tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §3 | `results\test2_metrics.json` (`all_receipts_ok = true`) |
| 27 | Discriminating Test 2 arm-2 parity / digests | 8/8 / 8/8 | `tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` §3 | `results\test2_assertions.json` (P2.4, P2.5) |
| 28 | Discriminating predictions matched | 10/10 | `tests\seam_pilot_v2\discriminating_tests\results\reconciliation.json` | `status = "all locked predictions matched"`, `mismatches = []` |
| 29 | Discriminating lock hash | `8cd4d993…996011ab` | `tests\seam_pilot_v2\discriminating_tests\design\discriminating_lock.json` | file SHA-256 |
| 30 | SA scale | 96 cases × 7 arms = 672 executions; 48 attack cases | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §1, §3 | `results\sa\runs.jsonl` (672 rows) |
| 31 | SA leak cases | 28/48; 30 events | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §6 | `results\sa\metrics.json`: `sentinelagent_alone.attack_successes = 28`, `unauthorized_effect_events = 30` |
| 32 | SA dynamic-state leaks | 24 of 28 | `tests\seam_pilot_sentinelagent\results\claims_update_sentinelagent.md` H2 | class breakdown |
| 33 | SA keyholder_widen leaks | 4/4 in arms 2/5 | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §7 | per-template table |
| 34 | SA arm 6 leaks / arm 7 false denials | 0 leaks; 20 benign FD cases / 28 FD events | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §6, §10 | `results\sa\metrics.json`: `apc_sentinelagent_retained.attack_successes = 0`; `apc_sentinelagent_fail_closed.benign_false_denial_count = 20`, `false_denial_events = 28` |
| 35 | SA signature family foreign key | 4 `SIGNATURE_INVALID` per token arm | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §7, §11 | code histograms; controls S2-foreign |
| 36 | SA controls | 10, all passed | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §11 | `results\sa\controls.json` (`ok = true`, 10 records) |
| 37 | SA determinism reruns | 20, 0 mismatches | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §12 | `results\sa\self_review.json` |
| 38 | SA admissions / token denials | 488 / 150 | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §12 | `results\sa\self_review.json` (`not_vacuous`) |
| 39 | SA reconciliation item 1 | FD events locked 26 vs observed 28 | `tests\seam_pilot_sentinelagent\results\sa\reconciliation.json` | item `arm7_false_denial_events` |
| 40 | SA reconciliation item 2 | TN locked 68 vs observed 20 (attack-case denominator) | `tests\seam_pilot_sentinelagent\results\sa\reconciliation.json` | item `arm5_confusion_true_negative_denominator` |
| 41 | SA lock hash | `9f2611a1…65d47f0` | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §3 | `design\sa_lock.json` |
| 42 | SA cases hash | `ca2f05d5…e42cb6d2` | `tests\seam_pilot_sentinelagent\results\SA_RESULTS.md` §3 | `design\sa_cases.json` |
| 43 | Boundary scale | 1,152 runs | `tests\seam_pilot_sa_boundary\results\boundary\reconciliation.json` | `run_reference.matrix_executions = 1152` |
| 44 | Boundary cell size | 96 rows per cell | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `*.rows = 96` |
| 45 | Boundary arm 1 leaks | 0 (both variants) | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `apc_alone::* .attack_successes = 0` |
| 46 | Boundary arm 2 leaks | 28 cases / 30 events | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `sentinelagent_alone::* .attack_successes = 28`, `unauthorized_effect_events = 30` |
| 47 | Boundary arm 2v / 5 leaks | 32 cases / 34 events | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `sentinelagent_alone_variant::*` and `apc_sentinelagent_scope_only::*`: `attack_successes = 32`, `unauthorized_effect_events = 34` |
| 48 | Boundary new (variant-specific) leaks | 4 per variant | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `attack_success_cases` lists (resource_widen ×4; omitted_forbidden_default ×4) |
| 49 | Boundary arm 6 leaks | 0; APC-DENY on 4 seam cases | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `apc_sentinelagent_retained::* .attack_successes = 0` |
| 50 | Boundary arm 7 leaks | 0; SHADOW-DENY on 4 seam cases; 20 benign FD / 28 FD events | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `apc_sentinelagent_fail_closed::*`: `attack_successes = 0`, `benign_false_denial_count = 20`, `false_denial_events = 28` |
| 51 | Boundary benign leaks | 0 | `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` | `benign_false_denial_count = 0` (arms 1, 2, 2v, 5, 6) |
| 52 | Boundary seam count | 4 per variant | `tests\seam_pilot_sa_boundary\results\boundary\manifest.json` | `seam_test.v1.seam_count = 4`, `seam_test.v2.seam_count = 4` |
| 53 | Boundary expected_vs_observed_ok | true (checks seam_count == 4 only) | `tests\seam_pilot_sa_boundary\results\boundary\manifest.json` | `expected_vs_observed_ok = true` |
| 54 | Boundary arm 2 canonical overstatement | 28 pre-existing leaks, not 0 | `tests\seam_pilot_sa_boundary\results\boundary\reconciliation.json` | item `arm2_canonical_leak_scope_overstated` |
| 55 | Boundary controls | 7, passed | `tests\seam_pilot_sa_boundary\results\boundary\manifest.json` | `controls.ok = true`, `records` (7) |
| 56 | Boundary self-review | ok = true | `tests\seam_pilot_sa_boundary\results\boundary\self_review.json` | `ok = true` |
| 57 | Boundary lock hash | `b4deab1a…082c4296` | `tests\seam_pilot_sa_boundary\results\boundary\manifest.json` / lock | `design\boundary_lock.json` |
| 58 | Boundary harness hash | `fa8f7e42…790814af4` | `tests\seam_pilot_sa_boundary\results\boundary\self_review.json` | `hash_unchanged:boundary_harness.py` |
| 59 | Formal core measured instances | E1 4/4; boundary 32/34, 28/30, 4 new | `RPaper(user)\FORMAL_CORE_DRAFT.md` §3–§4 | measured instances; cross-references above |

---

## 7. Change record

- **Consolidated from:** `tests\seam_pilot_v2\results\claims_update.md` (Pilot 1 H1–H6); `tests\seam_pilot_v2\results\claims_update_extension.md` (H1 action clause + revision notes); `tests\seam_pilot_v2\results\EXTENSION_E1_RESULTS.md` (8×5 run, arm-5 numbers, controls); `tests\seam_pilot_v2\discriminating_tests\results\REPORT.md` and `reconciliation.json` (Test 1/Test 2, 10/10 predictions); `tests\seam_pilot_sentinelagent\results\claims_update_sentinelagent.md` and `SA_RESULTS.md` (SA pair, 28 leaks); `tests\seam_pilot_sa_boundary\results\boundary\claims_update_boundary.md` (V1/V2 H1–H6); `tests\seam_pilot_sa_boundary\results\boundary\metrics.json` and `reconciliation.json` (authoritative boundary numbers); `RPaper(user)\FORMAL_CORE_DRAFT.md` (definitions, lemma, proposition, repair rule, protocol).
- **Superseded:** the claim ladder in `paper\Paper_Claims_and_Takeaways.md` (pre-consolidation). A one-line supersession note was added at its top; the file itself is otherwise untouched.
- **Reconciliation:** all source-vs-artifact discrepancies, errata (B1–B6), ambiguities, and convention disclosures are recorded verbatim in `paper\consolidation_reconciliation.md`. No source was silently normalized.
- **Not changed:** no frozen artifact (locks, harnesses, cases, traces, reports) was modified. Frozen hashes are recorded in `paper\consolidation_self_review.json`.