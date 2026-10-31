# Changelog

All notable changes to this repository are recorded here. The experiment
artifacts themselves are frozen; changes to them are never made in place.

## [0.1.7] - 2026-10-31

### Changed

- Applied the five-seat ARS review correction pass to
  `paper/MANUSCRIPT_REVISED.md`: rewrote Abstract, Introduction, Sections 2-9,
  and Appendix A; added the two-reading seam test, threat model, hypothesis key,
  claim synthesis, repair taxonomy, and field-level H3 audit. H3, H6, and ★
  moved from `SUPPORTED` to `REFINED`; H1's resource clause is `UNTESTED`;
  H4 and H7 remain `UNTESTED`. Receiver-relative novelty is reported
  separately from sender-relative violation.
- Regenerated canonical, standalone, and arXiv builds: 29, 29, and 32 pages;
  0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- Updated QA hash pins, manifest, export READMEs, and research status.

### Validation

- `python scripts/verify_artifacts.py`: 319 files, all hashes match.
- `python -m pytest -q qa`: 15 passed.
- `python -m pytest -q qa/test_arxiv_build.py`: 6 passed.
- TraceGrant Task D suite: 52 passed.
- No new experiments, references, or claims beyond the review corrections.
- `dist\sanitized` remains untouched; no submission, release, license, DOI,
  or repository visibility change.

## [0.1.6] - 2026-10-28

### Changed

- Scoped the Section 3.7 AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes. The broad
  "AI-assisted drafting ... throughout this work" wording was removed; no claim
  is made that an AI system authored the paper. No new claim, experiment, or
  reference was added.
- Rebuilt the canonical, standalone, and arXiv outputs after the disclosure
  change. The manuscript is now
  `5B85155C8A58185D1EE715A6F38150EFDA121F263E0C826984D0AF0A0CF2EF32`
  (115,399 bytes, 590 lines); the canonical PDF is
  `92A3945281EC5155E2567232F3BA184C33554DD4FB02CCB80F8C793A139540F3`
  (321,999 bytes, 25 pages); the standalone `main.tex` is
  `A632B591801FA6E80D203E8D4D7085E2866A4EACF62F8C3CDF2908F08B0A68DA`
  and its PDF is
  `1430E2DBFF0A4658C72504731AA28F04B127BA4C6D4F7C04AAC0C59282916EDD`
  (322,001 bytes, 25 pages); the arXiv source is
  `F1E614CE592CDDC058F90FDCCEF4651F42663DD164FD59FC02FD935FBC17F032`
  (141,592 bytes) and the arXiv PDF is
  `E2939B632D2A5FAB2AC9BEAECC5084D0C556AFADE6BFFC97994532D310083430`
  (323,588 bytes, 28 pages).
- Updated QA hash pins, build records, export READMEs, manifest, and packages.

### Validation

- Canonical build: 25 pages, 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull
  hboxes, 3 cosmetic underfull hboxes, and 1 stable label warning.
- Standalone export: 25 pages, 0 fatal errors, 0 overfull hboxes, 3 underfull
  hboxes, and 1 stable label warning.
- arXiv build: 28 pages, 0 missing glyphs, 0 fatal errors, 0 overfull hboxes,
  4 cosmetic underfull hboxes, and 1 stable label warning.
- Abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`;
  the reference list remains eight entries; H4 and H7 remain `UNTESTED`.
- All three PDFs contain zero `LMMono*-Italic` spans.
- Manifest, review package, arXiv package, repository QA suite, TraceGrant Task
  D suite, E1/SA/boundary checks, and extracted-package rebuilds were verified
  after generation. `dist/sanitized` remains untouched.
- No arXiv submission, public release, license, DOI, or repository visibility
  change has occurred.

## [0.1.5] - 2026-10-28

### Changed

- 28 October 2026 path-format correction: inline code and artifact paths now
  render upright monospace, including spans inside notes; italic monospace is
  prohibited by the build header. The artifact-root key is defined once in
  Section 3.5, Table 12 and the Appendix cross-reference it, long path
  parentheticals were shortened, and italic note lead-ins became bold run-in
  labels.
- Refreshed the canonical 26 October PDF, standalone LaTeX export, and
  28-page arXiv candidate. The manuscript is now
  `3C93BE57592BC022DCE353867E44273F41251DDF0FF849C2F95A7028DB4DA08A`;
  the canonical PDF is
  `BC6AB2C5A82654D7FC3831AE4B7CEA66EE4A4C38A5ABF5924BC8EC65F236C544`;
  the standalone `main.tex` is
  `ED7970DFA49DB36B3759B3ED59700679C81EED91BFA326723503C5670E9A8515`;
  the standalone PDF is
  `9B569A258F2510DC0823BDB839FFE9511CE4DE34171E5670EF30D35A17E20B7D`;
  the arXiv source is
  `FCA5B98B2C209BA72EC8FFEBDE792FFB450C48660D1E6C7A999B81E4D467C007`;
  and the arXiv PDF is
  `7B8E8E7B6E167C9E4523BBA2B1F6F752F04FBA5FFA64D254E54AC5CAB4986165`.
- Updated state docs, QA hash pins, build records, and export READMEs for the
  28 October build.

### Validation

- Canonical build: 25 pages, 321,990 bytes, 0 missing glyphs, 0 fatal LaTeX
  errors, 0 overfull hboxes, 3 cosmetic underfull hboxes, 6 ignored
  infinite-glue-shrinkage diagnostics, and 1 stable label warning.
- Standalone export: 25 pages, 321,988 bytes, 0 fatal errors, 0 overfull
  hboxes, 3 underfull hboxes, and 1 stable label warning.
- arXiv build: 28 pages, 323,573 bytes, 0 missing glyphs, 0 fatal LaTeX errors,
  0 overfull hboxes, 4 cosmetic underfull hboxes, and 1 stable label warning.
- All three PDFs contain zero `LMMono*-Italic` spans; all tested artifact paths
  render upright and break at path separators rather than mid-word.
- Abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`;
  the static reference list remains eight entries; H4 and H7 remain
  `UNTESTED`.
- No new claims, experiments, or references were added.
- The regenerated manifest and release packages were verified after generation;
  the repository QA suite and TraceGrant Task D suite passed; `dist/sanitized`
  remains untouched.
- No arXiv submission, public release, license, DOI, or repository visibility
  change has occurred.

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
