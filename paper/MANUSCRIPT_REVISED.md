# The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry

## Abstract

Agent authorization rarely stops at a mechanism boundary: a sender narrows authority, a bridge translates it into a record the receiver can read, and the receiver applies admission rules. Each can be correct alone while the composition admits a call the sender never authorized. This paper treats that handoff as a measurement problem and separates two questions: whether the composed system commits a sender-relative violation, and whether composition adds a failure the standalone receiver does not exhibit. Predictions, cases, arms, and hashes are frozen before execution; values come from stored artifacts. Across 2,446 executions, the composed arms admit 24/40 and 28/48 sender-unauthorized calls in the two pair pilots, but the standalone receivers admit the same calls; receiver-relative novelty is zero in both, both zeroes are construction-forced. One composition-specific test, an action-narrowing family, yields receiver-relative novelty of 4/4 under arm-native scoring and 0/4 under the frozen family-wide convention even as 4/4 attacks are admitted; consuming that set denies 4/4 attacks and allows 4/4 benign calls. Non-narrowing-preserving derivations leak four new cases per variant, standalone and composed, locating the fault at the bridge. We close with a replication package and repair taxonomy: consumption or evidence carriage when the narrowed fact crosses intact, derivation repair when the bridge widens. The zero is a recorded property of narrowing-preserving mappings on the frozen cases, not a theorem.

**Keywords:** cross-mechanism authorization; agent authorization; authorization seams; scope narrowing; evidence carriage; conformance testing; locked-artifact methodology

## 1. Introduction

A sender holds authority over a call space and narrows it before handing a call to another mechanism. A bridge translates the narrowed decision and the current state into a record the receiver can read. The receiver applies its own admission rules. Each party can be faithful inside its own world — the narrowing exact, the transport byte-perfect, the receiver's verdict consistent with its own policy — and the composed system can still admit a call the sender never authorized. The failure is not necessarily an unfaithful record. It can be a faithful record that carries a fact the receiver's decision never reads.

A concrete instance motivates the paper. In the E1 action-narrowing family (Section 4.2), the sender's root authority includes `send_external`, the narrowed authority does not, and the bridge writes the narrowed action set `[read_public, save_internal]` into the receiver-side snapshot. The action set crosses the seam intact. The receiver's synthesis never consults it, and the composed arm admits `send_external` on all four attack cases. The receiver is not parsing the record incorrectly; it is not reading the field that would have stopped the call. We call this the seam: the handoff between a sender's narrowing and a receiver's decision, owned by neither mechanism.

The research question is sender-relative: at a cross-mechanism handoff, does the composed system enforce the sender's narrowing, or does it admit calls the narrowing never conferred? The measurement question is narrower: does composition add an admission beyond what the standalone receiver already exhibits? The two questions coincide only when the receiver is safe on its own. When the receiver already admits the call, the composed system commits a sender-relative violation but adds no receiver-relative novelty. This paper reports both counts separately; the distinction is the main methodological correction of the study.

**Contributions.** The paper makes four contributions.

1. **A locked-artifact method for cross-mechanism seams.** Predictions, cases, arms, and input hashes are frozen before execution; runs are sequential, offline, and deterministic; predicted-versus-observed discrepancies are reconciled verbatim; and every reported number is generated from stored artifacts rather than transcribed by hand (Section 3.1).
2. **A two-reading seam test.** The test separates a sender-relative violation (the sender denies, the composed system admits) from receiver-relative novelty (the standalone receiver denies, the composed system admits). It also records what the receiver's decision reads, not merely what the record carries (Sections 3.2–3.3).
3. **An empirical map of four frozen experiment sets.** Across 2,446 executions, the two pair pilots show that the composed arms admit 24/40 and 28/48 sender-unauthorized calls, while the standalone receivers admit the same calls; receiver-relative novelty is zero, and those two zeroes are construction-forced. The one genuine composition-specific test is the E1 action family: receiver-relative novelty is 4/4 under arm-native scoring and 0/4 under the frozen family-wide convention, while the composed arm admits 4/4 attacks under both, with a consumption repair that denies 4/4 attacks and allows 4/4 benign calls. The boundary study shows that non-narrowing-preserving bridge derivations leak four new cases per variant both standalone and composed (Sections 4.1–4.5).
4. **A repair taxonomy and a replication package.** The taxonomy separates receiver-side consumption, evidence carriage, and retention of the upstream denial from bridge-side derivation repair. The package contains the frozen case sets, harnesses, locks, and protocol; it is a release candidate, not a public conformance service (Sections 5 and 8).

**What the paper does not claim.** The zero is a recorded property of narrowing-preserving mappings on the frozen case sets, not a theorem, and it is not a claim that seams are safe in general. The paper does not claim that APC, TraceGrant, or SentinelAgent is broken; their published guarantees are reported as their authors state them. It does not claim benchmark comparability, production safety for any repair arm, or authenticated transport for the HMAC test channel. Two hypotheses, H4 (shared audit trail) and H7 (intent layer), remain `UNTESTED` (Section 7.5). The broader attenuation and delegation literature is outside the measurement scope; the contribution is a cross-mechanism measurement, not a new attenuation primitive (Section 6).

**Roadmap.** Section 2 places the three formal spines and Progent. Section 3 presents the method, formal core, two-reading seam test, scoring conventions, execution ledger, threat model, and hypothesis key. Section 4 reports the four experiment sets. Section 5 draws the repair taxonomy and the practical implications. Section 6 positions the work, Section 7 states the threats and open hypotheses, Section 8 describes the replication package, and Section 9 concludes.

The formal objects are simple. A call space C collects calls c = (tool, resource, arguments, …). A mechanism M = (V_M, admit_M) comprises a vocabulary V_M — the fields the mechanism can represent and, structurally, read — and an admission function admit_M(c, ρ) ∈ {allow, deny}. Authority A ⊆ C is the call set a principal confers; a sender narrows A to A′ ⊆ A. A bridge B consumes the narrowed decision and state and writes the receiver-side record ρ_R = B(A′, state). Composition is admit_C(c) ≔ admit_R(c, B(A′)), and the composition's effective authority is A_C ≔ { c : admit_C(c) = allow }. The receiver's read set V_read ⊆ V_R is the set of fields its decision actually consults — not the fields the record carries, but the fields the decision reads.

![**Figure 1.** Anatomy of a cross-mechanism handoff — the sender narrows authority, the bridge translates it into a receiver-side record, and the receiver decides; the schematic distinguishes the record the bridge carries from the read set the receiver's decision actually consults.](figures/figure_1_handoff_anatomy.pdf){#fig:figure1 width=3.33in}

The schematic carries no data and no numbers. A fact in the carried record that no decision reads constrains no decision; Section 3.2 states this as a definitional observation, not an empirical result. The seam can therefore admit what the sender never narrowed even when the transport is clean.

## 2. Background — APC (Agentic Principal Chain), TraceGrant, SentinelAgent; Progent as reference

This section places the three formal spines whose within-mechanism guarantees leave the cross-mechanism slot uncovered, and it reports each upstream guarantee as its authors' self-report — never upgraded to a manuscript result and never cited as this program's measurement. None of the three spines supplies a cross-mechanism composition guarantee; the observation is scoped to these three systems and is not a universal negative. The purpose is to show where each guarantee stops, so that the uncovered slot — the seam between mechanisms — can be named plainly.

APC [APC] — the Agentic Principal Chain mechanism — reports within-mechanism authorization: a scope algebra with meet ⊓, conditions C1–C6, and Thm 4.7 (Composition Soundness), conditional on a complete effective restriction set, serialized admission, and a static X within a session. APC's “composition” is composition of action sequences inside one session; it is not composition across mechanisms. Its resource meet holds inside the mechanism. APC alone governs calls inside one mechanism; it says nothing about what happens when a narrowed call crosses into another mechanism's vocabulary, and it supplies no cross-mechanism composition guarantee. Its authorization reasoning is sound only relative to the assumptions the theorem names, and nothing in APC extends that reasoning across a bridge to a receiver with a different vocabulary.

TraceGrant [TraceGrant] reports within-mechanism delegation: POEC contracts, Eq. 2 / Algorithm 1. Its soundness is assumed (Eq. 10 is not proven). Like APC, TraceGrant's guarantee stays inside its own mechanism and extends no composition claim across a seam. Delegation soundness is an assumption of the formalism, not a result this program verifies, and it covers calls handled within TraceGrant's own contract model rather than calls handed off to another mechanism.

SentinelAgent [SentinelAgent] reports a token model τ with principles P1–P7 (P1 and P3–P7 TLA+-checked; P2 probabilistic), a TLA+ model of 2.7M states — an upstream self-report, not a measurement of this program — and Thm 4 (Composition Safety with Write-Impact Notification), which is stated for two delegation chains that both satisfy P1–P7 within its own framework. It does not state a guarantee for a chain handed to a different mechanism's decision procedure; that boundary is where this paper's cross-mechanism question begins. That figure is the authors' own model-scale claim; this program neither measured it nor relies on it as evidence.

The uncovered slot: within-mechanism guarantees do not compose across mechanisms. None of APC, TraceGrant, or SentinelAgent supplies a cross-mechanism composition guarantee. Scoped to these three — no universal negative — the slot remains: what happens at the seam between a sender's narrowing and a receiver's decision when the two mechanisms do not share a vocabulary or a decision rule. The three scopes differ in their limits, but they share the same boundary. APC's theorem is conditional on a static X and governs intra-session action-sequence composition inside one mechanism, so it says nothing about a call crossing into another mechanism's vocabulary. TraceGrant's soundness is assumed rather than proven (Eq. 10), so its delegation guarantee covers contracts handled within TraceGrant's own model, not calls handed off to another mechanism. SentinelAgent's theorem addresses composition of two chains within its own P1–P7 framework, not a chain handed to a different mechanism's decision procedure, so the cross-mechanism case falls outside it. Each guarantee stops at its mechanism's edge: a record can be faithful at the bridge and still carry nothing the receiver's decision reads; a signature can be valid and still attest nothing about the source of authority; a theorem conditioned on a static state says nothing about a dynamic handoff.

This paper's position is adjacent to that slot: narrowing-preservation plus the blindness observation — cross-mechanism composition — is the measurement target. The observation says a fact carried but never read constrains no decision; narrowing-preservation requires the composed system to enforce at least the sender's narrowing on the relevant family. Together they name the question the three spines leave to the seam, and this program measures whether it holds on the frozen case sets. The claim is deliberately scoped: it concerns these three spines, these mappings, and these case sets, and it is not a universal statement about every bridge or every mechanism pair.

Progent [Progent] is a close reference point rather than an input to this program: it enforces monotonic confinement inside a single privilege-control layer, where an SMT solver classifies each policy update as a narrowing or an expansion; this paper asks whether a comparable narrowing survives translation across a mechanism boundary. Its reported results remain its authors' self-report and are not used as an input or comparison here. Nothing about Progent is claimed or measured in this section, and its results play no role in the paper's measured claims.

Disclosures: say "reports," never upgrade a self-report to an established result; upstream guarantees and numbers stay self-reported; nothing in this section impugns any upstream mechanism; no production-safety claim; no benchmark comparability; citations are pointers, not verified inputs. Citation keys are bracketed — [APC], [TraceGrant], [SentinelAgent], [Progent] — and no bibliographic detail is invented. The industry/standards citation layer belongs to Section 6 and is not invoked here.

**Scope of positioning.** This is a measurement paper, not a survey of authorization theory. Section 6 positions the work against the three formal spines, the standards and systems that define the relevant vocabulary (OAuth token exchange and rich authorization requests, macaroons, object-capability systems, relationship-based access control, proof-carrying authentication, and SPKI), the closest 2026 agent-delegation work, and the two nearest empirical relatives. Those literatures contain the established vocabulary for attenuation, caveat discharge, ambient authority, and policy intersection; this paper uses that vocabulary but does not claim to extend it. The contribution is a cross-mechanism measurement of three specific mechanisms and their handoffs, plus a method and a replication package. A comparative treatment would require running the comparison systems under a common lock; none is run here.

Table 1 summarizes each formal spine and the scope of its composition claim.

**Table 1.** Formal spine and composition-claim scope.

| System | Formal spine | Composition-claim scope |
|---|---|---|
| APC | scope algebra, meet ⊓, conditions C1–C6, Thm 4.7 (Composition Soundness) | within APC, intra-session; conditional on complete restriction set, serialized admission, static X |
| TraceGrant | POEC contracts, Eq. 2 / Algorithm 1 | soundness assumed (Eq. 10), not proven |
| SentinelAgent | token τ, P1–P7, TLA+ (2.7M states), Thm 4 (Composition Safety) | within its own delegation framework; no cross-mechanism handoff guarantee |
| **This paper** | narrowing-preservation + blindness observation | cross-mechanism composition — the question the others leave to the seam |

Table note: the SentinelAgent "2.7M states" cell is an upstream self-report, not a measurement of this program; the TLA+ model covers P1 and P3–P7, while P2 (intent) is probabilistic.

## 3. Method

This section presents the method as a contribution in its own right: a measurement discipline for cross-mechanism authorization seams, built so that the numbers it produces can be re-derived from locked artifacts by an independent reader. Cross-mechanism authorization invites measurement failures that are hard to detect after the fact: scoring conventions chosen once the data are visible, and counts typed by hand into reports. The method is designed against both. It combines pre-registration everywhere with a lock-before-run execution stage; it generates every reported number from run artifacts rather than typing it; it reconciles predicted and observed outcomes verbatim rather than editing them into agreement; and it submits the consolidated record to a model-assisted adversarial review and a second quality-assurance pass before anything is frozen. The section proceeds from that discipline (Section 3.1) through the formal objects it measures (Section 3.2) and the seam-test predicate (Section 3.3) to the scoring conventions that govern every classification (Section 3.4), the execution program and its ledger (Section 3.5), and the scope the method accepts (Section 3.7). Outcomes are reported nowhere in this section; where a sentence might otherwise forecast what a run found, it is phrased as what the method does or as how a quantity is defined.

### 3.1 Pre-registration by lock

Every experiment in the program is locked before it runs. A design artifact freezes the case set, the arm roster, the predictions the run will be scored against, and the fingerprints of the executed inputs; the lock record exists before any execution begins, and the executed cases are the locked ones. Lock records and their fingerprints — for datasets, case sets, and harnesses — are part of each run's artifact tree: for the E1 extension's dataset lock and the discriminating tests' lock, for the SentinelAgent pair's lock and case set, and for the boundary run's lock and harness. Execution is strictly sequential, offline, and deterministic. Determinism is audited rather than presumed: the protocol replays locked executions and compares them against the originals, and in the SentinelAgent run the replay covered 20 executions with 0 mismatches.

A run then passes through the stages that discipline what may be said about it:

```
lock freeze cases, arms, predictions, hashes — before any run
run strictly sequential, offline, deterministic
audit anchors: oracle reproduction, case-dict equality, field checks
reconcile predicted-versus-observed recorded verbatim; never edited in
publish every number generated from artifacts; byte-verbatim embeds
```

The audit stage anchors a run's results to checks that an independent reader can reconstruct: reproduction of the scoring oracle, equality of the run's case dictionary against the locked cases, and field-level validation of the run records. The reconciliation stage is the integrity core of the method: whenever an observed outcome differs from a locked prediction, the difference is recorded verbatim, whether or not it favors the hypothesis under test, and it is not edited into agreement afterwards. The publish stage closes the loop: numbers are not transcribed by hand into the paper — every reported number is generated from the stored artifacts, and where the prose embeds an artifact value, it embeds that value byte-verbatim. A consequence we adopt throughout: a total is written only as the explicit sum of its enumerated components, and no rounded aggregate is used in its place.

### 3.2 The formal core

The definitions in this subsection are measurement instruments: they state what the program scores, not what any run observed. A call space C collects calls c = (tool, resource, arguments, principal, session, …). A mechanism M = (V_M, admit_M) comprises a vocabulary V_M — the fields the mechanism can represent and, structurally, read — and an admission function admit_M(c, ρ) ∈ {allow, deny}, evaluated over a call and a receiver-side record ρ. Authority A ⊆ C is the call set a principal confers; a sender narrows A to A′ ⊆ A. A bridge B is the seam's translation step: it consumes the narrowed decision together with state and writes the receiver-side record ρ_R = B(A′, state). Composition is admit_C(c) ≔ admit_R(c, B(A′)), and the composition's effective authority is A_C ≔ { c : admit_C(c) = allow }.

The read set V_read(ρ) ⊆ V_M is the set of fields on which admit_M actually depends — the support of the decision function, not the fields the record carries. This distinction is the formal core's one substantive definition. It yields a definitional observation:

**Blindness observation (definitional).** Fix a record ρ and a family F. If admit_R depends on c only through the projection π_{V_read}(c, ρ), and no value in V_read separates A′ ∩ F from its complement on a pair of calls, then no admission function over V_read can enforce A′ on that pair. The proof is immediate: a function of a projection cannot distinguish inputs that the projection identifies. The corollary is the paper's aphorism: carried but unread = uncarried (for decision purposes).

The observation is not an empirical result and is not tested by these experiments; it explains why a carried-but-unread fact cannot constrain a decision. What the experiments measure is whether a given receiver's read set separates the narrowed set on the frozen cases. A receiver can fail in three distinct ways: the fact is absent from its vocabulary, the fact is carried but not read, or the bridge does not carry it. Section 4.3 separates these loci.

**Narrowing-preservation.** A bridge is narrowing-preserving on a family F in the effective reading iff A_C ∩ F ⊆ A′ ∩ F. The transport reading asks only whether the narrowed record crosses; the effective reading asks whether the composed decisions enforce the narrowing. The paper adopts the effective reading because a narrowing that the composition does not enforce should not count as preserved. Both readings are recorded, and any classification that depends on the choice carries it.

**Mapping taxonomy.** The bridge variants named in the results are defined here. **M0** is the one-step, transport-faithful, scope-only bridge: it carries the sender's narrowed scope but no upstream decision. **M2** is digest-only evidence carriage; **M2-auth** is HMAC-signed evidence carriage; **M0-A** is M0 with a consuming action-scope gate. **T0** is the canonical narrowing-preserving mapping used by the primary runs; **V1** and **V2** are the two deliberately non-narrowing-preserving manifest derivations in the boundary run (Section 4.4). These labels name implementation choices, not properties of APC, TraceGrant, or SentinelAgent as published.

### 3.3 The seam test and two readings

The seam test is defined case-wise over the pilot-level arms. Let `deny(arm)` mean the arm denies the call, and `allow(arm)` mean it admits the call. Two predicates are reported separately:

$$
\mathrm{violation}_{S}(case) := \mathrm{deny}(\mathrm{arm}\ 1) \land \mathrm{allow}(\mathrm{arm}\ 5)
$$

$$
\mathrm{novelty}_{R}(case) := \mathrm{deny}(\mathrm{arm}\ 2) \land \mathrm{allow}(\mathrm{arm}\ 5)
$$

The first is sender-relative: the sender's narrowed arm denies, the composed arm admits. The second is receiver-relative: the standalone receiver denies, the composed arm admits. The seam test is the conjunction of no sender violation, no receiver violation, and a composed admission:

$$
\mathrm{seam}(case) := \mathrm{safe}(\mathrm{arm}\ 1) \land \mathrm{safe}(\mathrm{arm}\ 2) \land \lnot \mathrm{safe}(\mathrm{arm}\ 5)
$$

where `safe(arm)` holds exactly when no call outside that arm's own world's conferred authority executes. Arm 1 carries the sender's narrowed decision, arm 2 is the receiving mechanism evaluated standalone, arm 5 is the scope-only composition, and arms 6 and 7 are the evidence and fail-closed interventions. The predicate is the conjunction of the two readings: it is true only when the sender-relative violation and the receiver-relative novelty both fire. It is the definition the frozen artifacts record for the pilot-level test. The two predicates are reported separately because they can diverge: in Pilot 1 and the SentinelAgent pair, the sender-relative violation fires but novelty does not; in E1 under the family-wide convention both are false; under arm-native scoring both fire. Arms 6 and 7 are reported separately as repair outcomes, not folded into the predicate: a leaking repair arm is a repair failure, not a composition failure. The E1 discriminating test uses the arm-5 form and names that convention with its counts.

The distinction matters because the two questions diverge when the receiver is unsafe on its own. In Pilot 1 and the SentinelAgent pair, arm 5 admits the same calls as arm 2; the composed system commits sender-relative violations, but it adds no receiver-relative novelty. In E1 under arm-native scoring, arm 2 is safe and arm 5 admits, so both predicates fire. The result sections report both counts; a zero in the seam test is a statement about the conjunction, not about the absolute level of unauthorized admission.

**Falsification and stop conditions.** The two readings are exposed to different disconfirmations. A sender-relative violation is counted only when arm 1 denies and arm 5 admits; a frozen case on which arm 1 admits a call outside the sender's narrowed set would count against the premise that arm 1 carries the sender's narrowed decision on that case, and the case would be reclassified rather than scored as a violation, while a case on which both arms deny is not evidence that the composition enforces the narrowing. A receiver-relative novelty count is a count over the frozen cases: one locked case on which arm 2 denies and arm 5 admits in a set reported as zero-novelty would disconfirm that zero, while a case on which arm 2 also admits is the pair-pilot pattern and carries no composition-specific witness. A run stops rather than being scored if the lock or case-set hash does not match the executed inputs, if the scoring oracle cannot reproduce the locked labels, or if an arm's decisions cannot be reconstructed from its records. A derivation that is not narrowing-preserving is not scored as a seam failure; it is moved to the boundary condition and reported as a derivation-widening finding (Section 4.4). Because the seam test as operationalized is a widening test, a zero on a set where the composition does not widen is reported as construction-forced, not as confirmation of composition-independence. These conditions bind every count in Section 4 and leave H4 and H7 outside the test (Section 7.5).

### 3.4 Scoring conventions

Every classification of an arm's admissions names the scoring convention under which it was scored. The convention set is closed, and it contains four members: a frozen family-wide convention; an arm-native convention; a boundary convention with a canonical member and a variant-manifest member; and an arm-invariant convention for the SentinelAgent pair. Table 2 states what each convention scores, at definition level.

**Table 2.** Scoring-convention matrix — the four classification conventions and what each scores (definitional rows; no run data).

| Convention | What it scores |
|---|---|
| Family-wide (frozen) | Scores each arm of a mechanism family against a shared authorization norm derived from the handoff, including arms whose own world contains no handoff |
| Arm-native | Scores each arm against its own world's conferred authority |
| Boundary canonical / variant-manifest | Scores the standalone arm canonically regardless of the surrounding variant loop variable, and scores the variant arms against the authority that their variant-manifest derivation produces |
| SA arm-invariant | Scores by an admission relation applied identically across all arms of the family, including the standalone arm (role-resource conjunction, with the prohibited-composition rule applied to the standalone arm as well) |

Conventions are carried by disclosure rather than by report-time choice. Where more than one convention can classify the same records, each reported classification states the convention that produced it, and any selection rule between readings is stated with the report rather than assumed. This requirement binds the result sections: every count, contrast, or reconciliation that those sections report carries its convention, so that no number can be read outside the rule that generated it.

The family-wide convention is the frozen reference for the pair pilots: it scores every arm against the handoff-derived norm, including the standalone receiver whose own world contains no handoff. The arm-native convention scores each arm against its own world's conferred authority. Neither convention is universally correct; they answer different questions. The paper reports both where they diverge. The E1 composition-specific reading uses arm-native scoring because the question is whether the composed arm admits a call the receiver's own world would deny; the frozen family-wide reading is reported alongside it so that the convention dependence is visible. The SentinelAgent pair uses an arm-invariant relation applied to all arms; rescoping it would flip `composition_history_loss` arm 2 from leak to safe, and that sensitivity is disclosed in Section 7.1.


### 3.5 The execution ledger

The matrix execution ledger is an explicit record, transcribed from the frozen evidence base; Table 3 states it as an exact sum of its component runs, in the form the publish stage requires. The ledger includes E1's six control executions in the `+ 6` component: they are inside the 2,446 total. The SentinelAgent run's 10 control executions and the boundary run's 7 control executions are outside the total, as are the determinism replays and the separate Pilot-1 control, replay, and latency records; these secondary records are listed in the note below Table 3 so that no execution is counted twice. Control executions pin the admission behaviors on their own records.

**Table 3.** Matrix execution ledger — the program's matrix executions, stated as an explicit sum of its enumerated components.

| Run | Design | Executions |
|---|---|---|
| Pilot 1 (v2) — APC → TraceGrant | 80 cases × 7 arms | 560 |
| Extension E1 — action-narrowing + M2-auth | 8 cases × 5 arms | 40 + 6 control executions |
| Discriminating Test 1 (re-scoring only) | no new executions | 0 |
| Discriminating Test 2 | 8 cases (4 attack + 4 benign) × 2 arms | 16 |
| SentinelAgent pair — APC → SentinelAgent | 96 cases × 7 arms | 672 |
| Boundary — manifest-derivation variants (V1/V2) | 6 arms × 2 variants × 96 cases | 1,152 |
| **Total** | | **2,446 = 560 + 40 + 6 + 16 + 672 + 1,152** |

**Arm roster.** The same seven-arm structure is used in Pilot 1 and the SentinelAgent pair:

| Arm | Name | Role |
|---|---|---|
| 1 | `apc_alone` | sender alone; carries the narrowed decision |
| 2 | `tracegrant_alone` / `sentinelagent_alone` | receiver alone; no handoff |
| 3 | `apc_apc_preserved` | same-mechanism preserved control |
| 4 | `apc_apc_reset` | same-mechanism reset control |
| 5 | `apc_*_scope_only` | composed scope-only arm; the seam-test arm |
| 6 | `apc_*_retained` | composed evidence/attestation repair |
| 7 | `apc_*_fail_closed` | composed fail-closed repair |

The boundary run adds arm 2v (`sentinelagent_alone_variant`), the receiver evaluated with the variant manifest. The E1 extension uses arms 1, 2, 5, 6, and 7. The arm numbering is a label for the same role across sets, not a claim that the implementations are identical.

**Path notation.** The four artifact roots are:

- `v2` = `tests\seam_pilot_v2\results`
- `dt` = `tests\seam_pilot_v2\discriminating_tests\results`
- `sa` = `tests\seam_pilot_sentinelagent\results`
- `b` = `tests\seam_pilot_sa_boundary\results\boundary`

Full paths remain in the artifact tree.

**Outside the scale column (excluded from the total).** The SentinelAgent determinism replay, 20 executions; SentinelAgent control executions, 10; boundary control executions, 7; Pilot-1 control battery, 21 records; Pilot-1 determinism replay, 10 pairs; and the seven-arm latency harness, 100 warmup + 1,000 measured samples per arm. The latency harness output is `v2\latency.json`. E1's six control executions are inside the total, carried in the E1 row's `+ 6`. Totals are stated as explicit sums of enumerated components; no rounded aggregate is used.

**Implementation provenance.** APC's sender is the pinned upstream `apc/` package (commit `d31a1ea115a3`, abbreviated). The SentinelAgent receiver is the pinned upstream prototype (`sentinelagent_das_prototype.py`, SHA-256 `739d9db1e836`, abbreviated), with only the module-level key constant set by the harness. The TraceGrant receiver is the independent Task D implementation under `tests\tracegrant_task_d_20261014\implementation\`, wrapped without modification; its contract mapping is this program's design choice, not a reading of either paper. The bridge mappings throughout are this program's constructions, not upstream translations.

### 3.6 Review loop

The lock–run–publish discipline is completed by a review loop. After runs, the claim records are consolidated; the consolidated record is examined by a model-assisted adversarial review and again by a second quality-assurance pass, and the corrections raised are applied at source before the record is frozen. Reconciliation within this loop treats every predicted-versus-observed discrepancy verbatim, with no silent normalization. Where the results sections name upstream work — APC, TraceGrant, SentinelAgent, or Progent — it is reported as its authors state it, not re-derived here.

### 3.7 Ethics, AI use, and reflexivity

AI-assisted tools were used for the experiment implementation and artifact quality assurance. The SentinelAgent adversarial review was performed by `GLM-5.3-Flash Free`; a fresh-context OpenCode cross-check and a targeted external free-chat review were also used for quality assurance. These are not human peer review and do not constitute independent vendor validation. No AI system is an author; the author remains responsible for all claims, artifacts, and errors. No human-subjects data were collected; the work is synthetic and offline.

### 3.8 Threat model

The experiments are synthetic and offline. The threat model is deliberately narrow; it states what the case sets exercise, not what a deployed system must defend against.

| Element | Scope |
|---|---|
| Assets | the sender's narrowed authority; confidential markers; cumulative budget; freshness and revocation state; audit evidence |
| Adversary capability | a caller or delegate that can present calls and tokens to the receiver within the harness; can substitute recipients, widen resources, omit fields, replay calls, or mint a token with the published test key; cannot compromise the receiver process or bypass the bridge |
| Trust boundaries | sender → bridge → receiver; the bridge is the translation point; the receiver's own decision is trusted to run, but its read set is the object of measurement |
| Bridge status | V1/V2 are non-narrowing-preserving derivations, not a malicious bridge that forges signatures without the key; the paper measures mis-derivation, not full bridge compromise |
| Key model | HMAC-SHA256 with a public test constant; symmetric bearer key; any keyholder can mint a token the receiver verifies. Asymmetric delegation chains, where the receiver can distinguish minters, are out of scope |
| Out of scope | direct calls that bypass the bridge; a compromised receiver; side channels; prompt injection and intent classification (H7); network attacks; multi-hop chain reconstruction (H4) |
| Case mapping | `resource_widen`, `recipient_substitution`, `omitted_forbidden_default`, `principal_rebind`, `composition_history_loss`, `repeated_calls`, `budget_reset`, `expired_delegation`, `revoked_envelope`, `keyholder_widen`, `foreign_key_signed`, `unsatisfiable_verify` |

The threat model does not upgrade any finding into a vulnerability claim about APC, TraceGrant, or SentinelAgent. It identifies which capability each template exercises and which trust boundary the measured failure sits on.

### 3.9 Hypothesis key and status vocabulary

H1 — trusted-request laundering / scope trust; H2 — dynamic state, identity, and freshness do not cross and leak; H3 — state/identity vocabulary gaps manifest as silence, not misparse; H4 — no shared audit trail (`UNTESTED`); H5 — verification attests key possession and integrity, not authority; H6 — pair-wise failure shapes across the measured pairs; H7 — intent layer P2 (`UNTESTED`); ★ — the cross-cutting zero-under-preservation finding. The frozen experiment artifacts predate this key and use some labels differently; Appendix Table A1 records the lineage, and a legacy label is not read as the current label with the same number.

Status vocabulary: `SUPPORTED` means the stated claim held on the frozen cases under the stated conventions; it is not a statistical significance claim. `REFINED` means a narrower or partly supported version is carried and the original wording is not supported as stated. `UNTESTED` means no experiment in this program exercises the claim. `NOT CLAIMED` means the paper explicitly declines the claim. `REFUTED` means the frozen evidence contradicts the claim. The statuses are evidence grades for this paper's scope, not a community consensus.


## 4. Results

This section reports three pilots and a boundary run. Each subsection states, above its tables, the classification convention under which its classifications are scored, the effective witness set behind every count, and the two readings defined in Section 3.3: sender-relative violation (arm 1 denies, arm 5 admits) and receiver-relative novelty (arm 2 denies, arm 5 admits). All tables are generated from the frozen result artifacts and transcribe the artifact fields verbatim; the source line under each table names the file and fields from which every cell is drawn.

### 4.1 Pilot 1 — APC → TraceGrant (v2)

Pilot 1 is the first end-to-end pair of the program: a sender running APC narrows its authority and hands off to a receiver running TraceGrant. The pilot's purpose is to separate what crosses the seam cleanly from what does not, on 80 cases across seven arms — 40 attack and 40 benign cases per arm — with classifications scored under the frozen family-wide convention: the same reference rules applied to every arm on both sides of the handoff. Effective witness sets: the 40 attack cases are 10 templates × 4 attack parameters (8 runs each, attack and benign interleaved); and the 24 leak cases of the headline arm are 6 leak templates × 4 parameters — one design point per row, not 24 independent demonstrations. Under the two readings of Section 3.3, the pilot records 24/40 sender-relative violations (arm 1 denies, arm 5 admits) and 0/40 receiver-relative novelty (arm 2 denies, arm 5 admits), because arm 2 and arm 5 leak the same 24 cases. The zero is a statement about novelty, not about the absolute level of unauthorized admission. The pilot is a constructed case family rather than a benchmark, and no comparability with published benchmark numbers is claimed.

The division of labor between the two mechanisms is narrowed before the handoff, so the pair separates cases where a checkable fact exists on the receiving side from cases where no faithful record could make the fact checkable. What is checkable is denied. The four `resource_widen` attacks are dropped in every arm — including both standalone mechanisms (the sender and the receiver) — because the sender's scope meet holds on the resource side and the narrowed set, once crossed, lets any downstream check see the widened call for what it is. The resource clause of the scope-trust claim (H1 `REFINED`) is therefore **`UNTESTED`**, not refuted: the case set contains no resource-side trust failure to exercise, and a zero on a caught case is not evidence that the clause is false. The two representable attack classes inside the shared vocabulary — recipient substitution and the omitted-forbidden default — are caught (leaked 0) by mapping-side canonicalization and BIND constraints rather than by effect-time detection. They are caught-case and mapping-attribution findings, not silence instances; they do not support H3, and they are reported under H1 `REFINED` and the measured findings. The one seeded exception is the unsatisfiable-VERIFY template, treated as a completion-integrity boundary rather than an unauthorized-effect leak and also not an H3 instance.

What leaks is the unrepresentable. Six of the ten templates leak 4 cases each under the composed M0 arm — principal rebind, composition-history loss, repeated calls (4 cases but 6 unauthorized-effect events), budget reset, expired delegation, revoked envelope — for a total of 24 of 40 attack cases and 26 unauthorized-effect events, with confidential marker external effects recorded in 4 of those events. These are the fields of dynamic state, identity and freshness that the receiver's decision does not consume: some are absent from its vocabulary, some are carried but unread, and some are readable but not carried (Table 13). No decision on the receiving side reads them, so the same faithful transport that delivers resource scope correctly delivers nothing actionable about revocation or budget. Template-level leak counts and event counts are given in Table 5. Because the classes are aligned row-by-row with the six templates, the composition-type claim (H2 `SUPPORTED`) — that dynamic state, identity and freshness do not cross as actionable decision inputs and leak — is carried here with every count attached to its row; its cross-pair headline appears only in Section 4.3 and is not invoked in this section. Under the frozen family-wide convention, no Progent figure is used for comparison here; H6 is `REFINED` on the two measured receiving pairs, not on an external baseline: the pair similarity is partly construction-forced (Section 4.5).

Table 4 summarizes the per-arm outcomes.

**Table 4.** Pilot-1 arm outcomes (attack cases leaked, unauthorized-effect events, and benign false-denial cases per arm).

| Arm | Attack cases leaked | Unauthorized-effect events | Benign false denial cases |
|---|---:|---:|---:|
| `apc_alone` | 0 | 0 | 0 |
| `tracegrant_alone` | 24 | 26 | 0 |
| `apc_apc_preserved` | 0 | 0 | 0 |
| `apc_apc_reset` | 8 | 8 | 0 |
| `apc_tracegrant_scope_only` | 24 | 26 | 0 |
| `apc_tracegrant_retained` | 0 | 0 | 0 |
| `apc_tracegrant_fail_closed` | 0 | 0 | 20 |

*Reset-control note:* `apc_apc_reset` is the frozen same-mechanism reset control: 8 leak cases / 8 events on the shared 80 (composition 4, repeated 2, budget 2), identical to the frozen run's arm-4 cells.

**Receipt-failure note.** The standalone receiver recorded 4 receipt failures. `v2\raw_metrics.json` records `tracegrant_alone.receipt_failures = 4`; this control detail is not part of the 24/40 leak count and is not load-bearing for H2.

M0 is this program's one-step, transport-faithful bridge — a design choice of this implementation and not a defect of APC or of TraceGrant as published — and the composed arm with M0 (`apc_tracegrant_scope_only`) exhibits leak counts and event counts identical row-by-row to the standalone receiver in Table 5: the handoff does not add a dynamic-state leak class, it fails to remove the receiver's own. That identity is construction-forced and carries no evidential weight about composition (Section 4.5). The informative rows are the remaining arm comparisons. The arm that carries the sender's decision as an evidence record with a consistency digest (`apc_tracegrant_retained`, M2) shows 0 leaked attack cases and no false denials on the same case set. M2 did not sign the record: it was trusted harness input with a consistency digest. HMAC-signed M2-auth is introduced only in E1, and signature verification under a trusted key belongs to E1 M2-auth and to the SentinelAgent pair's arm 6. The 0/40 result therefore measures carriage of the upstream decision, not signature verification. The arm that instead refuses to translate what it cannot represent (`apc_tracegrant_fail_closed`) also shows 0 leaked cases, at a measured utility cost: 20 of 40 benign cases are falsely denied, in 28 distinct events.

Table 5 gives the leak-class structure.

**Table 5.** Leak-class table for the Pilot-1 family-wide arms (per-template leaked cases, unauthorized-effect events, and false-denial events, all under the frozen family-wide scoring convention).

| Template | `tracegrant_alone` leaked | `tracegrant_alone` unauthorized events | `tracegrant_alone` false denials | `apc_tracegrant_scope_only` leaked | `apc_tracegrant_scope_only` unauthorized events | `apc_tracegrant_scope_only` false denials | `apc_tracegrant_retained` leaked |
|---|---:|---:|---:|---:|---:|---:|---:|
| `resource_widen` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `principal_rebind` | 4 | 4 | 0 | 4 | 4 | 0 | 0 |
| `composition_history_loss` | 4 | 4 | 0 | 4 | 4 | 0 | 0 |
| `repeated_calls` | 4 | 6 | 0 | 4 | 6 | 0 | 0 |
| `budget_reset` | 4 | 4 | 0 | 4 | 4 | 0 | 0 |
| `expired_delegation` | 4 | 4 | 0 | 4 | 4 | 0 | 0 |
| `revoked_envelope` | 4 | 4 | 0 | 4 | 4 | 0 | 0 |
| `recipient_substitution` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `omitted_forbidden_default` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `unsatisfiable_verify` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The state/identity rows in Table 5 are the pilot's H3 observation, narrowed to a field-level account: silent non-enforcement, not crashes or misparses — the receiver admits these calls with no parse error, no gate code, and no effect-time detection, because the fact that should have been denied has no column in the receiver's decision. The broader claim that vocabulary gaps generally manifest as silence is not tested; the audited fields are set out in Table 13. The resource and caught-action rows are not H3 evidence.

**Worked numeric trace (Pilot 1; existing numbers only).** The ledger entry is 80 cases × 7 arms = 560 executions, with 40 attack cases per arm. Six leak templates × 4 attack parameters give the headline 24/40 leak cases; the per-template unauthorized-effect events are 4 + 4 + 6 + 4 + 4 + 4 = 26. The evidence-carriage arm records 0/40 leaks, and the fail-closed arm records 0 leaks with 20/40 benign false-denial cases and 28 false-denial events. Each value is the value already reported in this subsection and Tables 4–5; the trace introduces no new measurement.

### 4.2 Extension E1 and the resolving tests — the action family

Pilot 1 severe cases all sit on the state/identity side, so a second experiment asks the same question of a fact the receiver's vocabulary demonstrably does represent: the action. Extension E1 isolates one design point — a `send_external` call that is inside the sender's root set but outside the narrowed action set that crossed the seam — replicated across four attack cases on an axis the construction neutralizes (recipient value, budget); the four benign cases are context, and the effective sample size is 1 design point × 4 attack cases. The experiment spans 8 cases × 5 arms = 40 executions plus 6 control executions on a separate denominator (the 6 are counted in the 2,446 ledger but excluded from the 40-case E1 denominator), scored under the frozen family-wide reference convention. Under the two readings, E1 records 4/4 sender-relative violations; receiver-relative novelty is 0/4 under the frozen family-wide convention and 4/4 under the arm-native convention (Table 7). The reference oracle for this family is family-wide: it scores arm 2, which contains no handoff, against the handoff-derived norm — an authority-assignment convention for the standalone arm that is disclosed rather than hidden, and one that the first resolving test in this subsection re-scores.

The result decomposes transport from admission at the action field. The narrowed action set crosses the seam intact — the synthesized record in the composed arm carries exactly the narrowed set, `[read_public, save_internal]` — and the composed arm still admits the four attacks, 4/4, with 4 unauthorized-effect events; the record's action field is present in the snapshot and unread by the synthesis. This is the action-clause instance of the scope-trust claim (H1 `REFINED`), measured here: an authorization-carrying fact crosses the seam and a secondary receiving decision never reads it. In the frozen family-wide scoring the same 4/4 leaks appear in arm 2, which contains no handoff; the two M0 arms are scored identically and leak identically. The sender-relative reading is 4/4 in both conventions; the receiver-relative reading is 0/4 under the family-wide norm and 4/4 under the arm-native norm, because arm 2's own-world authority differs from the handoff-derived norm. The outcome matrix is given in Table 6; the four attack cases are `action_narrow-0-a` through `action_narrow-3-a`, and the four benign cases are `action_narrow-0-b` through `action_narrow-3-b` (arm mapping and case ids are also recorded in `v2\extension_e1\assertions.json` and `tests\seam_pilot_v2\design\extension_e1_cases.json`).

**Table 6.** E1 outcome matrix (per-arm attack leaks, unauthorized-effect events, benign false denials, and arm-6 signed-record verification on the 4 attack and 4 benign cases). Arm identifiers: arm 1 = `apc_alone`; arm 2 = `tracegrant_alone`; arm 5 = `apc_tracegrant_scope_only`; arm 6 = `apc_tracegrant_retained`; arm 7 = `apc_tracegrant_fail_closed`.

| Arm | Attack leaks | Unauthorized-effect events | Benign false denials | Arm-6 verified (8) |
|---|---:|---:|---:|---|
| 1 | 0/4 | 0 | 0/4 | n/a |
| 2 | 4/4 | 4 | 0/4 | n/a |
| 5 | 4/4 | 4 | 0/4 | n/a |
| 6 | 0/4 | 0 | 0/4 | `PROOF-GAP` after verify; 8/8 `EVIDENCE-VERIFIED` (report-only) |
| 7 | 0/4 | 0 | 0/4 | n/a |

Three mechanism-level facts sit alongside Table 6. First, the arm-5 confusion matrix on the eight-case family is TP `4`, FP `0`, FN `0`, TN `4` — precision `1.0`, recall `1.0` under this experiment's own contract. The matrix is construction-consistent rather than an independent estimate: the four attack cases are the cases built to be outside the narrowed action set, and the four benign cases are built to be inside it, so the scores record that the harness applied its own labels consistently. The substantive result is the admission pattern, not the precision/recall figure. This is a representable-but-unread consumption failure, reported under H1 `REFINED` and the formal core, not H3. Second, the evidence arm (`apc_tracegrant_retained`) denies all four attacks (`PROOF-GAP` after the shadow APC denies) while verifying the signed record on all four attack cases; the eight signed records across arm-6 runs — four attack and four benign — are all `EVIDENCE-VERIFIED`. This cell is report-only in the frozen metrics output — the raw field traces for signed-record admission codes are not stored in `v2\extension_e1\metrics.json`, and the count is carried from the frozen report's evidence-auth column (`v2\EXTENSION_E1_RESULTS.md` Section 3.4). Third, the three controls — `C-valid`, `C-mutated`, `C-replay` — each with a failure probe, pass 3/3 across 6 executions on their own denominator, all `lock_matches` true; they are not mixed into the 40-case run. The signing scheme is documented as HMAC-SHA256 over a canonical payload with a 56-byte key and is disclosed as a public test constant; the M2-auth arm assumes attestation is verified under the trusted key and does not establish authenticated transport. The dataset hash of the locked 8-case set is recorded in the E1 manifest as `1b7c6083ef22d40c8a0d3c3705357358b3508671bfbedc9db12f69a8b2e264ba` (design locks, not reseals).

Two pre-registered resolving tests then settle, respectively, where the action-clause violation is located and how the violation is repaired. Test 1 is scoring-only — zero new executions — and re-scores the four frozen arm-2 attack records against two authority conventions: the frozen family-wide handoff norm, under which arm 2 leaks 4/4, and the arm-native root norm, under which arm 2 leaks 0/4. On the same frozen records, the sender-relative count (arm 1 denies, arm 5 admits) is 4/4 under both conventions; the receiver-relative count (arm 2 denies, arm 5 admits) is 0/4 under the family-wide norm and 4/4 under the arm-native norm. The classification is therefore measured to be convention-dependent, and the convention-dependence is itself the finding: the composition-specific reading rests on the arm-native scoring of arm 2, which is the reading both resolving tests adopt going forward. Under that reading the action-family exception to the pair-similarity finding (H6 `REFINED`) is composition-specific: on this family, this arm, this mechanism — arm 1 denies, arm 2 is safe, arm 5 leaks, with no claim about other families. The seam test as operationalized here is a widening test; it can fire only where the composition widens, and a zero where the composition does not widen does not by itself establish composition-independence. Table 7 reports both tests.

**Table 7.** Resolving-test matrix for the E1 action family (scoring-sensitivity panel, Test 1; consumption-repair panel, Test 2). Panel labels: T1 = Test 1 (scoring sensitivity); T2 = Test 2 (consumption repair). T1 values are out of the 4 attack cases, shown as numerator/denominator.

| Panel | Test | Measured value |
|---|---|---|
| Scoring sensitivity (T1) | Arm-2 attack leaks under handoff norm (canonical) | 4/4 |
| Scoring sensitivity (T1) | Arm-2 attack leaks under root norm (arm-native) | 0/4 |
| Scoring sensitivity (T1) | Seam-test count under canonical scoring | 0/4 |
| Scoring sensitivity (T1) | Seam-test count under arm-native (root-norm arm-2) scoring | 4/4 |
| Consumption repair (T2) | Arm-5 attacks denied on action scope (`ACTION-SCOPE`) | 4/4 |
| Consumption repair (T2) | Arm-5 benign cases allowed | 4/4 |
| Consumption repair (T2) | Admitted calls with verifying receipt | 12/12 |
| Consumption repair (T2) | Arm-2 gate-outcome parity vs. canonical | 8/8 |
| Consumption repair (T2) | Arm-2 contract-digest parity vs. canonical | 8/8 |
| Consumption repair (T2) | Locked predictions matched (Test 1 + Test 2) | 10/10 |

Test 2 measures the repair (M0-A consumption rule): making the synthesized read set consume `snapshot.actions` denies all 4 attacks on action scope in the composed arm while allowing all 4 benign cases, with 12/12 of the admitted-call receipts verifying across the loop and 0 false denials anywhere, all under 16 sequential executions. The arm-2 control in the same loop — the same variant, cases scored against the same contract — is unchanged: gate outcome parity 8/8 with canonical, and the synthesized contract digests byte-identical on all 8 cases, so the variant changes admission handling only, not the M0 arm's own decisions. All 10 pre-registered predictions across the two tests match; the lock hash of the pre-registration is recorded in the artifact directory as `8cd4d9938348b43c7232eaa022280693d7e6f538c630d47f0c6d63bd996011ab`. This is the measured consumption-side instance of the formal core's repair rule (Section 3.2): the receiver must consume the narrowed action set it is handed; it is reported as measured, with no claim-ladder token, and it is not imported from a claim entry in this section.

**Test 2 runner-hash disclosure.** `dt\test2_manifest.json` records `runner_sha256_matches_mini_lock: false`. The earliest full run crashed while assembling the reconciliation after writing the test artifacts; the corrected runner re-ran the complete matrix. The mini-lock, cases, arms, and predictions were unchanged, and the manifest's `bookkeeping_note` records the deviation; no measurement or reported count changes.

Read together, Pilot 1 and the E1 resolving tests measure two loci. At the state/identity locus, the vocabulary gap is absolute and the leak count is the standalone count; sender-relative violations are 24/40 and receiver-relative novelty is 0/40. At the action locus, the sender-relative count is 4/4 under both conventions; the receiver-relative count is 0/4 under the frozen family-wide convention and 4/4 under the arm-native convention, and consumption — the receiver reading the fact it was already handed — closes the violation without disturbing the rest of the synthesis. Whether the action-family exception generalizes beyond this one family, and what other loci the second and third pairs expose, is deferred to Sections 4.3–4.5.

### 4.3 SentinelAgent pair — APC → SentinelAgent

The second receiving pair re-runs the composition program against SentinelAgent's delegation-token vocabulary: the locked bridge mints one delegation token per attempted call, and the receiving side executes the pinned prototype's own token checks; every classification in this subsection names its convention, which here is the pair's arm-invariant scoring: scopes are intersected with the receiving manifest and the composition term is applied to arm 2 as well, although arm 2's world contains no handoff; under a rescoping of the composition term to the handoff arms alone, the arm-2 `composition_history_loss` cells would read safe rather than leak, so the pair's arm-2 and arm-5 readings are one convention's readings. The witness structure is 12 templates × 8 runs, executed as 96 cases × 7 arms = 672 strictly sequential, offline, deterministic runs over 48 attack cases. Under the locked convention the pair records 28/48 sender-relative violations and 0/48 receiver-relative novelty, because arm 2 and arm 5 leak the same 28 cases. The self-review re-verified the lock and case-set hashes unchanged after the run and re-measured determinism with 20 re-executions and zero mismatches.

Under the locked convention the standalone receiving arm and the composed scope-only arm leak the same 28 of the 48 attack cases and emit the same 30 unauthorized-effect events. Their leak sets are identical by construction — same contract, same scoring, composition changing only which vocabulary handles the prelude calls — and we carry the identity as forced, not as evidence. The dynamic-state classes of the first pair repeat and dominate: 24 of the 28 leaks are principal/task identity (4 cases), composition history (4), repeated calls (4 cases with 6 events), cumulative budget (4), expiry (4), and revocation (4). This is the structural account for H3 `REFINED`: the audited state/identity aspects fail silently, but through three distinct loci — carried-but-unread (expiry), read-but-not-carried (revocation), and absent from the admission read set (principal/task, composition history, budget, replay). The original broad wording, that vocabulary gaps generally manifest as silence, is not tested; the field audit is Table 13. The remaining 4 signature-family leaks are not H3 evidence; they are treated under H5/H6 below. The receiver-relative seam test again returns zero under the locked conventions — no case is safe in both mechanism-alone arms and admitted under composition in this pair. The run's own integrity record is not uniformly green: the SentinelAgent manifest records `expected_vs_observed_ok = false`, and its metrics record `comparison.overall_ok = false`. The two failed checks are the false-denial-event lock (26 locked, 28 observed) and the arm-5 confusion true-negative denominator (68 locked, 20 observed on the attack-case basis); both are recorded verbatim in `sa\sa\reconciliation.json` with `affects_behavior_cells: false`, and Section 7.2 gives the full reconciliation. Neither changes a behavior cell or a reported leak count.

The two remediations carry measurable prices, and the pair headline is the frozen H2 claim: the repair is carrying the upstream decision, not a check inside the receiver's vocabulary (H2 `SUPPORTED`). In this pair the evidence arm records zero attack successes and zero false denials against the scope-only arm's 28 leaks. The fail-closed arm also records zero leaks, by refusing dynamic state it cannot translate, at a measured utility cost: 20 benign cases rejected and 28 false-denial events. The trust conditions are part of the finding: the evidence arm reads the signed attestation as verified under the trusted key, and the fail-closed arm accepts its 20 benign refusals deliberately — both scoped design choices of the mapping, neither claimed production-safe. H6 `REFINED` reads the same evidence pair-wise: within the measured pairs, the state/identity leak shapes are similar, but the similarity is partly an artifact of shared case templates and shared scoring; it is not a general cross-pair law. The differences that exist are remediation mechanics — signed attestation here, digest-only evidence carriage and receipts in the first pair — plus the one new standalone class the token ecosystem contributes, described below. Table 8 gives the per-template observations behind this paragraph.

**Table 8.** SentinelAgent pair, per-template outcome cells for the four arms that consume the token vocabulary (arm 2 `sentinelagent_alone`, arm 5 `apc_sentinelagent_scope_only`, arm 6 `apc_sentinelagent_retained`, arm 7 `apc_sentinelagent_fail_closed`): leaked cases, false-denial counts (`false_denials`), leak events. The arm-7 `false_denials` cells are per-template artifact values and are non-additive: they sum to 26, while the arm-level `false_denial_events` field is 28. The two additional events are the second-call `repeated_calls` events recorded in the reconciliation; the cells are artifact-faithful and do not sum to the arm-level total. Columns are arm number plus metric: leak = leaked cases; FD = false-denial count; ev = leak events; `*` marks the non-additive arm-7 FD count. Template identifiers are shown with spaces in place of underscores.

| template | 2 leak | 2 FD | 2 ev | 5 leak | 5 FD | 5 ev | 6 leak | 6 FD | 6 ev | 7 leak | 7 FD* | 7 ev |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| resource widen | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| principal rebind | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| composition history loss | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |
| repeated calls | 4 | 0 | 6 | 4 | 0 | 6 | 0 | 0 | 0 | 0 | 6 | 0 |
| budget reset | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |
| expired delegation | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |
| revoked envelope | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |
| recipient substitution | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omitted forbidden default | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| unsatisfiable verify | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| foreign key signed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| keyholder widen | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |

**Reconciliation note (SentinelAgent, arm 7).** The verbatim fields in `sa\sa\reconciliation.json` for item `arm7_false_denial_events` are: `locked`: 26; `observed`: 28; `locked_note`: "FD events = 20 benign dynamic refusals + 4 unsatisfiable_verify-a + 2 oracle-clean first calls of repeated_calls-a"; `explanation`: "The lock's derivation enumerated only 'first calls' of repeated_calls-0-a and -3-a (2 events), but each case produces two FD events: under the locked FD definition (oracle-clean AND denied AND not a signature rejection) the second call is also an FD because the refused first call never executes, leaving the oracle budget unconsumed; the shadow APC then denies the second call (SHADOW-DENY) after charging its own budget on the first approval. Observed events: repeated_calls-0-a ev0 T1-REFUSE:dynamic_state_untranslated / ev1 SHADOW-DENY; repeated_calls-3-a identical. The locked definition yields 28; only the derivation undercounted."; `seam_effect`: "none"; `affects_behavior_cells`: false.

**Reconciliation note (SentinelAgent, arm 5).** The verbatim fields in `sa\sa\reconciliation.json` for item `arm5_confusion_true_negative_denominator` are: `locked`: 68; `observed_attack_case_denominator`: 20; `observed_all_cases_denominator`: 68; `explanation`: "The lock's confusion block used the all-96-cases denominator for TN (48 benign + 20 caught attacks), while the metrics code computes TP/FP/FN/TN over the 48 attack cases (TN = 16 rejected + 4 allowed-no-effect). TP/FP/FN are 28/0/0 either way; counts agree: 28+20=48, 28+68=96. Denominator slip in the lock's block, recorded, not edited."; `seam_effect`: "none"; `affects_behavior_cells`: false.

The signature family is this pair's measurement of H5, and its first end-to-end test. Its witness structure is 2 pairs × 4 document parameters × 2 variants = 16 cases (8 attack, 8 benign), each executed across the 4 token arms. A token whose content would pass the checks but which is signed with the prototype's published key constant instead of the trusted harness key is rejected `SIGNATURE_INVALID` — 4 rejections per token arm, and not counted as a false denial under the locked scoring rule. Verification without the key cannot admit; verification with the key attests something narrower than authority. Delegate-minted tokens are admitted exactly like bridge tokens wherever the prior authorization is not restored, and a control presenting identical tokens attributed to two distinct minters returns identical codes. Within the token vocabulary, any keyholder is to the receiver equivalent to the issuer, and the frozen wording of H5 `REFINED` states the measured boundary for this pair: a validly-signed token attests to integrity and key possession, not source of authority — scoped to this pair, with the trust-boundary caveat that the pair exercises one prototype, one key model, one case family, and the "or a call to the DAS" alternative was not exercised end-to-end. The same property generates the pair's one new leak class: `keyholder_widen`, in which a caller-held delegate writes a manifest containing the widened resource and the token arms admit it 4/4 — a token-ecosystem standalone class (H6 `REFINED`) rather than a composition failure, and the observation that makes key distribution the critical interface of this seam.

Ten controls pass across the family — signature-validity failure probes, foreign-key rejection, two-minter indistinguishability, attestation tamper and replay — showing the checks are neither vacuous in the admit direction nor no-ops in the deny direction. Across the 7-arm, 96-case matrix, 756 evaluated events decompose exactly as 756 = 488 admissions + 150 token-attached denials + 118 denials without a token key. The 150 token-attached denials are 40 native P6/P7 denials, 42 attestation-stage denials in arm 6, and 68 pre-presentation refusals in arm 7. Of the 488 admissions, 230 carry no token key. The non-vacuity count is 638 = 488 + 150; the 118 denials without a token key are outside it. Table 9 reports the per-template codes; the ten controls follow.

**Table 9.** SentinelAgent signature family - per-template codes and leaks in the four token arms. Arm 2 = standalone; arm 5 = scope-only; arm 6 = retained signed attestation; arm 7 = fail-closed shadow deny. Cells are code x4 / leaked cases; `SIG-INVALID` abbreviates `SIGNATURE_INVALID`.

| template | kind | arm 2 | arm 5 | arm 6 | arm 7 |
|---|---|---|---|---|---|
| foreign_key_signed | attack | SIG-INVALID x4/0 | SIG-INVALID x4/0 | SIG-INVALID x4/0 | SIG-INVALID x4/0 |
| trusted_key_signed | benign | ADMITTED x4/0 | ADMITTED x4/0 | ADMITTED x4/0 | ADMITTED x4/0 |
| keyholder_widen | attack | ADMITTED x4/4 | ADMITTED x4/4 | APC-DENY x4/0 | SHADOW-DENY x4/0 |
| keyholder_plain | benign | ADMITTED x4/0 | ADMITTED x4/0 | ADMITTED x4/0 | ADMITTED x4/0 |

The ten controls, with expected and observed results:

- `S1-valid` — expected p6=ALLOWED by scope; p7=OUTPUT_ALLOWED; observed\
  p6=ALLOWED by scope:read_confidential; p7=OUTPUT_ALLOWED.
- `S1-failure` — expected p6=SIGNATURE_INVALID; p7=SIGNATURE_INVALID; observed the same.
- `S1-probe` — expected p6=TOKEN_REVOKED; p7=TOKEN_REVOKED; observed the same.
- `S2-foreign` — expected p6=SIGNATURE_INVALID; p7=SIGNATURE_INVALID; observed the same.
- `S2-trusted` — expected p6=ALLOWED by scope; p7=OUTPUT_ALLOWED; observed\
  p6=ALLOWED by scope:read_confidential; p7=OUTPUT_ALLOWED.
- `S2-two-minters` — expected p6_both=ALLOWED by scope; p7_both=OUTPUT_ALLOWED;\
  codes_identical=true; observed bridge\
  p6_bridge=ALLOWED by scope:read_confidential; p7_bridge=OUTPUT_ALLOWED; delegate\
  p6_delegate=ALLOWED by scope:read_confidential; p7_delegate=OUTPUT_ALLOWED;\
  codes_identical=true.
- `S2-mutated` — expected p6=SIGNATURE_INVALID; p7=SIGNATURE_INVALID; observed the same.
- `S3-valid` — expected gate=ALLOWED; tamper=ATT-SIG-BAD; observed gate=ATT-OK; tamper=ATT-SIG-BAD.
- `S3-mutated` — expected gate=ATT-SIG-BAD; probe=APC-DENY; observed the same.
- `S3-replay` — expected gate=ATT-BIND-MISMATCH; probe=ALLOWED; observed gate=ATT-BIND-MISMATCH; probe=ATT-OK.

ATT-SIG-BAD = ATTESTATION-SIGNATURE-INVALID; ATT-BIND-MISMATCH = ATTESTATION-BINDING-MISMATCH; ATT-OK = ATTESTATION-OK, the attestation stage's allow code (the `ALLOWED` entries in the expected column denote the same outcome).

### 4.4 Boundary — non-narrowing-preserving bridge variants (V1/V2)

The boundary run asks the reversed question: not whether a faithful bridge drops facts, but what happens when the bridge's own manifest derivation is not narrowing-preserving. Two derivations answer it. V1 derives the receiving manifest from the delegate's pre-narrowing role scope rather than the post-handoff effective scope; V2 fills an omitted-recipient default into the manifest's SEND endpoint (`forbidden-default@example.test`). Neither derivation consumes a fact the sender conferred; both widen. Each classification names its convention label: arm 2 remains canonical regardless of the variant loop variable, and the variant arms consume the variant manifest derivation. The boundary records 4 new sender-relative cases per variant; receiver-relative novelty is 4/4 against the canonical receiver and 0/4 against the variant receiver, so the new cases are bridge-attributable. The run executes 6 arms × 2 variants × 96 cases — 1,152 strictly sequential runs, 96 rows per arm-variant cell; 7 controls pass, and the self-review records `ok` with the harness and case-set hashes unchanged, while the boundary lock hash is recorded in `manifest.json.lock`. Its attack structure is deliberately thin: 1 design point × 4 cases per variant — the four `resource_widen` attacks under V1, the four `omitted_forbidden_default` attacks under V2 — so its 8 attack cases in total are not 8 independent designs.

Both derivations produce the predicted widening, with and without composition. Under V1 the composed arm leaks the 4 `resource_widen` attacks, among them the widened resource `docs:external/secret`, which the canonical arm 2 blocks; under V2 the composed arm leaks the 4 `omitted_forbidden_default` attacks. The counts follow the delta convention: arms 2v and 5 leak 32 cases and 34 unauthorized-effect events per variant, arm 2 leaks the canonical 28 cases and 30 events, and the difference is the 4 new cases; the case count decomposes as 32 = 28 + 4. The 32/32 identity between arm 2v and arm 5 is an identity of leak sets, not a claim that all 96 cases leak. Arm 1 leaks none in either variant. The receiver-relative seam counts follow the same shape: 4 per variant against canonical arm 2. Because the standalone variant arm 2v leaks the identical set per variant — forced by construction, not evidence — the seam test fires, but its firing carries no composition-specific witness. The informative contrasts are canonical arm 2, safe on the variant cases, against composed arm 5, leaking them; and arm 2v, leaking, against arm 2, safe.

The attribution is measured, in the frozen wording: the failure is the bridge's manifest derivation, not composition. The receiver cannot recover a fact the derivation did not narrow — the frozen derivation-side clause. The claim readings move accordingly. H1 `REFINED`: the bridge's manifest derivation extends scope trust — the receiver reads the signed manifest as authority — and the refinement lands on the derivation layer. H2 `SUPPORTED` is unchanged: V1 and V2 add no new dynamic-state class, and their new leaks are scope/manifest-derivation classes. These are derivation-widening findings under H1 `REFINED` and H6 `REFINED`, not H3: both mismatches are faithful to what the bridge wrote into the manifest — a role scope exceeding the root grant under V1, a default-filled send endpoint under V2. H5 `REFINED` now covers the keyholder property at the bridge/manifest layer: a bridge holding the key can write a widened manifest or a default-filled endpoint, and the receiver admits what it verifies. H6 `REFINED`: a bridge-design artifact, not a composition-specific failure.

Arms 6 and 7 suppress the widened calls rather than repair them. The evidence arm denies the 4 variant cases as `APC-DENY` per variant, with zero leaks; the fail-closed arm denies them as `SHADOW-DENY` ×4 per variant, with zero leaks and its measured cost of 20 benign false denials and 28 false-denial events. No benign case is falsely denied in arms 1, 2, 2v, 5 or 6, and the no-divergence control (CV1b) confirms the variant manifests match canonical on the benign cases that should not diverge. The missing step is not receiver consumption here; the derivation is at fault.

The receiver-relative zero survives, bounded. It is a property of narrowing-preserving mappings (canonical T0) on the frozen case sets and does not extend to non-narrowing-preserving derivations (Section 3.2). The run's manifest check is narrow, recorded verbatim: `expected_vs_observed_ok = true` checks the seam count only (Table 11 note). One locked statement was overbroad and is reconciled rather than edited (Table 10 note): arm 2 was stated as safe on all cases, and it is safe on the variant-specific cases per variant while carrying the pre-existing canonical leak set elsewhere. Finally, V1 and V2 are two derivations tested in one pair's token vocabulary; they are not asserted to be typical, nor the only or most likely bridges. Table 10 gives the absolute-plus-delta matrix and Table 11 the seam counts.

**Table 10.** Boundary absolute-plus-delta matrix — per arm-variant cell: leak cases, leak events, benign false-denial cases, false-denial events, and variant-template leak cases (the `resource_widen` template under V1, the `omitted_forbidden_default` template under V2).

| arm::variant | leak cases | leak events | benign FD cases | FD events | variant-template leak cases |
|---|---|---|---|---|---|
| apc_alone::v1 | 0 | 0 | 0 | 0 | 0 |
| apc_alone::v2 | 0 | 0 | 0 | 0 | 0 |
| sentinelagent_alone::v1 | 28 | 30 | 0 | 0 | 0 |
| sentinelagent_alone::v2 | 28 | 30 | 0 | 0 | 0 |
| sentinelagent_alone_variant::v1 | 32 | 34 | 0 | 0 | 4 |
| sentinelagent_alone_variant::v2 | 32 | 34 | 0 | 0 | 4 |
| apc_sentinelagent_scope_only::v1 | 32 | 34 | 0 | 0 | 4 |
| apc_sentinelagent_scope_only::v2 | 32 | 34 | 0 | 0 | 4 |
| apc_sentinelagent_retained::v1 | 0 | 0 | 0 | 0 | 0 |
| apc_sentinelagent_retained::v2 | 0 | 0 | 0 | 0 | 0 |
| apc_sentinelagent_fail_closed::v1 | 0 | 0 | 20 | 28 | 0 |
| apc_sentinelagent_fail_closed::v2 | 0 | 0 | 20 | 28 | 0 |

**Reconciliation note (boundary, arm 2).** The verbatim fields in `b\reconciliation.json` for item `arm2_canonical_leak_scope_overstated` are: `locked`: "boundary_condition.md and boundary_lock.json expected_per_arm_variant: sentinelagent_alone (arm 2, canonical) predicted 0 leaks / safe on all cases, for both v1 and v2"; `explanation` (excerpt): "The lock's 'arm 2 = 0 leaks / safe on all cases' overstated the prediction. … The variant-specific prediction holds: arm 2 safe on the variant cases; arm 5 leaks them; arm 2v leaks them standalone."; `resolution`: "recorded in reconciliation only; lock and artifacts unmodified; the variant-specific predictions (arm 2 safe on resource_widen / omitted_forbidden_default; arm 5 leaks them; arm 2v leaks identically standalone) all hold".

**Table 11.** Boundary seam counts per variant — the seam-test fields of the run manifest.

| variant | arm 1 leaks (`arm1_leaks`) | seam cases (`seam_cases`) | seam count (`seam_count`) |
|---|---|---|---|
| v1 | none | resource_widen-0-a, resource_widen-1-a, resource_widen-2-a, resource_widen-3-a | 4 |
| v2 | none | omitted_forbidden_default-0-a, omitted_forbidden_default-1-a, omitted_forbidden_default-2-a, omitted_forbidden_default-3-a | 4 |

*Note:* the manifest field `expected_vs_observed_ok = true` covers the seam count only (`seam_count == 4`).

### 4.5 Cross-cutting synthesis

The cross-cutting claim is a refinement, not a universal zero. Two readings are reported for every set: sender-relative violation (arm 1 denies, arm 5 admits) and receiver-relative novelty (arm 2 denies, arm 5 admits). Table 12 collects the counts; Table 13 audits the state/identity fields; Table 14 states the claim statuses.

**Table 12.** Two readings of the seam test — sender-relative violation and receiver-relative novelty, by experiment set.

| Experiment set | Attack cases | Sender-relative violation (arm 1 deny ∧ arm 5 allow) | Receiver-relative novelty (arm 2 deny ∧ arm 5 allow) | Construction note |
|---|---:|---:|---:|---|
| Pilot 1 (APC → TraceGrant) | 40 | 24/40 | 0/40 | arm 2 and arm 5 leak the same 24 cases; the identity of leak sets (24/24 cases, 26/26 events) is forced by shared contract and scoring |
| SentinelAgent pair | 48 | 28/48 | 0/48 | arm 2 and arm 5 leak the same 28 cases; the identity (28/28) is forced |
| E1, family-wide scoring | 4 | 4/4 | 0/4 | arm 2 leaks 4/4 under the handoff norm |
| E1, arm-native scoring | 4 | 4/4 | 4/4 | arm 2 is safe (0/4); the only genuine composition-specific test in the program |
| Boundary V1, canonical arm 2 | 4 variant attacks (96-case matrix) | 4 new / 4 variant attacks (32/96 total) | 4 new / 4 variant attacks | arm 2v leaks the same 4 new cases; receiver-relative novelty against arm 2v is 0, so the 4 new cases are bridge-attributable |
| Boundary V2, canonical arm 2 | 4 variant attacks (96-case matrix) | 4 new / 4 variant attacks (32/96 total) | 4 new / 4 variant attacks | arm 2v leaks the same 4 new cases; receiver-relative novelty against arm 2v is 0, so the 4 new cases are bridge-attributable |

*Notes:* Counts are attack-case counts, not execution counts; the 2,446-execution ledger is Table 3. "0/40" and "0/48" are novelty zeros, not zeros of sender-relative violation. For the boundary, the canonical receiver (arm 2) denies the four variant attacks, so the canonical-receiver novelty is 4/4; the variant receiver (arm 2v) leaks the same four, so the composition-specific novelty is 0/4. The two readings are both reported; the second is the one that attributes the failure to the bridge.

The first two rows carry the program's main negative result: the composed arms commit sender-relative violations on 24/40 and 28/48 attacks, but they add no receiver-relative novelty, because the standalone receivers leak the same calls. The zero is a statement about composition, not about safety: the sender's narrowing is not enforced, and the receiver is already unsafe on its own. The two pair-pilot zeroes — Pilot 1 and the SentinelAgent pair — are construction-forced identities of arm 2 and arm 5; they carry no evidential weight about composition. The E1 family-wide zero is a third pair-level zero, but it is convention-dependent rather than construction-forced: the same records give 4/4 under arm-native scoring. The boundary's composition-specific zero is a separate identity between arm 2v and arm 5, and the four new cases per variant are bridge-attributable. E1 is the only genuine composition-specific test in the program: arm 2 is safe under arm-native scoring, arm 5 admits 4/4, and the consumption repair reverses the admission pattern. Its result is one design point × four attack cases and is convention-dependent.

**Table 13.** Field-level audit of state and identity at the seam. Leak counts are the frozen per-template counts; the read-set column is from the pinned receiver code, not from the record's field list.

| Set | Field / aspect | Receiver representation | Admission reads it? | Bridge carries it? | Observed leak (arm 5) | Locus |
|---|---|---|---:|---:|---:|---|
| E1 (APC → TraceGrant) | action scope | snapshot `actions` | no (synthesis ignores it) | yes | 4/4 | carried but unread |
| SA | resource | token `manifest` ops | yes (P6 manifest match) | yes | 0/4 (`resource_widen`) | representable and read |
| SA | expiry | token `expiry` (signed) | no (P6 checks signature, revocation, manifest; not expiry) | yes, from snapshot status | 4/4 (`expired_delegation`) | carried but unread |
| SA | revocation | token `revoked` (not in canonical signature) | yes (P6 checks `revoked`) | no (bridge mints `revoked=False`) | 4/4 (`revoked_envelope`) | read but not carried |
| SA | principal / task | token `src`/`dst`, `intent_text`; not an admission input | no | partial (labels, not decision input) | 4/4 (`principal_rebind`) | absent from read set |
| SA | composition history | `parent_hash` (one-hop, not reconstructed) | no | no | 4/4 (`composition_history_loss`) | absent from read set |
| SA | budget | none | no | no | 4/4 (`budget_reset`) | absent |
| SA | replay state | none | no | no | 4/4 cases, 6 events (`repeated_calls`) | absent |
| SA | signature / key possession | token `signature` | yes | yes | 0/4 foreign key; 4/4 `keyholder_widen` | H5 boundary, not H3 |

*Note:* The table separates three failure loci that the original H3 wording grouped together: a field can cross and not be read (expiry; E1 action), be readable and not cross (revocation), or be absent from the receiver's vocabulary altogether (principal/task, composition history, budget, replay). The audit covers the fields exercised by the frozen templates; it is not a complete inventory of either mechanism.

Table 14 collects the claim ladder as this section measures it: each row carries its refined status, its locus, and the artifact evidence a reader can re-derive; the formal core, the extension's exception, and the boundary result are labeled measured.

**Table 14.** Claim-locus synthesis — refined statuses, section loci, and re-derivable evidence.

| claim / finding | status | locus | evidence (artifacts and cross-references) |
|---|---|---|---|
| H1 scope trust (action clause measured; resource clause `UNTESTED`; manifest-derivation clause measured) | REFINED | Sections 4.1, 4.2, 4.4 | `v2\raw_metrics.json` (`per_template.resource_widen.leaked`); `v2\extension_e1\metrics.json` (arm 2/5 leak fields); `dt\test1_rescored_arm2.json` (`counts`, `seam_test`); `b\metrics.json` (variant arms) |
| H2 dynamic state, identity, freshness do not cross as actionable inputs and leak | SUPPORTED | Sections 4.1, 4.3, 4.4 | `v2\raw_metrics.json` (`tracegrant_alone`, `apc_tracegrant_retained`); `sa\sa\metrics.json` (`sentinelagent_alone`, `apc_sentinelagent_retained`); `b\metrics.json` |
| H3 state/identity gaps manifest as silent non-enforcement, field-level | REFINED | Sections 4.1, 4.3, 4.5 | Table 13; `v2\raw_metrics.json` (`per_template.principal_rebind`, `per_template.composition_history_loss`, `per_template.repeated_calls`, `per_template.budget_reset`, `per_template.expired_delegation`, `per_template.revoked_envelope`); `sa\sa\metrics.json` (per-template fields); `tests\seam_pilot_sentinelagent\adapters\sa_harness.py` (`expiry_for`, `make_token`); `tests\sentinelagent_audit_20261014\upstream\sentinelagent_das_prototype.py` (P6) |
| H5 verification attests integrity and key possession, not authority | REFINED | Sections 4.3, 4.4 | `sa\sa\controls.json`; `b\metrics.json`; `b\manifest.json` |
| H6 pair-wise failure shapes; similar within measured pairs, partly construction-forced; E1 exception | REFINED | Sections 4.1, 4.2, 4.3, 4.4, 4.5 | `v2\raw_metrics.json`; `sa\sa\metrics.json`; `b\metrics.json`; `dt\REPORT.md` Sections 1–3 |
| ★ receiver-relative novelty zero under narrowing-preserving mappings on the frozen cases; sender-relative violations remain; two of three pair-level zeroes forced; E1 exception | REFINED | Section 4.5 | Table 12; `sa\SA_RESULTS.md` Section 1; `v2\EXTENSION_E1_RESULTS.md` Section 3.3; `b\manifest.json` (`seam_test.v1.seam_count`) |
| Zero-seam conditionality (cross-cutting finding) | measured — no status token | Section 4.5 | Section 3.2; `dt\REPORT.md`; `b\manifest.json` (`seam_test`) |
| E1 action-family exception (cross-cutting finding) | measured — no status token | Sections 4.2, 4.5 | `dt\test1_rescored_arm2.json` (`counts.arm2_attack_leaks_handoff_norm`, `counts.arm2_attack_leaks_root_norm`, `seam_test`); `dt\test2_metrics.json`; `dt\REPORT.md` Section 3 |
| Boundary bridge-layer attribution (cross-cutting finding) | measured — no status token | Sections 4.4, 4.5 | `b\metrics.json` (`sentinelagent_alone_variant::*`, `apc_sentinelagent_scope_only::*`); `b\reconciliation.json` item `arm2_canonical_leak_scope_overstated` |
| Repair patterns (cross-cutting finding) | measured — no status token (instance claims carry their own statuses) | Sections 4.1, 4.2, 4.3, 4.4, 4.5, 5 | Table 15; `dt\test2_metrics.json`; `sa\sa\metrics.json`; `v2\raw_metrics.json` |
| Keyholder finding (cross-cutting finding) | carried under H5 REFINED | Sections 4.3, 4.4 | `sa\sa\controls.json`; `b\metrics.json`; `b\manifest.json` |
| Formal core (blindness observation; seam proposition; repair rule) | definitional observation; measured proposition clauses — no status token | Sections 3.2, 4.5 | definitions and observation in Section 3.2; measured instances in Sections 4.2–4.4 |

**Artifact-root abbreviations for Table 14 (display-only).** `v2`, `dt`, `sa`, and `b` are defined in Section 3.5. Full paths remain in the artifact tree.

**Legacy-evidence note.** `v2\claims_update.md` is a legacy-key record. Its old-H6 block compares a local Task B fixture to Progent, is labeled directional-only, and is not used as evidence or as a baseline in this paper. The current H6 reading rests on the measured receiving pairs; Appendix Table A1 records the label lineage.

Table 14 is the claim ladder as this section measures it. The ★ row is `REFINED`, not `SUPPORTED`: the zero is a recorded property of narrowing-preserving mappings on the frozen cases, the two pair-pilot zeroes are construction-forced, and the only composition-specific test is the E1 action family. The H6 row is `REFINED` for the same reason: pair similarity is partly an artifact of shared templates and scoring. The H3 row is `REFINED` to the audited fields: the field audit separates carried-but-unread, read-but-not-carried, and absent, and the broad vocabulary-gap law is not tested. H1's resource clause is `UNTESTED`, not refuted. H2 and H5 keep their statuses within their scopes.

The formal core (Section 3.2) supplies the vocabulary for these observations: the blindness observation is definitional, and the seam proposition's clauses are measured rather than proved. The observation says that if the receiver's admission depends on the call only through its read-set projection, and no value in that read set separates the narrowed set from its complement on a call pair, then no admission function over the read set can enforce the narrowing on that pair; its corollary is the program's aphorism, carried but unread = uncarried (for decision purposes). The measured instances recur with effective n attached: in E1, the narrowed action set crossed the seam intact and the synthesis did not read it, and the consumption repair reversed the counts (Section 4.2, Table 7); in the SentinelAgent pair, the state/identity aspects fail through the three loci in Table 13, with the witness set 6 leak templates × 4 parameters = 24 attack cases of 48; in the boundary run, the widened manifest is admitted by the receiver standalone and composed — the bridge wrote the widened scope, so there is no consumption failure to repair at the receiver, and the derivation is the fault.

Those instances motivate the two repair loci. Receiver side, when the fact crossed intact: carry the upstream decision as evidence — signed attestation in the SentinelAgent pair, where the evidence arm eliminates all 28 leaks while recording no false denials itself; HMAC-signed M2-auth in E1, where the scheme denies 4/4 attacks; digest-only evidence carriage in Pilot 1 — or retain the upstream denial, as the fail-closed arms do at their measured benign costs (Table 15) — with consumption, not carriage, as the part that enforces. Derivation side, when the bridge itself widened: fix the manifest derivation at the bridge, so that the derivation preserves the narrowing. Figure 2 places the two loci in one picture.

![**Figure 2.** Where the decision can be rescued — the two repair loci of the seam program (schematic; no data). The upper band traces one delegated call through the pipeline these runs instrument: sender narrowing, bridge translation, the carried record, the receiver's read set, and the admission decision. Locus A sits at the receiver's admission step and applies when the narrowed fact crossed intact: consumption of the carried fact (the extension's mini-run) and evidence carriage of the upstream decision (digest-only in Pilot 1; signed in the SentinelAgent pair and E1 M2-auth), with the fail-closed refusal drawn as the measured fallback and its benign cost disclosed. Locus B sits at the bridge's derivation step and applies when the bridge itself widened: a narrowing-preserving manifest derivation, since no receiver-side consumption can recover a fact the bridge did not narrow. The annotation `carried but unread = uncarried` labels the gap between the carried record and the receiver's read set; Locus B points to the bridge-translation step, and Locus A points to that gap. Content is definitional-plus-measured (Section 3.2; the measured repair instances above); the figure carries no numbers and asserts no statuses.](figures/figure_2_repair_loci.pdf){#fig:figure2 width=7.0in}

No unconditional reading is available from these runs, and each sentence above is bounded the way its evidence is: by its scoring convention, by its case set, and by the trust model of the arm it describes. The two-count reading is the paper's main methodological correction: a zero in receiver-relative novelty is not a zero in sender-relative violation, and the difference is where the repair question lives.

## 5. Discussion — when seams add authority; repair patterns

**The practical question.** This section answers two questions the program was built to answer: when does a composed arm admit a call the sender's narrowing denies, and when does composition add an admission beyond what the standalone receiver already exhibits? The anatomy is the familiar one: a sender narrows authority, a bridge translates the narrowed decision plus state into a receiver-side record, and the receiver decides from that record. No party owns the seam. The measured answer is bounded: the composition-specific case is one family (the E1 action family), one scoring convention (arm-native), and the frozen case sets; the sender-relative violations are broader (24/40 and 28/48) but are not composition-specific. It is not a general claim about seams, and no production-safety claim is made for any repair arm. Every positive sentence below is conditional on the frozen mappings, case sets, and scoring conventions.

**Where the composed arm alone admits.** On the E1 action family, under arm-native scoring, the violation exists only in the composed arm. Arm 5 (M0 from the post-handoff snapshot) leaks `send_external` on 4/4 attacks, 4 unauthorized-effect events in total. Arm 1 (APC after the narrowed handoff) denies 4/4 with APC reason `action send_external not in scope`. Arm 6 (M2-auth signed evidence) denies 4/4 with `PROOF-GAP`, and all 8 signed records verify `EVIDENCE-VERIFIED` (report-only; Section 4.2). Arm 7 (shadow denial retained) denies 4/4. Benign calls are allowed 4/4 in every arm, zero false denials. The attributable locus is the receiver's synthesis: arm 5's snapshot carries the narrowed action set `actions = [read_public, save_internal]` yet M0 never consumes the action field — carried but unread is uncarried for decision purposes (Section 3.2). Under the frozen family-wide convention the arm-2 and arm-5 leaked sets are identical; under arm-native scoring arm 2 is safe and that identity no longer holds. The family-wide identity is forced by construction and carries no evidential weight about composition; it is disclosed as a convention, not evidence. This is precisely the blindness observation's measured instance (Section 3.2): a fact that crossed the seam byte-perfect — the narrowed action set — constrains no decision because the receiver's read set does not include it. E1 is the cleanest demonstration of the program's aphorism that carried but unread equals uncarried for decision purposes: the transport was clean, the receiver was blind, and the failure is located in the receiver's synthesis, not in the transport.

**Composition-specific on one family.** Under arm-native scoring on both arms — each arm scored by the authority its own world confers — arm 2 is safe on all 4 attacks and arm 5 leaks 4/4, so the receiver-relative count is 4/4. Under the frozen family-wide convention the same records give 0/4 receiver-relative novelty; the sender-relative count is 4/4 under both. The difference is the scoring convention, and that dependence is disclosed. Test 1 (scoring-only re-analysis, zero new executions) showed arm 2 safe against its own world's root authority (0/4 leaks under the root norm) while the frozen handoff-norm scoring kept the 4 leaks; the receiver-relative count is 4/4 under arm-native scoring and 0 under the family-wide convention. Test 2 resolves attribution positively with execution: an M0 variant whose admission rule consumes `snapshot.actions` denies all 4 attacks with gate code `ACTION-SCOPE`, allows all 4 benign cases, verifies 12/12 receipts, and leaves the arm-2 control unchanged — 8/8 gate-outcome parity, 8/8 byte-identical contract digests, 10/10 locked predictions matched. Consumption, not carriage, is enforcement: the receiver must read the narrowed fact, not merely receive it. The `ACTION-SCOPE-ABSENT` fail-closed branch (missing or empty action field) was not exercised in this family because every snapshot carries a non-empty action set; it remains untested here.

**Repairs.** Four loci follow: three receiver-side (evidence carriage, retain the upstream denial, consumption) plus the derivation-side rule from Section 3.2 (Figure 2).

*Evidence carriage (receiver).* When the fact crossed intact, carrying the upstream decision as evidence closes the measured leaks. In the SentinelAgent pair, arm 6 (signed attestation) closes all 28 baseline leaks with 0 leaks and 0 false denials. In E1, arm 6 (M2-auth) denies 4/4 attacks; all 8 signed records verify `EVIDENCE-VERIFIED` (report-only). In Pilot 1, arm 6 carries the decision as a digest-only record and closes the 24/40 baseline leaks. The caveat is load-bearing: the signed arms assume the attestation is verified under the trusted key, and M2-auth narrows tamper and replay but does not establish authenticated transport — the signer is the same harness that was the original trust anchor, and any holder of the public test key can mint valid records. Evidence carriage is therefore a fix only relative to a correctly deciding upstream: had the upstream APC admitted a widened scope, M2 would admit it too.

*Retain the upstream denial (receiver).* Keeping the sender's denial closes leaks at a measured utility cost. Pilot 1 arm 7 (fail-closed): 0 leaks on 40 attack cases, 20/40 benign false-denial cases, 28 false-denial events. SA arm 7: 0 leaks, 20 benign false-denial cases, 28 false-denial events. Boundary arm 7 (fail-closed): 0 leaks, SHADOW-DENY on the 4 seam cases per variant, 20 benign FD cases / 28 FD events. The utility cost is real: legitimate benign tasks are refused, and the cost is measured rather than asserted. Neither arm 6 nor arm 7 is production-safe; both are scoped design choices.

*Consumption (receiver).* Merely carrying the fact without reading it does not enforce. E1 Test 2: 4/4 attacks denied on `ACTION-SCOPE`, 4/4 benign allowed, 0 false denials, arm-2 control byte-identical — the narrowing-preserving meet's receiver-side half (Section 3.2). The general rule is to make the sender's boundary readable at the receiver and then read it: deny when the action snapshot is absent or empty (fail-closed), deny when the requested tool is outside the carried action set, otherwise run the unchanged synthesis. Evidence carriage is the transport; consumption is the enforcement.

*Derivation-side narrowing-preserving meet (bridge).* When the bridge itself widened the manifest (V1/V2), no receiver-side rule can recover a fact never narrowed. Boundary arm 5 leaks 32 cases / 34 events, which decompose as 28 pre-existing canonical leaks plus the 4 new cases per variant (32 = 28 + 4); standalone arm 2v leaks the identical 4 per variant; canonical arm 2 is safe on the variant-specific cases; arms 6/7 suppress APC-DENY / SHADOW-DENY ×4 per variant; seam count 4 per variant. Composition neither creates nor removes the failure: the identical admissions appear standalone in the variant arm. The fault is the bridge's manifest derivation — V1 widens role scope beyond root R, V2 default-fills the SEND endpoint — so the repair belongs at the bridge, not the receiver. Fix the derivation at the bridge.

**Keyholder finding (H5).** Signature verification attests key possession and payload integrity, not who minted the record; any keyholder is equivalent to the issuer within the token vocabulary. This holds for delegate-minted tokens — `keyholder_widen` admitted 4/4 in arms 2/5 — and for the bridge's own manifest derivation (V1/V2). SA signature controls: 4 `SIGNATURE_INVALID` per token arm for foreign-key probes; all 10 controls passed. Key distribution is the seam's critical interface: integrity plus key possession is not source of authority, so trusting a signature is not the same as trusting the minter.

**Positioning.** This paper offers two deliverables: a replication package and a repair taxonomy. The package contains the frozen case sets, harnesses, locks, and the locked-prediction protocol so that an independent reader can re-run the measurements; it is a release candidate, not a conformance service, certification, or benchmark, and it reports what a mapping carries rather than fixing it. The design rule is narrowing preservation at the mapping layer, with the measured receiver-locus repair (consumption) applied when the fact crossed intact and the bridge-level fix (derivation) applied when it did not. A broader expansion is a post-workshop decision, never a commitment made here. No roadmap; no production-safety claim.

**Statuses.** H1 `REFINED`; H2 `SUPPORTED`; H3 `REFINED`; H5 `REFINED`; H6 `REFINED`; ★ `REFINED`.

**Disclosures.** Receiver-relative novelty zero holds only for narrowing-preserving mappings (canonical T0) on the frozen case sets, with the exception and the bridge artifacts disclosed. Sender-relative violations are 24/40 and 28/48 and are not zero. The two pair-pilot zeroes are construction-forced; E1 is the only genuine composition-specific test, and it is convention-dependent (family-wide 0/4 vs arm-native 4/4), one family, 1 design point × 4, widening-only operationalization caveat. H1's resource clause is `UNTESTED`; H3 is field-level; H6 pair similarity is partly construction-forced. Arm 6 assumes attestation verified under the trusted key; arm 7 accepts 20 benign false denials; neither arm is production-safe; M2-auth does not establish authenticated transport. No claims beyond the frozen sets.

Table 15 collects the repair loci with their measured results.

**Table 15.** Repair patterns — four repair loci with measured results.

| Repair locus | Repair | Measured result |
|---|---|---|
| (a) receiver-side evidence carriage | carry upstream decision as evidence (digest-only in Pilot 1; signed in SA and E1 M2-auth) | Pilot 1 arm 6: 0 leaks (24/40 baseline closed), 0 false denials; SA arm 6: 0 leaks (all 28 baseline leaks closed), 0 false denials; E1 arm 6 M2-auth: 4/4 denied |
| (b) receiver-side retain the upstream denial | retain upstream denial (fail-closed / shadow deny) | Pilot 1 arm 7: 0 leaks; 20 benign FD cases; 28 FD events; SA arm 7: 0 leaks; 20 benign FD cases / 28 FD events; boundary arm 7: 0 leaks; SHADOW-DENY ×4 per variant; 20 benign FD / 28 FD events |
| (c) receiver-side consumption | consume narrowed action fact before admission | E1 Test 2: 4/4 attacks denied `ACTION-SCOPE`; 4/4 benign allowed; 12/12 receipts; arm-2 parity 8/8, digests 8/8; 10/10 predictions |
| derivation-side rule | narrowing-preserving meet at bridge | Boundary arm 5: 32 cases / 34 events = 28 pre-existing + 4 new per variant (32 = 28 + 4); standalone arm 2v leaks identical 4 per variant; seam count 4 per variant |

## 6. Related work

**Purpose.** This section positions the work against the three upstream approaches' own guarantees, as already reported in Section 2 and not re-measured here; the standards and authorization systems that supply the vocabulary of attenuation, evidence, and relationship-based policy; the 2026 agent-delegation line that proposes compositional authorization for agents; two close related works (Progent and MasDrift); and the industry/standards pointers carried from the frozen claim set. It reports no new results; guard language applies to others' numbers throughout. There are no tables and no figures in this section.

**Upstream formal spines.** APC's “Composition Soundness” (Thm 4.7) is intra-session composition of action sequences, conditional on a complete effective restriction set, serialized admission, and static X — a within-mechanism guarantee, not a cross-mechanism composition guarantee. TraceGrant's soundness is assumed (Eq. 10), not proven. SentinelAgent's Thm 4 is composition safety for two chains that both satisfy P1–P7 within its own framework; it does not cover a chain handed to a different mechanism's decision procedure. Each guarantee stops at its own boundary. This paper's narrowing-preservation rule plus the blindness observation (Section 3.2) addresses the question the three guarantees leave open: the moment authority crosses from one mechanism's vocabulary into another's. No upstream mechanism is claimed broken or failing; all upstream figures remain their authors' self-reports, and "reports" is the operative word, never "achieves".

**Industry / standards landscape.** These are pointers only; their bibliographic identities were checked, but their claims are unverified and none is treated as a verified fact. Noma (Apr 2026) is cited as an adjacent industry framing of inter-agent trust at handoffs; the IETF draft (revised Aug 2026) is cited as a related cross-domain authorization-sharing proposal. Neither is a measurement of the specific cross-mechanism translation gap this program instruments, and neither is adopted here as a result or a fix. arXiv 2605.05440 is cited as a related reference in the same area. None of these is a benchmark, a reproduced result, or a verified input to this manuscript; each citation is a pointer whose claims were not reproduced, and the frozen claim set governs if any pointer differs from it.

**Standards and credential vocabularies.** RFC 8693 defines OAuth 2.0 token exchange, including delegation and impersonation semantics for security tokens; RFC 9396 defines rich authorization requests, which carry fine-grained authorization data as structured `authorization_details`. Together they standardize how authority is requested and exchanged across domains, but neither specifies whether a receiver's admission reads the narrowed fact after the exchange. Macaroons make attenuation explicit through contextual caveats, and RFC 2693 specifies SPKI certificate structures for authorization and key distribution, including certificate chains. These are the established vocabularies for expressing, attenuating, and certifying authority; the seam measured here is the translation step between such a credential and a heterogeneous receiver's local decision. They are cited for definitions and contrast only, not as baselines.

**Systems and foundations.** Miller's object-capability analysis treats composition and confinement as properties of how authority is held and passed; Blaze, Feigenbaum, and Lacy frame trust management as the joint evaluation of policy, credentials, and trust; Appel and Felten's proof-carrying authentication makes the client carry evidence that the server checks before admission. Fong's relationship-based access control derives decisions from relationships and policy, and Zanzibar evaluates relationship tuples against a consistent, global authorization graph. These lines answer how to express, confine, attest, or derive authority. This paper asks a narrower question: whether a cross-mechanism handoff consumes the facts that carry the narrowing. None is re-implemented, reproduced, or used as a baseline.

**Recent agent-delegation work.** A 2026 line proposes compositional authorization and delegation mechanisms for agents. The least-autonomy theory of Parisel argues that per-action permission bounds are insufficient when actions can be combined, and formalizes a compositional blast radius and a collusion predicate over an agent influence graph. ChainCaps enforces monotonic capability attenuation across tool composition and names permission laundering as the failure mode. Overlaying Governance supplies a compositional delegation-and-scope framework that overlays agentic semantics onto relational policies. Local Allow, Global Deny proves that per-action authorization does not compose for relational policies, characterizing compositional authorization failures as 2-safety hyperproperties that no per-trace monitor detects. These works propose theories, mechanisms, frameworks, or impossibility results. None reports a cross-mechanism measurement of whether a heterogeneous receiver's admission reads the narrowed fact, which is the question here. They are positioning anchors, not baselines; no number is compared, and no novelty claim is made over them.

**Progent (reference only).** Progent is cited as a close related work on monotonic confinement inside a single privilege-control layer. No Progent figure is reproduced, re-measured, or compared here; the paper uses no Progent number as evidence, and no Progent result is treated as an input or a baseline. The word is “reports,” never “achieves”; Progent is cited as a reference only.

**MasDrift (related work).** MasDrift studies authorization preservation across multi-agent coordination architectures using benign productivity tasks [MasDrift]. Our narrower question concerns executions through two specific public authorization artifacts and their argument-binding paths; the small deterministic matrix is a conformance study, not an architecture benchmark and not a substitute for MasDrift's broader evaluation. No MasDrift number is reproduced, re-measured, or compared.

**Disclosures.** Others' numbers stay self-reported. Nothing claims APC, TraceGrant, SentinelAgent, Progent, or MasDrift is broken or fails; no vulnerability in any upstream mechanism as published is claimed. No production-safety claim; no benchmark comparability. No claims in this section go beyond the frozen sets. The industry/standards pointer set (Noma, the IETF draft, arXiv 2605.05440) is described as pointers, not verified facts. The standards, systems, and 2026 agent-delegation anchors are cited for definitions, contrast, and positioning only; none is a baseline, a reproduced result, or a verified input. No result in this paper depends on any of their claims.

**Scope of positioning.** The reference list is a positioning sample, not a survey: it covers the three measured formal spines, the standards and systems that define the relevant vocabulary, the closest 2026 agent-delegation work, the two nearest empirical relatives, and the industry pointers already in the frozen claim set. It does not attempt a comprehensive survey of delegation, capability, or policy literature, and no novelty claim is made over the uncited literature. A comparative treatment against any of these systems would require running it under a common lock with the same case families; none is run here, and none of their numbers is reproduced.

## 7. Threats to validity

This section states what the measured program does not claim: the construct limits of the case sets, the internal limits of the reconciliation record, and the external limits of interpretation. Two hypotheses remain open as future instruments; every other limitation is a plain disclosure, not a softened claim. Table 16 maps each threat to the section that raises it.

### 7.1 Construct threats

The case sets are constructed witnesses, not benchmarks. The first pilot family is 10 templates × 8 runs and the SentinelAgent family is 12 templates × 8 runs, each written for this program and frozen before any run. Their structure, not their scale, is what licenses a reading: the E1 extension rests on a single design point with a neutralized parameter axis, measured as 1 design point × 4 attack cases, and the boundary run rests on two design points, each 1 × 4 cases — 8 attack cases in total, which are not 8 independent cases.

Convention dependence is a construct threat as much as a disclosure. The E1 receiver-relative count is 0/4 under the frozen family-wide convention and 4/4 under the arm-native convention; the sender-relative count is 4/4 under both. The convention was locked and disclosed, not chosen after the fact. SentinelAgent scoring is arm-invariant, and rescoping it would flip `composition_history_loss` arm 2 from leak to safe. At the boundary, arm 2 is always canonical regardless of the variant loop variable while the variant arms use the variant manifest derivation, so the identity of arm 2v with arm 5 per variant is forced by construction. The composed arm's absolute count is accordingly 32 = 28 + 4 — the pre-existing canonical set plus the per-variant new cases. Three forced identities — Pilot 1 arm 2 ≡ arm 5 at 24/24 leaked cases and 26/26 events, SentinelAgent arm 2 ≡ arm 5 at 28/28 leaked cases, and boundary arm 2v ≡ arm 5 at 32/32 leaked cases per variant — are identities of leak sets, not claims that every case leaks; they carry no evidential weight about composition and are labeled forced.

Two operational caveats complete the construct picture. As operationalized, the E1 seam test can fire only where the composition widens: a zero where it does not does not by itself establish composition-independence, and the same caveat may attach to the original pilots' seam test, which was not re-verified on that point. Separately, arm 2's authority assignment in E1 is a disclosed convention — the own-world norm is the one discriminating Test 1 adopts, and under the alternative reading the same records locate the failure in the mapping's authority assignment, still not in a mechanism interaction. The field-level audit in Table 13 is limited to the fields exercised by the frozen templates; it is not a complete inventory of either mechanism.

### 7.2 Internal threats

The reconciliation record is part of the evidence and was never edited. Within the SentinelAgent reconciliation, the two checks that failed are recorded verbatim: false-denial events locked as 26 and observed as 28, and the arm-5 confusion true-negative denominator locked as 68 and observed as 20 on the attack-case basis. Both carry `affects_behavior_cells: false` in that record, which is why they change no outcome cell and remain on file. At the boundary, the reconciliation records `expected_vs_observed_ok` as a scope check — it verifies the manifest's expected seam count and nothing beyond it — and the canonical arm-2 leak scope was carried as overstated: 0 in the locked reading against 28 pre-existing observed cases.

Two constraints limit the repair results from inside. Arm 7's shadow-denial action rule (`tool not in snapshot.actions`) was not independently exercised: the retained shadow denial fired first in all four E1 attacks. And M2-auth does not establish authenticated transport — the key is a public test constant, the signer is the same harness that was the original trust anchor, and there is no forger control. On the trust side, arm 6 assumes the attestation is verified under the trusted key and arm 7 accepts 20 benign false denials; neither repair arm is claimed production-safe, and neither should be read as one. The E1 precision and recall figures are construction-consistent, not independent estimates: the attack and benign labels are the same construction that generates the cases.

### 7.3 External threats

V1/V2 are plausible bridge designs; they may be mis-designs, and they are not asserted to be typical, the only, or the most likely bridges. No generalization beyond the frozen case sets is claimed. No vulnerability is claimed in APC, TraceGrant, or SentinelAgent as published: the measured findings are properties of this implementation under the locked bridge mappings and key models, and the upstream mechanisms' own evaluations remain their authors' self-reports; this manuscript reports those self-reports and assesses none of those systems. No comparability with published benchmark numbers is claimed, neither theirs against this program's counts nor this program's against theirs. Finally, the zero-novelty statement — composed arms adding no receiver-relative admission beyond the receiver's own, under narrowing-preserving mappings (canonical T0) on the frozen case sets, with the E1 exception and the bridge artifacts disclosed as measured — has the standing of a recorded property of every case built, not a theorem. Sender-relative violations are not zero: the composed arms admit 24/40 and 28/48 calls the sender's narrowing denies in the two pair pilots.

**Design-space rationale.** The program holds the sender fixed at APC and varies the receiver across two vocabularies: TraceGrant's action-scope records and SentinelAgent's state/identity records. That one-factor design is deliberate. It isolates receiver-side consumption from sender-specific quirks and keeps the seam test comparable across pairs. The two receivers were selected for vocabulary contrast and public availability, not as a representative sample of authorization mechanisms, and the two bridge variants are this program's own designs. What travels beyond these cases is the measurement instrument — the seam predicate, the two readings, and the repair taxonomy — not the measured rates. A different sender, receiver, bridge, or case family would require its own lock, predictions, and reconciliation; a production deployment would add transport, key management, and policy factors that this matrix holds out.

### 7.4 The not-claimed canon

The frozen not-claimed list is restated here by group, without softening and without upgrading.

Scope of the experiments. Not claimed: bridges beyond V1/V2 — the two variants are this program's own constructed designs, and typicality is not asserted. Not claimed: generalization beyond the frozen case sets, whose witness sets are as stated in Section 7.1. Not claimed: comparability with published benchmark numbers, since the case sets are constructed here and upstream evaluations are self-reported by their authors. Not claimed: that the zero-novelty result generalizes beyond these pilots' case families; it is a recorded property of every case built, not a theorem. Not claimed: that receiver-relative novelty zero means sender-relative safety — the sender-relative violations are reported separately, at 24/40 and 28/48.

Upstream mechanisms. Not claimed: any vulnerability in APC, TraceGrant, or SentinelAgent as published; the findings are properties of this implementation under the locked bridge mappings and key models.

Repair patterns. Not claimed: production safety of arms 6 or 7 — arm 6 assumes the attestation is verified under the trusted key, and arm 7 accepts 20 benign false denials; both are scoped design choices. Not claimed: authenticated transport for M2-auth — the key is a public test constant, the signer is the same harness, and no forger control exists. Not claimed: arm 7's shadow-denial action rule was independently exercised — it was not, because the retained shadow denial fired first. Not claimed: that the replication package is a conformance service, certification, or benchmark; it is a release candidate containing frozen case sets and harnesses.

Conventions. Not claimed: convention-invariance of the seam test — the counts differ under frozen family-wide scoring versus arm-native scoring (0 versus 4/4 for receiver-relative novelty), and the canonical disclosure is unchanged and remains accurate. Not claimed: rescoping-neutrality of SentinelAgent scoring, which is arm-invariant and would flip `composition_history_loss` arm 2 from leak to safe under rescoping. Not claimed: boundary-convention invariance — arm 2 is always canonical regardless of the variant loop variable, and arm 2v matches arm 5 per variant by construction. Not claimed: that the seam test as operationalized measures more than where the composition widens; a zero where it does not would not by itself establish composition-independence. Not claimed: an unchallenged authority assignment for arm 2 in E1 — the own-world norm is a disclosed convention.

Hypotheses. Not claimed: that H3 is a general law of vocabulary gaps; the carried claim is the field-level account in Table 13, limited to the audited fields. Not claimed: that H6 is a general pair-similarity law; the similarity within the measured pairs is partly construction-forced, and the E1 action family is a composition-specific exception. Not claimed: that H1's resource clause is false; it is `UNTESTED`, because the `resource_widen` cases are caught in every arm and do not exercise a resource-side trust failure. Not claimed: that H3 covers caught representable cases, the E1 action-family consumption failure, or the V1/V2 derivation widening; those are reported under H1/H6 and the measured findings, not H3.

Open hypotheses. Not claimed here: the shared-audit-trail hypothesis and the intent-layer hypothesis — carried below as unbuilt instruments, not as findings and not as claims.

### 7.5 Two hypotheses carried open

**H4 — `UNTESTED`.** This is an unmeasured surface, not a demonstrated failure: H4's claim is that there is no shared audit trail across the mechanisms — the SHA-256 evidence chain on the sender-mechanism side, the receiver's receipts, and the hash-linked tokens are three separate provenance records, and this hypothesis is not tested in any pilot. The SentinelAgent tokens in the runs are one-hop, each parent hash resolving to the root, so no chain reconstruction and no cross-mechanism trail interchange was exercised in either the SentinelAgent pilot or the boundary run. The next instrument is identified but not built here: a case family that reconstructs authority from a token hash chain and compares it with the APC envelope's history. Nothing adjacent is imported into this claim.

**H7 — `UNTESTED`.** The intent layer of the SentinelAgent pair, its principle P2, may be gameable through benign-word override, and this was not tested: P2's `intent_text` was carried in the run records but never classified, and neither the E1 extension nor the boundary run exercised it. No probing instrument is introduced in this paper, and the hypothesis stands as open.

**H4/H7 gate.** Neither hypothesis was exercised in this revision: no H4 or H7 experiment was designed, locked, or executed, and no result for either appears anywhere in this paper. Both remain `UNTESTED`; a future test would require a new pre-registered lock, a case set, and its own reconciliation before it could be reported. No claim in this paper depends on H4 or H7.

**Table 16.** Threat ledger — each threat and the section that raises it.

| Threat | Raised in |
|---|---|
| Bridges beyond V1/V2 out of scope; V1/V2 not asserted typical | Section 7.3 |
| Production safety of the repair arms not claimed | Sections 7.2, 7.4 |
| Shared audit trail and intent layer carried open, not claimed | Section 7.5 |
| Generalization beyond the frozen case sets not claimed | Sections 7.1, 7.4 |
| No vulnerability claim about the upstream mechanisms as published | Sections 7.3, 7.4 |
| Comparability with published benchmark numbers not claimed | Sections 7.3, 7.4 |
| The zero-novelty result is a recorded property, not a theorem | Sections 7.3, 7.4 |
| Sender-relative violations are not zero; the two readings differ | Sections 4.5, 7.4 |
| Family-wide versus arm-native convention dependence | Sections 7.1, 7.4 |
| SentinelAgent arm-invariant scoring; rescoping flip | Sections 7.1, 7.4 |
| Boundary arm-2 canonical convention; forced arm-2v identity | Sections 7.1, 7.4 |
| M2-auth does not establish authenticated transport | Sections 7.2, 7.4 |
| Arm 7's shadow-denial action rule not independently exercised | Sections 7.2, 7.4 |
| E1 seam test operationalized only where the composition widens | Sections 7.1, 7.4 |
| Arm-2 authority assignment as a disclosed convention | Sections 7.1, 7.4 |
| H1 resource clause is UNTESTED, not refuted | Sections 4.1, 7.4 |
| H3 is field-level, not a general vocabulary-gap law | Sections 4.3, 4.5, 7.4 |
| H6 pair similarity is partly construction-forced | Sections 4.5, 7.4 |
| E1 precision/recall are construction-consistent, not independent | Section 7.2 |
| Replication package is not a conformance service or certification | Sections 5, 7.4, 8 |

## 8. Reproducibility and artifacts

This section describes the replication package prepared as a release candidate — the program's practical deliverable at workshop stage. It is protocol description only: what was frozen, what was locked, and what was re-verified. It carries no result claims, and it is not a conformance service, certification, or benchmark.

### 8.1 What the package contains and how it was run

The package contains the four frozen experiment sets — the two pair pilots, the action-clause extension with its resolving tests and controls, and the boundary run — as runnable case sets with their harnesses under the locked-prediction protocol. Predictions, cases, arms, and locked input hashes were frozen before execution; the one recorded harness-hash deviation is Test 2's runner hash, disclosed in Section 4.2; executions were strictly sequential, offline, and deterministic; discrepancies between predicted and observed values were reconciled verbatim into files that were never edited after the fact; and each published number was generated from the artifacts and embedded byte-verbatim. The execution ledger records the scale: 2,446 = 560 + 40 + 6 + 16 + 672 + 1,152.

Re-execution discipline is part of the package. The SentinelAgent program recorded determinism reruns of 20 executions with 0 mismatches, and its control battery passed 10/10; the boundary run's control battery passed 7/7. The controls exist so that a reader can check claims about repair results before trusting them. Scoping limits are carried with the package as well: there is a single implementation per repair pattern, so each repair measurement is scoped to its own implementation; the package reports what a mapping carries and does not fix anything; and sanitization and cleanup of the release tree remain pending. The package is a release candidate, not a public release: repository URL, license, DOI, and archival location are not yet assigned. It is not a conformance service, certification, or benchmark, and no third party has run it.

### 8.2 The artifact hash ledger

Table 17 lists six frozen addresses; two are also quoted in the text, and the table is not a complete hash inventory. The numbers in this paper are traceable through the artifact tree to the artifacts that generated them. Table 17 transcribes the frozen addresses for the E1 dataset, the discriminating-tests lock, the SentinelAgent lock and case set, and the boundary lock and harness, in each case from the frozen source map that records each value and its artifact root.

**Table 17.** Artifact hash ledger — frozen lock/case/harness hashes.

| Artifact | Frozen hash |
|---|---|
| E1 dataset (canonical `dataset_sha256`) | `1b7c6083…b2e264ba` |
| Discriminating lock (file SHA-256) | `8cd4d993…996011ab` |
| SA lock (file SHA-256) | `9f2611a1…65d47f0` |
| SA cases (file SHA-256) | `ca2f05d5…e42cb6d2` |
| Boundary lock (file SHA-256) | `b4deab1a…082c4296` |
| Boundary harness (file SHA-256) | `fa8f7e42…790814af4` |

*Note:* row 1 is the canonical dataset hash recorded in the E1 lock; rows 2–6 are file SHA-256 values. The table is a citation aid, not a complete hash inventory.

**Suffix note.** Displayed hashes are variable-length truncations; row 3 uses a 7-character suffix and row 6 uses a 9-character suffix. Full 64-character values are in the ancillary `hashes.txt`.

## 9. Conclusion

This paper asked a narrow question about a broad practice: when one authorization mechanism narrows a decision and hands it to another through a bridge, what crosses, and what can the receiver no longer derive? The question matters because the composed pair's decision is what executes, while each mechanism's own guarantee — conditional on its own envelope, its own contracts, its own static assumptions — stops at the handoff that nobody owns.

The method was chosen to make the answer auditable rather than merely reported. Predictions, case sets, arms, and hashes were locked before any run; executions were sequential, offline, and deterministic; mismatches were reconciled verbatim; and every published number was generated from the artifacts. Four experiment sets put 2,446 = 560 + 40 + 6 + 16 + 672 + 1,152 executions behind the measured statements below.

The measured answer is conditional, and its conditions are part of the answer. The composed arms commit sender-relative violations on 24/40 and 28/48 attacks in the two pair pilots, but the standalone receivers admit the same calls, so receiver-relative novelty is zero; the two pair-pilot zeroes are construction-forced. The one genuine composition-specific test is the E1 action family: 4/4 sender-relative violations, 0/4 receiver-relative novelty under the frozen family-wide convention, 4/4 under arm-native scoring, with a consumption repair that denies 4/4 attacks and allows 4/4 benign calls. The exception is one design point × four attack cases and is convention-dependent. At the boundary, two non-narrowing-preserving bridge designs produced four new cases per variant that appear identically in the standalone variant arm — a bridge-design artifact, not a composition-specific failure. The keyholder caveat stands: a signature verifies integrity and key possession, not the source of authority. Every positive sentence here is conditioned on the frozen sets, the locked mappings, and the scoring conventions under which the counts were produced.

The practical deliverable is the replication package of Section 8: frozen case sets, harnesses, and the locked-prediction protocol, packaged so that an independent reader can re-run the measurements. It is a release candidate, not a conformance service or certification. The package reports; it does not fix.

What remains open is stated in Section 7 as unbuilt instruments rather than findings: no shared audit trail has been measured across the mechanisms, and the sentinel pair's intent layer has not been probed. The closing status of the measured program is: H1 `REFINED` (action clause measured; resource clause `UNTESTED`; manifest-derivation clause measured), H2 `SUPPORTED`, H3 `REFINED` (field-level), H5 `REFINED`, H6 `REFINED`, and ★ `REFINED` for the zero-novelty finding — with the two open hypotheses above carried forward as instruments, not claims — H4 `UNTESTED`, H7 `UNTESTED`.

Continuation beyond the workshop decision point is not a commitment made here; any expansion is a post-workshop decision taken on its own evidence.

## Declarations

**Data availability.** The counts reported here are generated from the frozen artifact tree described in Section 8. The replication package is a release candidate: public archiving is pending, and no repository URL, DOI, license, or archival location is asserted because none has been assigned. The frozen case sets, harnesses, locks, and reconciliation records remain available for inspection on request to the author, subject to the release gates in Section 8. No new data were generated for this revision.

**Ethics.** No human-subjects data were collected. The experiments are synthetic and offline, and no personally identifying data were processed. AI-assisted tools were used for implementation and quality assurance; their roles are described in Section 3.7. No AI system is an author, and the author remains responsible for all claims, artifacts, and errors.

**Author contributions (CRediT).** The manuscript is single-authored. Prathamesh N. Patil is the sole author and is responsible for all claims, artifacts, and errors. CRediT roles are not asserted in this revision; a final role statement is pending author confirmation.

**Competing interests.** No competing interests are declared in this revision. A final competing-interest confirmation is pending before submission; no financial or non-financial interest is asserted.

**Funding.** No funding source is declared in this revision. A final funding statement is pending before submission; no grant, sponsor, or institutional support is asserted.

**Limitations.** The claims are limited to the frozen case sets, mappings, and scoring conventions in Section 3 and the threats in Section 7. The case sets are constructed witnesses, not benchmarks; the E1 result is one design point × four attack cases; the boundary run has two design points; the two pair-pilot zeroes are construction-forced; and no production-safety or generalization claim is made. H4 and H7 remain `UNTESTED`. The replication package is a release candidate, not a public conformance service.

## Appendix A. Hypothesis lineage and operationalization

The frozen experiment artifacts predate the current hypothesis key, and some labels changed meaning between the pilot records and this manuscript. Table A1 records the lineage so that a legacy label is not read as the current label with the same number. It is provenance, not evidence, and it changes no status.

**Table A1.** Hypothesis lineage — legacy artifact labels, their operationalizations, and the current manuscript labels.

| Legacy artifact label | Legacy operationalization | Current manuscript label | Status / provenance |
|---|---|---|---|
| H1 (all artifact sets) | Receiving mechanism re-derives scope or trusts the already-authorized caller | H1 | `REFINED`; action and manifest-derivation clauses measured; resource clause `UNTESTED` |
| H2 (all artifact sets) | Dynamic state, identity, and freshness do not cross and leak | H2 | `SUPPORTED`; unchanged label |
| H3 (v2 only) | VERIFY postconditions are an admission/completion boundary | No direct current-H3 equivalent; historical completion-integrity finding | Reported under H1/H6 and the measured findings, not current H3. `v2\claims_update.md` H3; `raw_metrics.json` `unsatisfiable_verify` |
| H4 (v2 only) | Mapping choices decide whether a failure is a mechanism property or an artifact | No direct current-H4 equivalent; historical mapping-attribution finding | Reported under H1 `REFINED` and the measured findings, not current H4. `case_generator.py` tags recipient/default cases old H4; those are caught-case evidence, not current H3 or H4 |
| H6 (v2 only) | Comparison with the Progent reference numbers | No current-H6 equivalent; current H6 is similar-pair vs dissimilar-pair failure shapes | Historical, directional-only Progent block; not used as a comparison or baseline. Current H6 rests on the SA/boundary measurements and is `REFINED` |
| H3–H6 (SA/boundary) | Vocabulary mismatch; no shared audit trail; verification gap; similar/dissimilar failure shapes | H3–H6 | H3 `REFINED` (field-level, Table 13); H4 `UNTESTED`; H5 `REFINED`; H6 `REFINED` |
| H7 (manuscript only) | Intent layer P2 | H7 | `UNTESTED`; `intent_text` carried but never classified |

The frozen artifacts are not edited; this table is the reconciliation. In particular, recipient/default cases tagged old H4 in `tests\seam_pilot_v2\design\case_generator.py` are caught-case evidence and are not current H3 or current H4 evidence.

**Status changes from the pre-review draft.** H3 moved from `SUPPORTED` to `REFINED` because the field audit separates carried-but-unread, read-but-not-carried, and absent, and the broad vocabulary-gap law is not tested. H6 moved from `SUPPORTED` to `REFINED` because pair similarity is partly construction-forced. ★ moved from `SUPPORTED` to `REFINED` because the two pair-pilot zeroes are forced and E1 is the only composition-specific test. H1's resource clause moved from "not supported" to `UNTESTED` because the `resource_widen` cases are caught in every arm and do not exercise a resource-side trust failure. No frozen artifact was edited.

**Table A2.** Effective witness sets behind the reported counts — executions, case structure, and independent design points.

| Experiment set | Executions | Cases | Attack cases | Effective independent witness | Construction note |
|---|---:|---:|---:|---|---|
| Pilot 1 (v2) | 560 | 80 = 10 templates × 8 runs (40 attack + 40 benign) | 40 = 10 templates × 4 parameters | 6 leak templates × 4 parameters = 24 headline leak cases; one design point per template row | The 24/40 headline counts template cases, not 24 independent designs. |
| E1 extension | 46 = 40 + 6 control | 8 = 4 attack + 4 benign | 4 = 1 design point × 4 cases | 1 design point × 4 attack cases | Recipient and budget axes neutralized; the four attacks are replicates of one design point. |
| Discriminating Test 1 | 0 new | 4 frozen arm-2 attack records | 4 | 1 scoring comparison (family-wide versus arm-native) over 4 cases | Scoring-only re-analysis; no new executions. |
| Discriminating Test 2 | 16 | 8 = 4 attack + 4 benign; 2 arms | 4 = 1 repair design × 4 cases | 1 repair design × 4 attack cases | Consumption repair; arm-2 control 8/8 gate and digest parity. |
| SentinelAgent pair | 672 | 96 = 12 templates × 8 runs (48 attack + 48 benign) | 48 = 12 templates × 4 parameters | 6 state/identity leak templates × 4 = 24 of 48; signature family 16 = 2 pairs × 4 document parameters × 2 variants | The 28/48 headline is 24 state/identity leaks plus 4 signature-family leaks. |
| Boundary V1/V2 | 1,152 | 96 rows per arm-variant cell; 6 arms × 2 variants | 8 = 2 design points × 4 cases | 1 design point × 4 cases per variant; 2 design points total | Four new cases per variant; not 8 independent designs. |
| **Total** | **2,446 = 560 + 46 + 0 + 16 + 672 + 1,152** | — | — | — | E1's 46 includes its six control executions, as in Table 3. |

*Note:* every cell restates a design fact already stated in Sections 3.5 and 4.1–4.4; the table introduces no new measurement and no new count. Executions are matrix runs; the control and replay records excluded from the 2,446 total remain as stated in Section 3.5.

**Path notation.** The roots `v2`, `dt`, `sa`, and `b` are defined in Section 3.5; full paths remain in the artifact tree.

## References

\raggedright

**[APC]** Xabier Muruaga. *Bounded Agents: Delegation Security for Multi-Agent AI Systems.* arXiv:2608.15888v1, 16 August 2026. DOI: 10.48550/arXiv.2608.15888. <https://arxiv.org/abs/2608.15888>.

**[TraceGrant]** Bohao Liao, Jingchao Wang, Qipeng Song, Jin Cao, Jieling Wang, and Boyu Deng. *TraceGrant: A Contract-Governed Security Framework for the Task-Effect Lifecycle of Networked LLM Agents.* arXiv:2608.21126v1, 21 August 2026. DOI: 10.48550/arXiv.2608.21126. <https://arxiv.org/abs/2608.21126>.

**[SentinelAgent]** KrishnaSaiReddy Patil. *SentinelAgent: Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems.* arXiv:2604.02767v1, 3 April 2026. DOI: 10.48550/arXiv.2604.02767. <https://arxiv.org/abs/2604.02767>.

**[Progent]** Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, and Dawn Song. *Progent: Securing AI Agents with Privilege Control.* arXiv:2504.11703v3, revised 14 May 2026. DOI: 10.48550/arXiv.2504.11703. <https://arxiv.org/abs/2504.11703>.

**[MasDrift]** Zhuoning Xu, Xiucheng Zhang, Hanjun Luo, Yingbin Jin, Yinpeng Dong, and Hanan Salam. *MasDrift: Benchmarking Authorization Preservation Across Multi-Agent Architectures.* arXiv:2608.07556v3, revised 15 October 2026. DOI: 10.48550/arXiv.2608.07556. <https://arxiv.org/abs/2608.07556>.

**Noma Security.** *Your Agents Are Trusting Each Other - Should They?* Noma Security Blog, 23 April 2026. Byline: Diana Kelley. <https://noma.security/blog/your-agents-are-trusting-each-other-should-they>. Industry blog; not peer reviewed.

**J. Diaconu, M. Yannuzzi, H. Muyal, F. Brockners, N. Kale, A. Agarwal, J. Hickman, and A. Lal.** *Cross-Domain AuthZ Information sharing for Agents.* Internet-Draft draft-diaconu-agents-authz-info-sharing-01, 4 August 2026. <https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/01/>. Work in progress; not endorsed by the IETF.

**Krti Tallam.** *Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure.* arXiv:2605.05440v1, 6 May 2026. DOI: 10.48550/arXiv.2605.05440. <https://arxiv.org/abs/2605.05440>.

**M. Jones, A. Nadalin, B. Campbell, J. Bradley, and C. Mortimore.** *OAuth 2.0 Token Exchange.* RFC 8693, Internet Engineering Task Force, January 2020. DOI: 10.17487/RFC8693. <https://www.rfc-editor.org/rfc/rfc8693>. Standards-Track RFC; not a measurement of this program.

**Ruoming Pang, Ramon Caceres, Mike Burrows, Zhifeng Chen, Pratik Dave, Nathan Germer, Alexander Golynski, Kevin Graney, Nina Kang, Lea Kissner, Jeffrey L. Korn, Abhishek Parmar, Christina D. Richards, and Mengzhi Wang.** *Zanzibar: Google's Consistent, Global Authorization System.* 2019 USENIX Annual Technical Conference (USENIX ATC 19), pp. 33–46, Renton, WA, July 2019. <https://www.usenix.org/conference/atc19/presentation/pang>. Peer-reviewed conference paper; not reproduced here.

**Arnar Birgisson, Joe Gibbs Politz, Úlfar Erlingsson, Ankur Taly, Michael Vrable, and Mark Lentczner.** *Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud.* Network and Distributed System Security Symposium (NDSS), 2014. DOI: 10.14722/ndss.2014.23212. <https://www.ndss-symposium.org/ndss2014/programme/macaroons-cookies-contextual-caveats-decentralized-authorization-cloud/>. Peer-reviewed conference paper; not reproduced here.

**T. Lodderstedt, J. Richer, and B. Campbell.** *OAuth 2.0 Rich Authorization Requests.* RFC 9396, Internet Engineering Task Force, May 2023. DOI: 10.17487/RFC9396. <https://www.rfc-editor.org/rfc/rfc9396>. Standards-Track RFC; not a measurement of this program.

**C. Ellison, B. Frantz, B. Lampson, R. Rivest, B. Thomas, and T. Ylonen.** *SPKI Certificate Theory.* RFC 2693, Internet Engineering Task Force, September 1999. DOI: 10.17487/RFC2693. <https://www.rfc-editor.org/rfc/rfc2693>. Informational RFC; not a measurement of this program.

**Mark S. Miller.** *Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control.* PhD thesis, Johns Hopkins University, Baltimore, MD, 2006. <https://jscholarship.library.jhu.edu/items/b8376e55-208e-4fcc-81a2-ad5a7de0acbb>. No DOI; not reproduced here.

**Matt Blaze, Joan Feigenbaum, and Jack Lacy.** *Decentralized Trust Management.* 1996 IEEE Symposium on Security and Privacy, pp. 164–173, IEEE Computer Society Press, 1996. DOI: 10.1109/SECPRI.1996.502679. Peer-reviewed conference paper; not reproduced here.

**Andrew W. Appel and Edward W. Felten.** *Proof-Carrying Authentication.* Proceedings of the 6th ACM Conference on Computer and Communications Security (CCS), pp. 52–62, ACM, New York, NY, USA, 1999. DOI: 10.1145/319709.319718. Peer-reviewed conference paper; not reproduced here.

**Philip W. L. Fong.** *Relationship-Based Access Control: Protection Model and Policy Language.* Proceedings of the First ACM Conference on Data and Application Security and Privacy (CODASPY), pp. 191–202, ACM, New York, NY, USA, 2011. DOI: 10.1145/1943513.1943539. Peer-reviewed conference paper; not reproduced here.

**Christophe Parisel.** *A Theory of Least Autonomy in AI.* arXiv:2607.09744v1, 3 July 2026. DOI: 10.48550/arXiv.2607.09744. <https://arxiv.org/abs/2607.09744>. arXiv preprint; not reproduced here.

**Xiaochong Jiang, Shiqi Yang, Ziwei Li, Lifei Liu, Haoran Yu, and Yichen Liu.** *ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation.* arXiv:2605.26542v4, revised 1 July 2026; published at the Second Workshop on Agents in the Wild: Safety, Security, and Beyond (AIWILD) at ICML 2026. DOI: 10.48550/arXiv.2605.26542. <https://arxiv.org/abs/2605.26542>. Workshop paper; not reproduced here.

**Amjad Ibrahim and Yong Li.** *Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI.* arXiv:2606.03518v1, 2 June 2026. DOI: 10.48550/arXiv.2606.03518. <https://arxiv.org/abs/2606.03518>. arXiv preprint; not reproduced here.

**Anmol Pandey, Aditya Jain, Liang Chen, and Carsten Maple.** *Local Allow, Global Deny: Why Per-Action Authorization Does Not Compose in LLM Agents.* arXiv:2610.27620v1, 20 October 2026; extended version of a paper accepted at the 8th IEEE International Conference on Trust, Privacy and Security in Intelligent Systems and Applications (IEEE TPS 2026). DOI: 10.48550/arXiv.2610.27620 (pending registration). <https://arxiv.org/abs/2610.27620>. Preprint; not reproduced here.

*Reference status: APC, TraceGrant, SentinelAgent, Progent, and MasDrift are arXiv preprints; no peer-reviewed venue is asserted. Noma is an industry blog; the IETF draft entry is an active individual Internet-Draft, not an RFC, while RFC 8693 and RFC 9396 are Standards-Track RFCs and RFC 2693 is an Informational RFC. Zanzibar, Macaroons, Fong, Blaze et al., and Appel and Felten are peer-reviewed conference papers; Miller is a PhD thesis; the four 2026 agent-delegation entries are arXiv preprints, one of which (ChainCaps) reports workshop publication. Bibliographic identities were checked on 20 October 2026 (seven entries), 22 October 2026 (MasDrift), 5 November 2026 (RFC 8693, Zanzibar, Macaroons), and 6 November 2026 (the ten entries added in this revision); the works were not reproduced, and none is treated as a verified input to the measurements.*
