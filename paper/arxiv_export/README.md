# arXiv-compliant named-author export

This directory is the **arXiv submission candidate** for the manuscript. It is
not a public release and it has not been submitted.

It is generated from the frozen standalone LaTeX export by
`paper/build/build_arxiv.py`. The frozen canonical build remains
`paper/latex_export/` and `paper/drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf`; neither
is modified by this export.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Generated arXiv source: 1-inch margins, 10 pt, named author |
| `main.pdf` | 27-page reference compile of this source |
| `figures/figure_1_handoff_anatomy.pdf` | Canonical Figure 1, vector PDF, byte-identical copy |
| `figures/figure_2_repair_loci.pdf` | Canonical Figure 2, vector PDF, byte-identical copy |
| `ARXIV_METADATA.md` | Proposed arXiv metadata and remaining author decisions |
| `README.md` | This file |

## Build

From the repository root:

```powershell
python paper/build/build_arxiv.py
```

The script verifies the frozen `paper/latex_export/main.tex` SHA-256, applies
only these changes, and compiles with XeLaTeX three times:

- `margin=0.75in` becomes `margin=1in` (arXiv minimum);
- the author display name and PDF metadata become `Prathamesh N Patil`;
- Figure 2 is fitted to `\linewidth` instead of a fixed 7-inch width.

No manuscript sentence, number, table, reference, figure, or hypothesis status
is changed. The generated `main.tex` differs from the frozen export only in
those six content lines plus the build header.

## Verified output

- 27 pages, US Letter (612 x 792 pt), 10 pt body type, 1-inch geometry.
- 0 missing glyphs, 0 LaTeX errors, 0 overfull hboxes.
- 4 cosmetic underfull hboxes and 1 stable `Label(s) may have changed` warning.
- All fonts embedded; both figures are vector; `pdfimages` reports zero raster
  images.
- Title-page and PDF metadata author: `Prathamesh N Patil`.
- Abstract unchanged: 222 words, SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- Eight static reference entries; H4 and H7 remain `UNTESTED`.
- No public email, repository URL, DOI, or license is printed.

The canonical 24-page PDF is unchanged and still uses the historical
`Prathamesh Patil` title-page/metadata string. The arXiv candidate uses the
`Prathamesh N Patil` form already recorded in `CITATION.cff`.

## Remaining submission gates

arXiv endorsement, license selection, public contact email, ORCID (optional),
repository URL, archival DOI, and release sanitization remain owner decisions.
A double-blind venue would require a separate anonymized build; this one is
named-author.
