# Proposed language revisions for SA_RESULTS.md and consolidation (never edits)

These are proposed rewordings only; no SA artifact is edited by this experiment.

## Replacement for the SA_RESULTS.md 'zero seam is universal' generalization

Current (SA_RESULTS.md section 2 / claims_update_sentinelagent.md section 'Cross-cutting'):
  "In every pair we have built and run, the failures of a cross-mechanism handoff are subtractive: ... the
  composition creates no authorization failure that one of the mechanisms does not already exhibit standalone."

Proposed conditional form:
  "In every pair we have built and run UNDER A NARROWING-PRESERVING MAPPING, the failures of a cross-
  mech anism handoff are subtractive: the seam carries less context than the receiving mechanism needs, and
  the composition creates no authorization failure that one of the mechanisms does not already exhibit
  standalone. This does not extend to non-narrowing-preserving bridges: the boundary experiment (V1/V2) shows
  a non-narrowing-preserving manifest derivation lets the receiving arm admit a case the canonical arm blocks,
  but the same leak appears in standalone arm 2v, so it is a bridge-design artifact, not composition-specific."

## Replacement for 'every leak is standalone, never composition-specific'

Proposed conditional form:
  "Every leak is standalone, never composition-specific, for a narrowing-preserving bridge (canonical T0). For non-narrowing-preserving bridges (V1 role-scope derivation: resource_widen-0-a, resource_widen-1-a, resource_widen-2-a, resource_widen-3-a; V2 resolved-call default: omitted_forbidden_default-0-a, omitted_forbidden_default-1-a, omitted_forbidden_default-2-a, omitted_forbidden_default-3-a), the composed arm leaks a case the canonical arm blocks, but standalone arm 2v leaks identically, so composition neither creates nor removes the failure."

## Bridge-conditionality disclaimer (to attach to every zero-seam claim)

  "The zero-seam result holds for narrowing-preserving canonical T0 on the frozen 96-case set. It is bounded,
  not assumed: non-narrowing-preserving bridges (V1/V2) admit cases the canonical arm blocks, though those
  leaks exist standalone (arm 2v) and are therefore bridge-design artifacts, not composition-specific failures."

## Conventions to disclose alongside any zero-seam restatement

- The arm-2 authority input is the frozen case root scope, via canonical T0 (arm 2 always canonical).
- Arm 2==arm 5 (SA pilot) and arm 2v==arm 5 (boundary, each variant) are construction-forced identities,
  not evidence; the informative contrast is canonical arm 2 (safe) vs composed variant arm 5 (leak).
- The SA scoring is arm-invariant (`permitted &= role_resources`, `prohibited_composition` applied to arm 2);
  rescoping `prohibited_composition` would flip composition_history_loss arm 2 leak->safe (disclosed, not hidden).

