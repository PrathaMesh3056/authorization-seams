# APC call → TraceGrant Contract mapping (design choice, written before code)

Date: 2026-10-19. Status of everything in this file: **DESIGN CHOICE / HYPOTHESIS (ours)**.
Nothing here is READ from either paper. Neither paper specifies how to turn one
APC-authorized call into a TraceGrant Contract; this document is our own
construction, and every result produced with it is a statement about *this
implementation under this mapping*, never about "TraceGrant's behavior".

## 1. The modeling problem

- APC's unit of authorization is a single tool call evaluated against a session
  scope `S=(R,A,D,X)`, a budget, prior-action state, and an intent `Ψ`.
- TraceGrant's unit of authorization is a task-level Contract
  `<MAY, MUST, BIND, VERIFY>`, frozen at establishment, enforced against a
  Ledger of evidence, obligations, budgets, and one-shot effect certificates.
- There is no paper-specified translation. The smallest bridge we can build is a
  **one-step Contract**: one effect obligation whose MAY entry is the attempted
  tool, whose BIND constants are the canonical attempted arguments, and whose
  VERIFY is a postcondition on the mock tool's observable result.

This bridge necessarily drops most of APC's session state. The experiment is
designed to measure which dropped fields matter, and to separate failures caused
by the bridge shape from failures caused by TraceGrant's own checks.

## 2. Paper re-read records used for this design

These are the same records as in `phase0_state.md` §3, repeated here because the
prompt requires the re-read record in this file.

### 2.1 APC paper

Query: "Authorization Scope Definition 4.1, meet composition rule, Theorem 4.8 composition soundness preconditions"   Date: 2026-10-19
Opened: `C:\Users\prath\Downloads\RPaper\authorization_pilot\vendor\bounded-agents\paper\main.tex`, lines 219-309 (Section 4.1 `Authorization Scope`, Definition 4.1, the meet `S1 ⊓ S2 = (R1∩R2, A1∩A2, D1∩D2, X1∪X2)`, Definitions 4.2-4.4, Section 4.4 `Prior-Action State`, Section 4.5 `Composition Constraints`, Theorem 4.8 with its proof and `Scope and limitations` paragraph). Also lines 63-90 for the abstract/contributions.
Blocked: nothing failed to load. The PDF `bounded-agents.pdf` was not opened visually; the `.tex` source above is the paper's own source text for that PDF.
Stopped: no for these sections; the evaluation section, appendices and related work were not read.
Conclusion: within the sections opened, Theorem 4.8 is conditional on (1) completeness of X, (2) serialized admission, and (3) static X within a session, and it concerns same-mechanism composition of APC action sequences, not a cross-mechanism handoff.

### 2.2 TraceGrant paper

Query: "Contract MAY/MUST/BIND/VERIFY structure, Equation 2 static analysis, Algorithm 1 line 14 CheckScope/CheckVerification"   Date: 2026-10-19
Opened: `C:\Users\prath\Downloads\RPaper\tracegrant_task_d_20261014\sources\paper.txt` (extracted from `sources\tracegrant-2608.21126v1.pdf`), lines 230-318 (Sections 4.2.1-4.2.2, Equation 1, the POEC Contract description, Equation 2, Algorithm 1 lines 1-18), lines 392-440 (Section 4.4, Equations 8-10), lines 755-823 (Section 5.7 and the optional-recipient gap), lines 914-940 (Section 6.3 Limitations).
Blocked: the extraction has two-column interleaving artifacts and replacement characters. Algorithm 1 line 14 is legible as `if ¬CheckScope(C′,RΣ,Σ) ∨ ¬CheckVerification(E,C′,OΣ,Σ) then return Reject`. The saved page images `page-05.png`...`page-08.png` were not visually inspected.
Stopped: no for these sections; the evaluation, appendices and related work were not read.
Conclusion: within the sections opened, acceptance requires both CheckScope and CheckVerification (the algorithm rejects if either fails); the Contract fields have the meanings quoted below; and Section 6.3 says binding must cover every authority-bearing argument that appears at runtime, including optional ones. A search of the whole extracted text for `composition`/`Theorem`/`serializ` found no cross-mechanism composition theorem; the word appears only as "task composition"/"task decomposition".

Claim: The four Contract components mean: MAY = permitted tools/operations, target scope, argument constraints, call budgets; MUST = dependency-aware obligation graph; BIND = permitted source/type/evidence constraints/derivation for each authority-bearing argument; VERIFY = postconditions after an effect.
Status: READ
Access: read-directly (`sources/paper.txt:234-260`)
Source: `tracegrant_task_d_20261014/sources/paper.txt:234-260`
Not claimed: This does not specify how to translate any non-TraceGrant authorization object into these components; the translation below is ours.

## 3. Registry used by the mapping (design choice)

The Task D synthetic registry (`implementation/example_contracts.py:11-34`) does
not contain the four mock tools. We add a v2 registry in `adapters/tracegrant_adapter.py`
with these tool schemas. Treating reads as `kind='effect'` is a deliberate
distortion: in the paper's vocabulary a read is a query, but the existing
`MockWorld` read calls produce observable effects and APC authorizes them as
actions. This makes every mock call checkable through `check_call` and is
recorded as a design choice, not as a reading of the paper.

| Tool | kind | authority args | payload args | result_fields |
|---|---|---|---|---|
| `read_confidential` | effect | `resource: string` | — | `content: string` |
| `read_public` | effect | `resource: string` | — | `content: string` |
| `save_internal` | effect | `resource: string` | `body: string` | `status: string` |
| `send_external` | effect | `recipient: string` | `body: string` | `status: string` |
| `apc_state` (M2 only) | query | `tool: string`, `resource: string` | — | `apc_allowed: boolean`, `apc_reasons: string`, `budget_remaining: number`, `composition_clear: boolean`, `freshness: string`, `revoked: boolean`, `principal: string`, `task: string`, `tool: string`, `resource: string`, `recipient: string`, `evidence_digest: string` |

## 4. M0 — primary one-step scope-only mapping (arms 2 and 5)

Given a downstream call with canonical arguments (the same `MockWorld.canonical`
result the existing pilot uses, so Python-signature defaults are already applied)
and a scope snapshot from APC (or, in arm 2, from the frozen case's root scope):

1. **MAY** = `{tool: Permission(budget=1, allowed_args=[all canonical argument names], constraints=...)}`
   where the constraints are:
   - `resource`: `Constraint(type=string, choices=[every resource in the snapshot's R])`;
     the snapshot is the **post-handoff** effective scope (`APC.envelope.effective_scope`
     after `handoff()`), so M0's resource authority is exactly what the handoff
     conferred, even when the handoff's role scope contains a resource the root
     authorization never held;
   - `recipient`: `Constraint(type=string, choices=[the snapshot's allowed recipient])`;
   - payload args: no constraint and no `trusted_payloads` entry.
2. **MUST** = `[{id: "F1", kind: "effect", tool: tool}]`.
3. **BIND** = for each authority argument, a constant binding to the canonical
   attempted value with `constraints` equal to the MAY constraint. Payload args
   are not bound. In `complete` binding mode every authority arg in
   `allowed_args` must be bound, which this satisfies.
4. **VERIFY** = `{F1: {postconditions: {result_field: expected_value}}}` where the
   expected value is derived from the mock tool's known return
   (`CONFIDENTIAL-MARKER:{resource}`, `PUBLIC-MARKER:{resource}`, `saved`, `sent`).
   The unsatisfiable-VERIFY template deliberately replaces this with
   `status: delivered_to_human`.
5. `state = establish(contract, registry, session=call.session)`; on `ValueError`
   the adapter returns deny with the rejection reason.
6. `decision, _ = check_call(CallRequest(tool, arguments, obligation="F1"), state)`.
   `ALLOW` → allow; `PROOF-GAP`, `DENY`, `STEP_UP_AUTH` → deny.

**What M0 translates:** the requested tool name as the MAY key (not checked
against APC's action set), resource choices from R, the recipient allowlist from
APC's parameter policy, canonical argument defaults, call budget = 1, and a
VERIFY predicate derived from the toy result schema.

**What M0 does not translate:** APC's action-set membership check, principal,
task, X / prior-action composition history, cumulative cost consumed, envelope
expiry, revocation, cross-call replay state, and the semantic truth of admitted
payloads. These omissions are the condition under test in Phase 0.5.

**Why this is deliberately incomplete on the action type:** H1 asks whether the
receiving mechanism re-derives scope or trusts the "already authorized" caller.
M0 uses the requested tool as the Contract's MAY key. If a downstream caller asks
for `read_confidential` after APC authorized `read_public`, M0 will synthesize a
Contract for `read_confidential`, constrained only by the resource set. This is
the trust-laundering path the experiment exists to measure; it is a mapping
artifact, not a TraceGrant mechanism property.

## 5. M1 — conservative-reject variant (arm 7)

M1 uses the same Contract construction as M0 but refuses before establishment if
any of the following cannot be translated:

1. the requested tool is not in the root authorization's action set A;
2. an authority argument has no scope-derived constraint, where the resource
   constraint must be derivable from the **intersection of the root R and the
   handoff R** (the handoff scope alone is not trusted; a resource present only
   in the handoff scope is treated as untranslatable), and the recipient must
   have an allowlist entry;
3. no observable, satisfiable VERIFY value can be derived from the frozen tool
   schema and the mock tool's known return;
4. the call's principal or session differs from the handoff context;
5. the case exercises envelope expiry, revocation, prior-action composition
   history, cumulative cost, or cross-call replay (all of which M0's Contract
   cannot represent natively).

Each refusal returns deny with `mapping_note` naming the field. M1 is expected to
deny many benign cases; that is the point of a fail-closed control. It must not
leak.

## 6. M2 — retained-upstream evidence variant (arm 6)

M2 adds one evidence obligation to M0:

- `E1` = evidence obligation on the synthetic query tool `apc_state`, with
  `query_args={"tool": tool, "resource": resource}` and fields requiring:
  `apc_allowed=true`, `apc_reasons=""`, `budget_remaining>=0`,
  `composition_clear=true`, `freshness ∈ {current, renewed}`, `revoked=false`,
  `principal=<handoff principal>`, `task=<handoff task>`, `tool=<tool>`,
  `resource=<resource>`, `recipient=<recipient>` (when present), and
  `integrity={"evidence_digest": <sha256 of the canonical APC decision package>}`.
- `MUST = [E1, F1(dependencies=["E1"])]`, `BIND` unchanged, `VERIFY` unchanged.
- Before `check_call`, the adapter calls
  `admit_evidence(EvidenceRecord(...), state)`. The record is built by the
  harness from the **shadow APC admission** of the same call (serialized first,
  per the execution order). If admission fails, the adapter denies.

The evidence record is trusted harness input, not a signed APC artifact. A real
deployment would need authenticated, replay-resistant evidence transport; this
experiment does not test that. M2 therefore shows what *can* be carried, not what
a production handoff would verify cryptographically.

## 7. M3 — alternate task-level Contract (Phase 5.5 diagnostic only)

For the composition-history and repeated-call families, M3 builds a single
two-obligation Contract (`E1=read`, `F1=send/save`, `dependencies=[E1]`) from the
whole prelude+attempt sequence, instead of one fresh Contract per call. This is
closer to the paper's task-level Contract shape and is used only to test whether a
top Phase 3 finding disappears under a more faithful Contract shape. It is not
one of the seven arms and its results are reported separately.

## 8. Arm-by-arm mapping use

| Arm | Mechanism gate | Mapping / state carried |
|---|---|---|
| 1 `apc_alone` | APC | none; APC sees all calls with full state |
| 2 `tracegrant_alone` | TraceGrant | M0 from the frozen case root scope (root R); no APC anywhere; fresh Contract per call |
| 3 `apc_apc_preserved` | APC | same-mechanism control; envelope narrowed to `agent:b`, budget/composition preserved |
| 4 `apc_apc_reset` | APC | same-mechanism control; budget/composition reset at handoff |
| 5 `apc_tracegrant_scope_only` | TraceGrant | M0 from APC's **post-handoff** effective scope snapshot; shadow APC runs first and updates state but its denial is not propagated. Because the snapshot is the post-handoff scope, a handoff that widens the role scope widens M0's resource choices too; this is the arm that the arm-2 root-scope mapping does not share. |
| 6 `apc_tracegrant_retained` | TraceGrant | M2; shadow APC decision + pre-admission budget state passed as admitted evidence. The evidence records `apc_allowed`, which is the post-handoff APC's own decision; if that APC admitted a widened scope, M2 admits it too (the trust boundary is the evidence, not TraceGrant). |
| 7 `apc_tracegrant_fail_closed` | TraceGrant | M1; deny on any untranslatable exercised field, including a resource present only in the handoff scope and not in the root R |

**Interpretation of "run APC's admission first" (execution order):** in every
arm the calls are executed strictly sequentially, never concurrently. In arms
2/5/6/7 the handoff is serialized: APC (if present) admits the prelude and a
shadow admission of the downstream call completes first, committing its budget
and composition state, and only then does the Contract get synthesized and
checked. In arm 5 the shadow APC denial is recorded (`apc_shadow_reasons`) but
is not allowed to block the handoff, because the arm's hypothesis is precisely
that only the static scope crosses. In arm 6 the shadow decision/state is what
crosses. This is a design choice; it is what makes arms 5 and 6 meaningfully
different.

## 9. Anticipated failure modes (HYPOTHESIS, before data)

- M0 is expected to leak on: action-type widening, principal/task rebinding,
  composition-history loss, cumulative-budget reset, expiry, revocation, and
  cross-call replay. These are the fields it does not translate.
- M0 is expected to catch recipient substitution and omitted-argument forbidden
  defaults, because it canonicalizes arguments and derives the recipient
  constraint from APC's allowlist.
- M0's unsatisfiable-VERIFY case is expected to be admitted by `check_call`
  (which does not evaluate VERIFY) and to fail only at `check_receipt`; this is
  an admission/completion boundary, not a confidentiality leak.
- M1 is expected to deny every attack template and a large fraction of benign
  cases whose construction touches dynamic state.
- M2 is expected to close the M0 leaks by carrying the shadow APC decision as
  evidence, at the cost of depending on trusted evidence transport.

## 10. Mapping artifact vs mechanism behavior — the classification rule

- **Mapping artifact**: the failure depends on an M0 choice that could reasonably
  be made differently while still using TraceGrant's Contract vocabulary (e.g.,
  using the requested tool as the MAY key instead of checking A; using a fresh
  Contract per call instead of a task-level Contract; choosing an unsatisfiable
  VERIFY value).
- **Mechanism / Contract-vocabulary behavior**: the failure persists under a
  reasonable alternative mapping because the Contract model itself has no field
  for the exercised fact (principal identity, expiry, revocation, prior-action
  composition history, cumulative cost) and `check_call` has no place to consult
  it.
- Every disagreement in `results/disagreements.md` gets one of these verdicts,
  and Phase 5.5 tries to make the top three disappear under M1/M2/M3 before the
  finding is kept.

## 11. Claim records

Claim: A one-step Contract per APC call is a possible bridge, but it drops APC's
principal chain, prior-action history, cumulative budget, expiry state and
revocation state.
Status: DESIGN CHOICE (HYPOTHESIS)
Access: reasoning (no source states this; it follows from the field lists in `models.py:94-101` and `core.py:70-96`)
Source: `tracegrant_task_d_20261014/implementation/models.py:94-101`; `authorization_pilot/vendor/bounded-agents/apc/core.py:70-96`
Not claimed: This does not show that a richer Contract cannot carry those facts as
evidence; M2 is exactly such an attempt.

Claim: Under M0 the unsupported fields can leak, so the composition condition in
`composition_condition.md` predicts those cases unsafe before any run.
Status: HYPOTHESIS (untested at the time of writing)
Access: reasoning (mapping design, not measured)
Source: none (our construction)
Not claimed: This does not show that TraceGrant's intended task-level Contract
would leak the same way; M3 tests one such alternative in Phase 5.5.
