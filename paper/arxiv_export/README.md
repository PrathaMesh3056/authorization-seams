# arXiv-compliant named-author export

This directory is the **arXiv submission candidate** for the manuscript. It is
not a public release and it has not been submitted.

It is generated from the current standalone LaTeX export by
`paper/build/build_arxiv.py`. The canonical build remains
`paper/latex_export/` and `paper/drafts/MANUSCRIPT_DRAFT_2026-10-31.pdf`; neither
is modified by this export. The export was refreshed on 31 October 2026 for
the five-seat review correction pass.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Generated arXiv source: 1-inch margins, 10 pt, named author |
| `main.pdf` | 32-page reference compile of this source |
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
(`0EDEC38B19B0836B5E52B0626C60CECCD7533665CD69BFDB19D5C6CCA468A1BA`), applies
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
- Abstract: 278 words, SHA-256
  `060C2D9F7A78D8E346DC4B8A3BA8278BFD5A34883E6B33CED33CAC90A0D57CD7`.
- Twenty pipe tables (18 labeled, including Appendix Table A1); eight static reference
  entries; H4 and H7 remain `UNTESTED`.
- No public email, repository URL, DOI, or license is printed.
- Generated source: 159,328 bytes, SHA-256
  `52F399DBDC3B65B54B751A2D85ACCBD3ADB21E7F9EB77DDE33F239F0AF1818A5`.
- Reference PDF: 340,381 bytes, SHA-256
  `33207E1E00DB205F3C123C763EDC8FC978C959C2417EB2B4AC4B68D304933CE1`.

The canonical 29-page PDF uses the historical `Prathamesh Patil`
title-page/metadata string. The arXiv candidate uses the `Prathamesh N Patil`
form already recorded in `CITATION.cff`.

## 28 October path-format and disclosure revision (historical)

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- The upstream export now forces upright `\texttt` and `\path` rendering, so
inline code and paths inside notes are upright monospace. The artifact-root key
is defined once in Section 3.5, Table 12 and the Appendix cross-reference it,
and long path parentheticals were shortened. No claim, number, reference, table
datum, figure, or H4/H7 status changed; at that revision the abstract remained
222 words and the reference list remained eight entries.

## 31 October review-correction pass

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and ★ are `REFINED`; H1's resource clause is `UNTESTED`; H4 and H7
  remain `UNTESTED`.
- The abstract is now 278 words; the reference list remains eight entries.
- The generated source and reference PDF above reflect this build.

## Remaining submission gates

arXiv endorsement, license selection, public contact email, ORCID (optional),
repository URL, archival DOI, and release sanitization remain owner decisions.
A double-blind venue would require a separate anonymized build; this one is
named-author.
