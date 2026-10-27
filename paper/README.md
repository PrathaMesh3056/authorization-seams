# Paper sources

This directory contains the manuscript source and canonical build. The frozen
predecessor (`MANUSCRIPT.md`) and the frozen claim authority
(`CONSOLIDATED_CLAIMS.md`) are **not** included here; they remain in the project
archive. See `docs/REVIEW_CORRECTIONS_2026-10-21.md` for what was superseded
and why.

| Path | Contents |
|---|---|
| `MANUSCRIPT_REVISED.md` | Manuscript source; the only build input |
| `hashes.txt` | Frozen Table 15 hashes; do not edit |
| `drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf` | Canonical 25-page named-author preprint PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf` | Archived 23 October canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-21.pdf` | Archived 21 October PDF |
| `figures/` | Canonical vector figures and their recorded hashes |
| `build/` | Pandoc + XeLaTeX build scripts and preamble |
| `latex_export/` | Frozen standalone single-file LaTeX source and reference PDF |
| `arxiv_export/` | 28-page arXiv-compliant named-author build (1-inch margins) |

## Build

```powershell
pwsh -File paper/build/build.ps1
# or
bash paper/build/build.sh

# arXiv-compliant candidate (1-inch margins)
python paper/build/build_arxiv.py
```

The build checks the manuscript SHA-256 before doing anything. If the hash does
not match `EXPECTED_SHA` in `build/preprocess.py`, the build stops. That is the
intended behavior for a frozen manuscript.

The canonical PDF is not overwritten by the build. A successful build writes
`build/manuscript_build_wide.pdf`; compare it against the canonical PDF
deliberately if you intend to refresh the manuscript.

## Manuscript facts

- Canonical build: single-column `article`-class, letter paper, 10 pt, 0.75 in
  margins, 25 pages, 16 tables including Appendix Table A1.
- arXiv candidate: single-column `article`-class, letter paper, 10 pt, 1-inch
  margins, 28 pages; see `arxiv_export/README.md` and `docs/ARXIV_BUILD_QA.md`.
- 8 static reference entries, both figures vector in both builds.
- Named-author build: the canonical title page and PDF metadata name
  Prathamesh Patil; the arXiv candidate uses `Prathamesh N Patil` to match
  `CITATION.cff`. Public contact information is not printed. A double-blind
  venue would require re-anonymization.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  recorded canonical build; three cosmetic underfull hboxes, six ignored
  infinite-glue-shrinkage diagnostics, and one stable label warning remain.
- The final public contact address is a pending release decision.

## Scope

- The manuscript is prepared for workshop/short-paper or tool-track/arXiv
  submission, not a main-track submission.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiment is part of this package.
- Progent is related work only. No Progent figure is reproduced, re-measured,
  or compared.
