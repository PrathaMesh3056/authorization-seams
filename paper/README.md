# Paper sources

This directory contains the corrected draft. The frozen predecessor
(`MANUSCRIPT.md`) and the frozen claim authority (`CONSOLIDATED_CLAIMS.md`) are
**not** included here; they remain in the internal working archive. See
`docs/REVIEW_CORRECTIONS_2026-10-21.md` for what was superseded and why.

| Path | Contents |
|---|---|
| `MANUSCRIPT_REVISED.md` | Corrected manuscript source; the only build input |
| `hashes.txt` | Frozen Table 15 hashes; do not edit |
| `drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf` | Canonical 24-page named-author draft PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-21.pdf` | Archived 21 October draft PDF |
| `figures/` | Canonical vector figures and their recorded hashes |
| `build/` | Pandoc + XeLaTeX build scripts and preamble |
| `latex_export/` | Standalone single-file LaTeX source and reference PDF |

## Build

```powershell
pwsh -File paper/build/build.ps1
# or
bash paper/build/build.sh
```

The build checks the manuscript SHA-256 before doing anything. If the hash does
not match `EXPECTED_SHA` in `build/preprocess.py`, the build stops. That is the
intended behavior for a frozen draft.

The canonical PDF is not overwritten by the build. A successful build writes
`build/manuscript_build_wide.pdf`; compare it against the canonical draft
deliberately if you intend to refresh the draft.

## Draft facts

- Single-column `article`-class, letter paper, 10 pt, 0.75 in margins.
- 24 pages, 8 static reference entries, both figures vector.
- Named-author build: the title page and PDF metadata name Prathamesh Patil;
  the placeholder email is not printed. A double-blind venue would require
  re-anonymization.
- Zero missing glyphs, zero LaTeX errors, zero overfull hboxes in the recorded
  build; three cosmetic underfull hboxes and one stable label warning remain.
- The author email is intentionally not printed. The final public address is an
  open release gate.

## Scope

- The draft is a workshop/short-paper or tool-track/arXiv candidate, not a
  main-track submission.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiment is part of this package.
- Progent is related work only. No Progent figure is reproduced, re-measured,
  or compared.
