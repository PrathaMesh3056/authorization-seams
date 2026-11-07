# Paper authority and reference records

Internal review material. This directory is not part of the public release
package and must not be copied into `dist/sanitized` or a release archive
without a separate sanitization decision.

## Contents

| File | Role | Status |
|---|---|---|
| `CONSOLIDATED_CLAIMS.md` | Frozen paper-facing claim authority, dated 19 October 2026 | Read-only; byte-identical copy of the archive original |
| `REFERENCE_VERIFICATION_2026-10-22.md` | Historical identity record for the first eight reference entries | Historical; not the current 21-entry record |
| `REFERENCE_VERIFICATION_2026-11-06.md` | Consolidated index of the 21 reference entries in the 6 November 2026 manuscript | Current index; transcribes asserted checks, performs no new checks |

## Provenance

- `CONSOLIDATED_CLAIMS.md` copied unchanged from
  `C:\Users\prath\Downloads\RPaper\paper\CONSOLIDATED_CLAIMS.md`.
  Size 44,813 bytes; SHA-256
  `AB088CDFBAF64B14C57C63423B908DEAF7404465C15852FD355D6C3F7870BE51`.
- `REFERENCE_VERIFICATION_2026-10-22.md` copied unchanged from
  `C:\Users\prath\Downloads\RPaper\paper\REFERENCE_VERIFICATION.md`.
  Size 10,094 bytes; SHA-256
  `355F6CA736D3A1EEF234D80716759154381A3DF9FE88CF6326692CF5603CDE17`.
- `REFERENCE_VERIFICATION_2026-11-06.md` was created for this migration from
  the reference list at `paper/MANUSCRIPT_REVISED.md` lines 707-753. It
  transcribes the check dates asserted by the manuscript's reference-status
  paragraph; it does not re-query any locator, reproduce any text, or upgrade
  any status.

## Authority rules

- The frozen claim authority is not edited here. The current manuscript may
  deviate only where a dated correction record says so; see
  `docs/RECHECK_RECONCILIATION_2026-10-21.md`.
- `paper/hashes.txt` remains the frozen Table 15 hash record and is separate
  from this directory.
- The 6 November manuscript's printed reference list is the authoritative
  bibliography for this revision. `paper/venue_codaspy2027/references.bib` is
  a 19-entry venue draft: it includes PEDIGREE (excluded from the 6 November
  paper) and omits Noma and Tallam. It is not the current bibliography.
- The public-release exclusion in `docs/ARTIFACT_SCOPE.md` still applies to
  the frozen claim authority. This private-repository mirror exists so a
  reviewer can audit claims and references in one place.
