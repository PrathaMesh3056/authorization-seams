# SA pair — review revision (19 Oct 2026)

Revision of the post-run report layer after the independent adversarial review
(`results\ADVERSARIAL_REVIEW.md`, GLM-5.3-Flash Free; verdict NON-BLOCKING).

## What changed and why

- **SA-1 (MAJOR, wording-only).** Three universal sentences that predated the E1
  discriminating tests were bounded to the frozen family-wide oracle and now cite
  the measured E1 arm-native exception (`paper\CONSOLIDATED_CLAIMS.md` ★/§4.2):
  - `SA_RESULTS.md` §1 and §2 (blockquote);
  - `claims_update_sentinelagent.md` "Cross-cutting".
- **SA-3 (MINOR).** `SA_RESULTS.md` §6 note + §12: the "150 token-check denials"
  label now reads "150 denials with a token event attached (40 native P6/P7 denials,
  42 attestation-stage denials in arm 6, 68 pre-presentation refusals in arm 7)".
  The split is computed from `results\sa\runs.jsonl` by the generator's
  `denial_split()` helper, not hand-typed.
- **SA-4 (MINOR).** `SA_RESULTS.md` §9 (and the mirrored claims H3 line): "no effect
  is produced" → "no unauthorized effect is produced and no obligation is
  fabricated — the four admitted cases do execute their declared `internal_write`".
- **SA-9 (MINOR).** One scoring-convention line added under "Cross-cutting" in
  `claims_update_sentinelagent.md` (arm-invariant oracle; rescoping arm 2 would
  flip `composition_history_loss` to safe).
- **SA-2 (MINOR) deferred.** The `hash_unchanged:raw_metrics.json` short label is
  ambiguous with the SA's own raw_metrics; the checked file is the v2 reused input
  (full path + hash are recorded in `results\sa\manifest.json`). Fixing the printed
  label would require rewriting the run-time `results\sa\self_review.json`, so it is
  left for a future run; the resolution is recorded in
  `paper\consolidation_reconciliation.md` §H.
- **SA-5/6/7/8 (INFO)** need no artifact change (historical embedded paths; the
  disclosed key/trust boundary; arm-7's refusal keys on case-declared
  `exercised_aspects`; and the prompt erratum arm 4 = 8/8).

## How it was regenerated

    python sa_reports.py     # run from tests\seam_pilot_sentinelagent

Every number in the regenerated reports is computed by the generator from the
frozen artifacts under `results\sa\`; the diff against the pre-revision copies is
wording-only. Verified after regeneration:

- `results\sa\runs.jsonl`, `metrics.json`, `controls.json`, `self_review.json`,
  `manifest.json`, `phases.json` — hashes unchanged;
- `results\sa\reconciliation.json` — byte-identical; and
- the 11 frozen inputs re-hashed — 11/11 match (the review's §5 table).

## Pre-revision copies

- `SA_RESULTS.pre-revision.md`
- `claims_update_sentinelagent.pre-revision.md`
- `sa_reports.pre-revision.py`

These are the exact bytes before the 19 Oct regeneration. Nothing was deleted; the
review's own disclosed temp files remain in `results\review_tmp\`.

— Recorded by the QA gate, 19 Oct 2026.
