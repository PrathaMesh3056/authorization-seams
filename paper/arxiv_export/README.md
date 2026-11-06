# arXiv-compliant named-author export

This directory is the **arXiv submission candidate** for the manuscript. It is
not a public release and it has not been submitted.

It is generated from the current standalone LaTeX export by
`paper/build/build_arxiv.py`. The canonical build remains
`paper/latex_export/` and `paper/drafts/MANUSCRIPT_DRAFT_2026-11-06.pdf`; neither
is modified by this export. The export was rebuilt on 6 November 2026 for the
positioning and related-work revision.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Generated arXiv source: 1-inch margins, 10 pt, named author |
| `main.pdf` | 35-page reference compile of this source |
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
(`C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139`), applies
only these changes, and compiles with XeLaTeX three times:

- `margin=0.75in` becomes `margin=1in` (arXiv minimum);
- the author display name and PDF metadata become `Prathamesh N Patil`;
- Figure 2 is fitted to `\linewidth` instead of a fixed 7-inch width.

This export changes no manuscript sentence, number, table, reference, figure,
or hypothesis status. The generated `main.tex` differs from the source export
only in those content lines plus the build header.

## Verified output

- 35 pages, 358,240 bytes, US Letter (612 x 792 pt), 10 pt body type, 1-inch
  geometry.
- 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- 4 cosmetic underfull hboxes and 1 stable `Label(s) may have changed` warning.
- All fonts embedded; both figures are vector; `pdfimages` reports zero raster
  images.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain.
- Title-page and PDF metadata author: `Prathamesh N Patil`.
- Abstract: 222 words, SHA-256
  `35C17A00CBB3A15B5C67298F45E37FE7D663275A65A1CB38DA78BB84FDF89F45`.
- Twenty-one pipe tables (19 labeled, including Appendix Tables A1 and A2);
  twenty-one static reference entries; H4 and H7 remain `UNTESTED`.
- No public email, repository URL, DOI, or license is printed.
- Generated source: 175,158 bytes, SHA-256
  `2E0C4C858E3CD941D0FEDE1E0FB78CF6C607547BFA49738DB2886C151D298D25`.
- Reference PDF: 358,240 bytes, SHA-256
  `84DADE9A8B83EB5C8D0DCEED975A15984B63DC0CCBB7BC07E471067D18DEDAF0`.

The canonical 32-page PDF uses the historical `Prathamesh Patil`
title-page/metadata string. The arXiv candidate uses the `Prathamesh N Patil`
form already recorded in `CITATION.cff`.

## Source package

`dist/arxiv/authorization-seams-arxiv-2026-11-06.zip` is the upload candidate.
It is 169,835 bytes, SHA-256
`DED4065954CFE8538D58057D8948F66A65BBCA978C738801320514733C083483`, and
contains only `main.tex` (pinned SHA-256
`2E0C4C858E3CD941D0FEDE1E0FB78CF6C607547BFA49738DB2886C151D298D25`) plus the
two vector figures. It was extracted into an empty directory and compiled three
times with pdfTeX 1.40.28; the clean-room PDF is 35 pages with 0 fatal errors,
0 overfull hboxes, 2 cosmetic underfull hboxes, and 0 missing characters. The
zip does not include the reference PDF or any build artifacts.

## 6 November 2026 revision

- Section 6 restructured and deduplicated. Ten verified references added:
  RFC 9396, RFC 2693, Miller's *Robust Composition*, Blaze et al., Appel and
  Felten, Fong, Parisel, ChainCaps, Overlaying Governance, and Local Allow,
  Global Deny. The reference list grew from eleven to twenty-one entries.
- The Introduction's scope paragraph now matches the expanded positioning;
  Section 7.3 gained a design-space rationale.
- Abstract unchanged at 222 words; no new experiment, count, claim, status, or
  frozen artifact changed. H4 and H7 remain `UNTESTED`.

## 5 November 2026 revision (historical)

- Abstract trimmed from 278 to 222 words; no new number, claim, status, or
  citation was added.
- Added mandatory Declarations: data availability, ethics, author
  contributions/CRediT, competing interests, funding, limitations. Author-specific
  CRediT, competing-interest, and funding confirmations remain pending rather
  than invented.
- Added three verified adjacent pointers (RFC 8693, Zanzibar, Macaroons) and a
  falsification/stop-condition paragraph; added effective-witness Appendix
  Table A2; added `report-only` qualifiers to the E1 8/8 `EVIDENCE-VERIFIED`
  cells; added an explicit H4/H7 gate.
- The reference list grew from eight to eleven entries. No frozen artifact was
  edited.

## 31 October review-correction pass (historical)

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and the zero-novelty finding are `REFINED`; H1's resource clause is
  `UNTESTED`; H4 and H7 remain `UNTESTED`.
- The abstract was 278 words at that point.

## Remaining submission gates

arXiv endorsement, license selection, public contact email, ORCID (optional),
repository URL, archival DOI, and release sanitization remain owner decisions.
A double-blind venue would require a separate anonymized build; this one is
named-author.
