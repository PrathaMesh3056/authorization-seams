# Changelog

All notable changes to this repository are recorded here. The experiment
artifacts themselves are frozen; changes to them are never made in place.

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
