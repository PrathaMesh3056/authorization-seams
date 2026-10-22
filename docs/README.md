# Documentation index

This directory mixes two kinds of material:

- **New repository documentation** written for this package (method overview,
  reproducibility, scope, release gates, sanitization).
- **Copied internal status/QA records** from the working archive. They are kept
  for traceability, not as submission text.

| File | Kind | Purpose |
|---|---|---|
| `METHOD_OVERVIEW.md` | new | What the study measures and how to read the claims |
| `REPRODUCIBILITY.md` | new | How to rebuild the paper and verify artifacts |
| `ARTIFACT_SCOPE.md` | new | What is and is not included, and why |
| `RELEASE_CHECKLIST.md` | new | Open gates before publishing/submitting |
| `RELEASE_SANITIZATION.md` | new | Machine-local path and input review procedure |
| `REPO_BUILD_QA.md` | new | Local build, integrity, and packaging validation record |
| `RESEARCH_STATUS.md` | copied | Internal status snapshot and open gates |
| `FINAL_BUILD_QA.md` | copied | Build, font, reference, and export QA |
| `FONT_QA_REPORT.md` | copied | Font embedding and fallback checks |
| `ARTIFACT_SNAPSHOT.md` | copied | Recorded hashes and build state |
| `SUBMISSION_METADATA_CHECKLIST.md` | copied, redacted | Venue/author metadata gates |
| `TOOLCHAIN.md` | copied | Verified toolchain versions |
| `REVIEW_CORRECTIONS_2026-10-21.md` | copied | Superseded characterizations and corrections |
| `RECHECK_RECONCILIATION_2026-10-21.md` | copied | 21 October recheck reconciliation and finalization procedure |

## Redactions and frozen-file caveat

- `SUBMISSION_METADATA_CHECKLIST.md` is a repository copy. The internal
  placeholder email it recorded has been replaced with
  `<public-email-unresolved>`. The original file in the internal archive is
  unchanged.
- Copied records are snapshots. Where a copied record disagrees with the
  corrected manuscript, the manuscript (`paper/MANUSCRIPT_REVISED.md`) and
  `REVIEW_CORRECTIONS_2026-10-21.md` control; `CONSOLIDATED_CLAIMS.md` is a
  frozen predecessor and is not included.
