# arXiv-compliant named-author export

This directory is the **arXiv submission candidate** for the manuscript. It is
not a public release and it has not been submitted.

It is generated from the current standalone LaTeX export by
`paper/build/build_arxiv.py`. The canonical build remains
`paper/latex_export/` and `paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf`; neither
is modified by this export. The export was refreshed on 28 October 2026 for
the inline code/path formatting correction and AI-use disclosure revision.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Generated arXiv source: 1-inch margins, 10 pt, named author |
| `main.pdf` | 28-page reference compile of this source |
| `figures/figure_1_handoff_anatomy.pdf` | Canonical Figure 1, vector PDF, byte-identical copy |
| `figures/figure_2_repair_loci.pdf` | Canonical Figure 2, vector PDF, byte-identical copy |
| `ARXIV_METADATA.md` | Proposed arXiv metadata and remaining author decisions |
| `README.md` | This file |

## Build

From the repository root:

```powershell
python paper/build/build_arxiv.py
```

The script verifies the pinned `paper/latex_export/main.tex` SHA-256
(`A632B591801FA6E80D203E8D4D7085E2866A4EACF62F8C3CDF2908F08B0A68DA`), applies
only these changes, and compiles with XeLaTeX three times:

- `margin=0.75in` becomes `margin=1in` (arXiv minimum);
- the author display name and PDF metadata become `Prathamesh N Patil`;
- Figure 2 is fitted to `\linewidth` instead of a fixed 7-inch width.

This export changes no manuscript sentence, number, table, reference, figure,
or hypothesis status. The generated `main.tex` differs from the source export
only in those content lines plus the build header.

## Verified output

- 32 pages, 340,381 bytes, US Letter (612 x 792 pt), 10 pt body type, 1-inch
  geometry.
- 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- 4 cosmetic underfull hboxes and 1 stable `Label(s) may have changed` warning.
- All fonts embedded; both figures are vector; `pdfimages` reports zero raster
  images.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain.
- Title-page and PDF metadata author: `Prathamesh N Patil`.
- Abstract unchanged: 222 words, SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- Sixteen pipe tables, including Appendix Table A1; eight static reference
  entries; H4 and H7 remain `UNTESTED`.
- No public email, repository URL, DOI, or license is printed.
- Generated source: 141,592 bytes, SHA-256
  `F1E614CE592CDDC058F90FDCCEF4651F42663DD164FD59FC02FD935FBC17F032`.
- Reference PDF: 323,588 bytes, SHA-256
  `E2939B632D2A5FAB2AC9BEAECC5084D0C556AFADE6BFFC97994532D310083430`.

The canonical 25-page PDF uses the historical `Prathamesh Patil`
title-page/metadata string. The arXiv candidate uses the `Prathamesh N Patil`
form already recorded in `CITATION.cff`.

## 28 October path-format and disclosure revision

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- The upstream export now forces upright `\texttt` and `\path` rendering, so
inline code and paths inside notes are upright monospace. The artifact-root key
is defined once in Section 3.5, Table 12 and the Appendix cross-reference it,
and long path parentheticals were shortened. No claim, number, reference, table
datum, figure, or H4/H7 status changed; the abstract remains 222 words and the
reference list remains eight entries.

## Remaining submission gates

arXiv endorsement, license selection, public contact email, ORCID (optional),
repository URL, archival DOI, and release sanitization remain owner decisions.
A double-blind venue would require a separate anonymized build; this one is
named-author.
