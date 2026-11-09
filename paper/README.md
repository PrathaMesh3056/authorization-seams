# Paper sources

This directory contains the manuscript source and canonical build. The frozen
claim authority (`CONSOLIDATED_CLAIMS.md`) is mirrored read-only under
`paper/authority/`; the frozen predecessor (`MANUSCRIPT.md`) remains in the
project archive. See `docs/REVIEW_CORRECTIONS_2026-10-21.md` for what was
superseded and why.

| Path | Contents |
|---|---|
| `MANUSCRIPT_REVISED.md` | Manuscript source; the only build input |
| `hashes.txt` | Frozen Table 15 hashes; do not edit |
| `authority/` | Frozen claim authority and reference-verification records; internal review only |
| `drafts/MANUSCRIPT_DRAFT_2026-11-09.pdf` | Canonical 38-page named-author preprint PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-11-08.pdf` | Archived 8 November canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-11-07.pdf` | Archived 7 November canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-11-06.pdf` | Archived 6 November canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-11-05.pdf` | Archived 5 November canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-31.pdf` | Archived 31 October canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf` | Archived 23 October canonical PDF |
| `drafts/MANUSCRIPT_DRAFT_2026-10-21.pdf` | Archived 21 October PDF |
| `figures/` | Canonical vector figures and their recorded hashes |
| `build/` | Pandoc + XeLaTeX build scripts and preamble |
| `latex_export/` | Standalone single-file LaTeX source and reference PDF |
| `arxiv_export/` | 42-page arXiv-compliant named-author build (1-inch margins) |

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
  margins, 38 pages, 21 tables (19 labeled, including Appendix Tables A1 and
  A2).
- arXiv candidate: single-column `article`-class, letter paper, 10 pt, 1-inch
  margins, 42 pages; see `arxiv_export/README.md` and `docs/ARXIV_BUILD_QA.md`.
- 21 static reference entries, both figures vector in both builds.
- Abstract: 230 words; SHA-256
  `3BDB1BA2BA53DBC95BB96DE5C950B5498E6F1C0742F3C67EE87C61559A211D92`.
- Named-author build: the canonical title page and PDF metadata name
  `Prathamesh N Patil`; the arXiv candidate uses the same form, matching
  `CITATION.cff`. Public contact information is not printed. A double-blind
  venue would require re-anonymization.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  recorded canonical build; five cosmetic underfull hboxes, eight ignored
  infinite-glue-shrinkage diagnostics, and one stable label warning remain.
  The arXiv candidate has zero missing glyphs, zero errors, zero overfull
  hboxes, three cosmetic underfull hboxes, and the same stable label warning.
- The final public contact address is a pending release decision.
- The mandatory Declarations section is present; the author has confirmed no
  external funding, no competing interests, full single-author CRediT roles,
  and author-retained data availability. Confirm these again before submission.
- The 8-9 November second external-review completion pass retitled the paper,
  rewrote the abstract to 230 words, reframed E1 as a widened derivation with
  byte-identical receiver contracts in arms 2 and 5, disclosed the absence of a
  native receiver baseline, and added a source line under every table; see
  `docs/RESEARCH_STATUS.md`.
- The 7 November external-review reconciliation changed the E1 framing, added
  Pilot 1's 8/40 falsified-prediction disclosure, restored H1's resource clause
  to "not supported" per the frozen authority, and corrected the Table 12
  boundary denominator; see `docs/RESEARCH_STATUS.md`.
- `paper/hashes.txt` is frozen and its header says "Table 15"; the current
  artifact-hash ledger in the manuscript is Table 17. The frozen file is not
  edited; this note records the numbering drift only.

## Scope

- The manuscript is prepared for workshop/short-paper or tool-track/arXiv
  submission, not a main-track submission.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiment is part of this package.
- Progent is related work only. No Progent figure is reproduced, re-measured,
  or compared.
- RFC 8693, Zanzibar, and Macaroons are verified adjacent pointers only; none is
  a baseline or a reproduced result.
