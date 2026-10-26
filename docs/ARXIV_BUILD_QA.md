# arXiv build QA - 26 October 2026

**Target:** arXiv preprint, initial submission, named-author build.
**Official sources checked 26 October 2026:**

- arXiv format requirements:
  <https://info.arxiv.org/help/policies/format_requirements.html>
- arXiv licenses:
  <https://info.arxiv.org/help/license/index.html>
- arXiv endorsement:
  <https://info.arxiv.org/help/endorsement.html>
- arXiv endorsement policy update, 21 January 2026:
  <https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy>
- ACM preprint policy:
  <https://www.acm.org/publications/policies/roles-and-responsibilities>
- CODASPY 2027 CFP, for route comparison:
  <https://www.codaspy.org/2027/cfp.html>

This record documents a **build**, not a submission. No arXiv account action,
license choice, endorsement request, public release, or DOI assignment has been
made.

## Why a separate build was needed

The canonical 23 October PDF is a 24-page, single-column, named-author build
with **0.75-inch margins**. arXiv requires a **minimum 1-inch page margin** and
10-14 pt type. Uploading the canonical PDF as-is would risk a format
correction. The canonical PDF and frozen LaTeX export are therefore unchanged;
a separate arXiv candidate was generated.

The same review also confirmed that arXiv is named-author (no anonymity), while
CODASPY 2027 requires a 12-page double-column anonymized research submission
(abstract 16 November 2026; paper 23 November 2026). The current 24-page
single-column paper is not a CODASPY-ready submission.

## Inputs and build

| Item | Value |
|---|---|
| Frozen manuscript | `paper/MANUSCRIPT_REVISED.md` |
| Manuscript SHA-256 | `84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66` |
| Frozen LaTeX source | `paper/latex_export/main.tex` |
| Frozen LaTeX SHA-256 | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| Build script | `paper/build/build_arxiv.py` |
| Output source | `paper/arxiv_export/main.tex` |
| Output PDF | `paper/arxiv_export/main.pdf` |
| Toolchain | Pandoc 3.12.1 (source export) + XeLaTeX 4.16 / MiKTeX 25.12 |

The build script verifies the frozen source hash before writing anything. It
applies only the following changes:

1. `margin=0.75in` to `margin=1in`;
2. author display name and PDF metadata to `Prathamesh N Patil` (matching
   `CITATION.cff`);
3. Figure 2 from a fixed 7-inch width to `\linewidth`, so it fits the 1-inch
   text measure.

A line-level diff against the frozen export shows exactly those six changed
content lines (one margin line, four author-metadata lines, and one Figure 2
width line) plus the generated-file header. No sentence, number, table,
reference, figure, or hypothesis status changed.

## Output checks

| Check | Result |
|---|---|
| Pages | 27 |
| Page size | 612 x 792 pt (US Letter) |
| Body type | 10 pt |
| Margins | 1-inch geometry; text line boxes at 72 pt |
| PDF SHA-256 | `6A023B39741D6F52852C7883EEA94EF3DA4108DB7B8AE10318272FC3B4D593E3` |
| PDF size | 324,267 bytes |
| Source SHA-256 | `C6C350D856DEA6F842F9B3A6F95E108643372BF9007616D0749A784038670C93` |
| Source size | 135,931 bytes |
| Missing glyphs | 0 |
| LaTeX errors | 0 |
| Overfull hboxes | 0 |
| Underfull hboxes | 4 cosmetic |
| Label warning | 1 stable `Label(s) may have changed` warning |
| Embedded fonts | All fonts embedded |
| Raster images | 0; both figures are vector |
| PDF metadata author | `Prathamesh N Patil` |
| Title page author | `Prathamesh N Patil` |
| Public email printed | No |
| Repository URL printed | No |
| DOI printed | No |
| License printed | No |

The page count increased from 24 to 27 because the text measure narrowed from
7.0 to 6.5 inches. That is a deliberate layout consequence, not a content
revision.

Some text bounding boxes report an x-coordinate a few points below 72 pt
because of glyph side bearings (for example, italic or table glyphs). The
geometry package still sets the line boxes at the 1-inch margin; no line or
table overflows the page.

## Content-preservation checks

- Abstract: 222 words; SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- Static reference list: 8 entries.
- H4 and H7: `UNTESTED` in the source and the PDF.
- Progent: related work only; no reproduced figure or comparison.
- The canonical 24-page PDF and frozen LaTeX source remain byte-identical.
- Both arXiv figures are byte-identical copies of the canonical vector PDFs.
- No internal placeholder email, local Windows path, or token-shaped secret
  appears in the generated source or PDF text.
- No line numbers or watermark.

## Visual review

Pages 1, 4, 18, 23, and 27 were rendered at 110 dpi and inspected. The title
page, a dense table page, Figure 2, the threats section, and the reference list
show no clipping, overlap, missing glyph, or broken table. All 27 pages were
checked mechanically for text presence, text bounds, embedded images, and
drawing content.

## Packaging checks

- arXiv source package:
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip` (158,232 bytes;
  SHA-256 `75CAFCA9C1D5E7CDFE49FAF0C05C3C2D30BBE6ACCB897933E2C01A74796EB417`).
  It contains `main.tex` and the two vector figures. Extracted into a clean
  temporary directory, it compiles to 27 pages with 0 missing glyphs, 0 LaTeX
  errors, 0 overfull hboxes, 4 underfull hboxes, and 1 stable label warning.
- Review package: `dist/seam-conformance-kit-20261026-review.zip`. It extracts,
  verifies 306 tracked files, passes the 15 repository QA tests, and rebuilds
  the arXiv candidate to 27 pages. The current checksum is in the adjacent
  `.sha256` sidecar; it changes when tracked documentation changes.
- The review package is **not** a public-release package: frozen evidence and
  toolchain notes still contain machine-local paths. The sanitized tree remains
  the release path.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files.

## Remaining gates

- arXiv endorsement: the 21 January 2026 policy requires **both** an
  institutional email and prior arXiv authorship for automatic endorsement;
  otherwise personal endorsement from an established `cs.CR` author is needed.
- arXiv license: author choice; irrevocable per announced version. CC BY 4.0 is
  a common manuscript choice if there is no publisher conflict; the arXiv
  perpetual non-exclusive license is the restrictive fallback.
- Public contact email and optional ORCID.
- Public repository URL and archival DOI, if the paper is to link them.
- Release sanitization and license selection.
- CODASPY 2027, if pursued: separate 12-page double-column anonymized build,
  abstract by 16 November 2026, paper by 23 November 2026.
- Any double-blind venue requires a separate anonymized PDF and metadata.

## Gate reminder

This build does **not** close the release checklist. The repository remains
private; no public email, license, repository URL, archival DOI, or arXiv
submission has been created. H4 and H7 remain `UNTESTED`.
