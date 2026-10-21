# Method overview

This is a plain-language orientation to the study. The manuscript is the
authority for all claims; this page does not add any.

## The problem

Authorization often crosses a mechanism boundary. A sender narrows its
authority, a bridge translates the narrowed decision into a record the receiver
can read, and the receiver applies its own admission rules. Each component can
behave correctly in isolation while the composed handoff admits a call the
sender never authorized. The study treats that handoff as a **measurement
problem**: what can and cannot be carried across the seam?

## Locked-artifact protocol

For each experiment set:

1. Predictions, cases, arms, and input hashes are frozen before execution.
2. Runs are strictly sequential, offline, and deterministic.
3. Predicted-versus-observed discrepancies are reconciled verbatim into files
   that are not edited afterward.
4. Every number reported in the manuscript is generated from stored artifacts
   rather than transcribed by hand.

The execution ledger records 2,446 executions across the four frozen sets
(560 + 40 + 6 + 16 + 672 + 1,152). One harness-hash deviation is disclosed in
the manuscript (Section 4.2): Test 2's runner hash differs from its mini-lock
after a crash during reconciliation; cases, arms, and predictions were
unchanged, and no measurement or reported count changes.

## Frozen experiment sets

| Set | What it covers |
|---|---|
| APC → TraceGrant pilot | Pair pilot with seven arms and the resolving tests |
| APC → SentinelAgent pilot | Second pair, 96 cases, pinned prototype receiver |
| E1 action-clause extension | Action-narrowing family where attribution depends on the scoring convention |
| Boundary run | Bad-bridge variants V1/V2 at the mapping boundary |

Seven arms separate receiver-alone, sender-side narrowing, and composed
behavior. The seam predicate is defined over arms 5/6/7; the E1 extension uses
the arm-5 form, and arm 2 is the receiver-alone reference. Exact arm semantics
are in the frozen design documents under `tests/seam_pilot_*/design/`.

## Mapping taxonomy

Bridge mappings are design choices, not readings of either paper. The frozen
designs label them M0, M2, M2-auth, M0-A, T0, V1, and V2. The manuscript's
Section 3.2 explains each and where it applies.

## Composition senses

APC's composition result is **intra-session action-sequence composition**, not
cross-mechanism composition. The study therefore does not treat APC's theorem
as a claim about the seam. SentinelAgent's Theorem 4 is scoped to two chains
satisfying P1–P7 within its own framework. Both are inputs to the design, not
verified guarantees about the seam.

## Reading the result

- Under narrowing-preserving bridge mappings on the frozen case families,
  composition adds no admission beyond the receiver's own, **with one measured
  exception** in an action-narrowing family whose attribution depends on the
  scoring convention.
- Forced and contingent identities are labeled separately; do not pool them.
- A zero-seam outcome in Pilot 1 is a property of the frozen case family and
  the arm identities, not evidence of universal safety. The manuscript states
  the caveat explicitly.
- Two SentinelAgent-pair prediction overrides, covering two case families, were
  justified by the frozen set and are recorded in the results, not hidden.

## Out of scope

- **Progent** is related work only. Its published numbers are its authors'
  self-report; no Progent figure is reproduced, re-measured, or compared.
- **H4 and H7 remain `UNTESTED`.** They are not experiments in this package,
  and no partial run should be presented as a test.
- No new claims, baselines, or performance measurements are added by this
  repository.

## Where to look

- `paper/MANUSCRIPT_REVISED.md` — corrected draft.
- `docs/REVIEW_CORRECTIONS_2026-10-21.md` — what was superseded.
- `tests/seam_pilot_v2/results/`, `tests/seam_pilot_sentinelagent/results/`,
  `tests/seam_pilot_sa_boundary/results/` — frozen outputs.
- `tests/tracegrant_task_d_20261014/REPORT.md` — independent Task D
  implementation report.
