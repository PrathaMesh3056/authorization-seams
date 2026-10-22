# Changelog

All notable changes to this repository are recorded here. The experiment
artifacts themselves are frozen; changes to them are never made in place.

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
