# Day-7 stop/continue decision

## What the locked matrix established

- A 7-arm x 80-case local matrix ran end-to-end (560 executions, no crashes).
- The scope-only cross-mechanism handoff admits 24/40 attack cases;
  the retained-evidence mapping admits 0/40; the fail-closed mapping
  admits 0/40 but denies 20/40 benign cases.
- The locked condition scored precision 0.750 / recall 1.000
  against arm 5; the four resource false positives and four VERIFY false positives are
  understood and refine the condition rather than indicating mechanism defects.
- Replay determinism: 10 pairs semantically identical.

## Decision

**CONTINUE for one bounded extension; STOP the novel-finding claim on the current result.**

Reasons to continue:

1. The main gap (24/40) is representational and reproducible, and M2 demonstrates it is
   closable *under trusted evidence transport*. Real deployments need authenticated,
   replay-resistant evidence, which this experiment deliberately did not build. That is a
   concrete, well-scoped follow-up.
2. The action-type clause of the composition condition - the sharpest version of the
   'trusts the caller' question - is untested. One added handoff (role A a strict subset
   of root A) and one attack case would test it without enlarging the frozen set.

Reasons to stop claiming novelty now:

1. No mechanism-level defect was found in either implementation under this mapping. The
   leaks are fields the Contract model does not carry, and the fail-closed/reset controls
   reproduce known v1 behavior.
2. The unsat-VERIFY and resource-widen expectations were falsified; the remaining result
   is an attribution result (which failures belong to the mapping and which to the
   Contract vocabulary), not a new vulnerability class.

## Stop/continue criteria for the extension

- STOP the seam line if the action-narrowing case is denied by both mappings and the
  authenticated-evidence follow-up yields no distinct failure beyond F1.
- CONTINUE to a second mechanism pair only if the authenticated-evidence follow-up
  produces a failure that is not attributable to trusted-input assumptions or to the
  one-step Contract shape.

No further frozen-set edits. Any extension is a new frozen set with its own lock.

