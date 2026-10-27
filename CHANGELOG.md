# Changelog

All notable changes to this repository are recorded here. The experiment
artifacts themselves are frozen; changes to them are never made in place.

## [0.1.4] - 2026-10-26

### Added

- 26 October 2026 audit correction pass: H3 narrowed to state/identity
  vocabulary gaps; caught/E1/boundary findings rehomed under H1/H6 and the
  measured findings; zero-seam construction-forced disclosure added to
  Sections 1, 4.5, and 9; Appendix A/Table A1 hypothesis-lineage
  reconciliation added; legacy Progent citation qualified; 638 arithmetic
  wording corrected; Table 12 display-only artifact-root aliases added; and
  Figure 2's Locus B connector corrected.
- Pre-edit provenance copies archived under `paper/backups/` and
  `paper/figures/superseded/`: the pre-audit manuscript, the 23 October
  standalone export, and the pre-audit Figure 2 SVG/PDF. The 23 October
  canonical PDF remains archived at
  `paper/drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf`.
- New canonical 26 October PDF and refreshed standalone export:
  `paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf` and
  `paper/latex_export/main.pdf`.
- 28-page arXiv-compliant named-author candidate under
  `paper/arxiv_export/`, with 1-inch margins, both figures vector, zero
  missing glyphs, zero fatal LaTeX errors, and zero overfull hboxes.

### Changed

- `paper/MANUSCRIPT_REVISED.md` is now
  `1732872C36D4AC5EAE349450ACA946120F0EA21A2C48235F58985167A414CCC2`;
  the canonical PDF is
  `B3D39ED0D5F26CB42C1B436D43B9D5FFCC3C6FE613461C860561A0DBEBB788D3`;
  the standalone `main.tex` is
  `4C27CB582582473B961C9DD7E7574D67BD2ECB9C00CA55E6AFDDA493044D8602`;
  and the arXiv PDF is
  `7022C36250F5E690E574CB2AF814A2BFD8C538FFBF2812AD156188192FE514D1`.
- Updated the state docs, QA pins, build README, export READMEs, metadata
  checklist, figure changelog, and artifact snapshot for the 26 October build.
- The generated build excludes `paper/latex_export/main.aux` and
  `paper/latex_export/main.log` as local compile output.

### Validation

- Canonical build: 25 pages, 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull
  hboxes, 3 cosmetic underfull hboxes, 6 ignored infinite-glue-shrinkage
  diagnostics, and 1 stable label warning.
- arXiv build: 28 pages, 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull
  hboxes, 4 cosmetic underfull hboxes, 3 ignored infinite-glue diagnostics in
  the extracted package compile, and 1 stable label warning.
- Abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`;
  the static reference list remains eight entries; H4 and H7 remain
  `UNTESTED`.
- No new claims, experiments, or references were added by the correction pass.
- The regenerated manifest verifies every tracked file; `python -m pytest -q
  qa` passes 15 tests; the TraceGrant Task D suite passes 52 tests; the review
  zip extracts, verifies, and rebuilds the 28-page arXiv candidate.
  `dist/sanitized` remains untouched and verifies at 298 files.
- No arXiv submission, public release, license, DOI, or repository visibility
  change has occurred.

## [0.1.3] - 2026-10-23

### Fixed

- Corrected the 638 denominator wording to the full 96-case matrix scope: 488
  admissions plus 150 token-attached denials = 638 counted events; the 150
  decomposes as 40 native P6/P7, 42 attestation-stage, and 68 pre-presentation
  denials. This is a non-vacuity count, not a count of all token events and not
  a "token-event call" denominator.
- Refreshed the canonical PDF, standalone LaTeX export, package, state docs,
  manifest, and QA hashes. The pre-638 23 October PDF/zip/source are archived in
  the working archive; the previous local commit preserves the pre-correction
  repository state.

### Notes

- No new claims, experiments, references, or H4/H7 status; the abstract and
  eight-reference list are unchanged.
- F2, F3, F6, F9, F13, and F14 are resolved; F1 remains a minor identifier
  line-break residual. F7, F8, F10-F12, and the listed NITs are minor/cosmetic;
  F15 is an optional editorial note.
- `dist/sanitized` remains untouched; no push has occurred.

## [0.1.2] - 2026-10-23

### Fixed

- Corrected the handoff-norm sentence from "kept the 4 denials" to "kept the
  4 leaks" (independent review F4).
- Scoped the Table 12 H6 row to the measured pairs with the disclosed E1
  action-family exception (independent review F5).
- Refreshed the canonical PDF, standalone LaTeX export, package, state docs,
  manifest, and QA hashes. The pre-F4F5 23 October PDF/zip are archived in the
  working archive; the previous local commit preserves the pre-correction
  repository state.

### Notes

- No new claims, experiments, references, or H4/H7 status; the abstract and
  eight-reference list are unchanged.
- Remaining independent-review items are minor or cosmetic and non-blocking.
- `dist/sanitized` remains untouched; no push has occurred.

## [0.1.1] - 2026-10-23

### Changed

- Finalized the named-author 23 October draft: F1-F13 corrections, the author
  block and matching PDF metadata, a refreshed canonical PDF, and a refreshed
  standalone LaTeX export.
- Added MasDrift as the eighth reference after the 22 October 2026 arXiv check;
  the first seven identities remain the frozen 20 October set.
- Table 15's caption and table body now both appear on page 23; the suffix note
  is at `MANUSCRIPT_REVISED.md` line 521.

### Notes

- H4 and H7 remain `UNTESTED`; no new claims, experiments, or references
  beyond the authorized MasDrift addition.
- One stable label warning and three cosmetic underfull hboxes remain.
- The build is named-author; a double-blind venue requires re-anonymization.
- `dist/sanitized` remains untouched; no push has occurred.

## [0.1.0] - 2026-10-21

### Added

- Corrected manuscript source (`paper/MANUSCRIPT_REVISED.md`) and canonical
  24-page draft PDF (`paper/drafts/MANUSCRIPT_DRAFT_2026-10-21.pdf`).
- Standalone LaTeX export of the same draft (`paper/latex_export/`).
- Pandoc + XeLaTeX build scripts for Windows and POSIX shells.
- Selected frozen experiment trees for APC → TraceGrant, APC → SentinelAgent,
  and the bridge-boundary study, with cases, locks, and stored results.
- Independent TraceGrant Task D implementation and adoption examples.
- Pinned SentinelAgent prototype excerpt (MIT) with provenance notes.
- `artifacts/sha256sums.txt` and `scripts/verify_artifacts.py` integrity checks.
- Repository QA tests under `qa/`.
- Method, reproducibility, artifact-scope, sanitization, and release-gate docs.

### Notes

- Hypotheses H4 and H7 remain `UNTESTED`; no H4/H7 experiments are included.
- Progent is related work only. No Progent figure is reproduced, re-measured,
  or compared.
- License selection, final public email, repository URL, archival DOI, and
  venue metadata remain open release gates (`docs/RELEASE_CHECKLIST.md`).

### Validation

Recorded in `docs/REPO_BUILD_QA.md`:

- artifact manifest verifies for 294 tracked files;
- 9 repository QA tests and 52 TraceGrant Task D tests pass;
- E1, SentinelAgent (`672` rows), and boundary (`1,152` rows) lock checks pass;
- the paper builds to 24 pages with zero missing glyphs, zero LaTeX errors, and
  zero overfull hboxes;
- a local clone verifies byte-identical content and rebuilds the paper;
- the sanitized tree and review zip both re-verify after extraction.
