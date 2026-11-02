# arXiv build QA - 31 October 2026

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

The canonical 31 October PDF is a 29-page, single-column, named-author build
with **0.75-inch margins**. arXiv requires a **minimum 1-inch page margin** and
10-14 pt type. Uploading the canonical PDF as-is would risk a format
correction. The canonical PDF and standalone LaTeX export were refreshed for
the 31 October review-correction pass, but the arXiv layout remains a separate
candidate generated from that export. The 23 October 24-page PDF remains
archived.

The same review also confirmed that arXiv is named-author (no anonymity), while
CODASPY 2027 requires a 12-page double-column anonymized research submission
(abstract 16 November 2026; paper 23 November 2026). The current 29-page
single-column paper is not a CODASPY-ready submission.

## Inputs and build

| Item | Value |
|---|---|
| Current manuscript | `paper/MANUSCRIPT_REVISED.md` |
| Manuscript SHA-256 | `79CB8E608CD516B18077943E10433A8F22C834B05AD5D19156330B53B258A876` |
| Current LaTeX source | `paper/latex_export/main.tex` |
| LaTeX source SHA-256 | `0EDEC38B19B0836B5E52B0626C60CECCD7533665CD69BFDB19D5C6CCA468A1BA` |
| Build script | `paper/build/build_arxiv.py` |
| Output source | `paper/arxiv_export/main.tex` |
| Output PDF | `paper/arxiv_export/main.pdf` |
| Toolchain | Pandoc 3.12.1 (source export) + XeLaTeX 4.16 / MiKTeX 25.12 |

The build script verifies the pinned source hash before writing anything. It
applies only the following changes:

1. `margin=0.75in` to `margin=1in`;
2. author display name and PDF metadata to `Prathamesh N Patil` (matching
   `CITATION.cff`);
3. Figure 2 from a fixed 7-inch width to `\linewidth`, so it fits the 1-inch
   text measure.

A line-level diff against the current source export shows exactly those six
changed content lines (one margin line, four author-metadata lines, and one
Figure 2 width line) plus the generated-file header. No sentence, number,
table, reference, figure, or hypothesis status changed.

## Output checks

| Check | Result |
|---|---|
| Pages | 32 |
| Page size | 612 x 792 pt (US Letter) |
| Body type | 10 pt |
| Margins | 1-inch geometry; text line boxes at 72 pt |
| PDF SHA-256 | `33207E1E00DB205F3C123C763EDC8FC978C959C2417EB2B4AC4B68D304933CE1` |
| PDF size | 340,381 bytes |
| Source SHA-256 | `52F399DBDC3B65B54B751A2D85ACCBD3ADB21E7F9EB77DDE33F239F0AF1818A5` |
| Source size | 159,328 bytes |
| Missing glyphs | 0 |
| Fatal LaTeX errors | 0 |
| Overfull hboxes | 0 |
| Underfull hboxes | 4 cosmetic |
| Ignored infinite-glue diagnostics | 2, non-fatal |
| Label warning | 1 stable `Label(s) may have changed` warning |
| Embedded fonts | All fonts embedded |
| Raster images | 0; both figures are vector |
| PDF metadata author | `Prathamesh N Patil` |
| Title page author | `Prathamesh N Patil` |
| Public email printed | No |
| Repository URL printed | No |
| Manuscript DOI printed | No; the reference list cites external DOIs |
| License printed | No |

The page count increased from 29 to 32 because the text measure narrowed from
7.0 to 6.5 inches. That is a deliberate layout consequence, not a content
revision.

Some text bounding boxes report an x-coordinate a few points below 72 pt
because of glyph side bearings (for example, italic or table glyphs). The
geometry package still sets the line boxes at the 1-inch margin; no line or
table overflows the page.

## Content-preservation checks

- Abstract: 278 words; SHA-256
  `060C2D9F7A78D8E346DC4B8A3BA8278BFD5A34883E6B33CED33CAC90A0D57CD7`.
- Static reference list: 8 entries.
- H4 and H7: `UNTESTED` in the source and the PDF.
- Progent: related work only; no reproduced figure or comparison.
- The 31 October canonical PDF and current LaTeX export remain unchanged by
  this export. The 23 October 24-page PDF remains archived.
- Both arXiv figures are byte-identical copies of the canonical vector PDFs.
- No internal placeholder email, local Windows path, or token-shaped secret
  appears in the generated source or PDF text.
- No line numbers or watermark.

## 31 October review-correction pass

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and ★ are `REFINED`; H1's resource clause is `UNTESTED`; H4 and H7
  remain `UNTESTED`.
- Abstract: 278 words; eight references.
- The generated source and PDF above reflect this build.

## 28 October path-format and disclosure revision (historical)

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- The upstream export now forces upright `\texttt` and `\path` rendering, so
  code and paths inside notes are upright monospace rather than italic
  monospace. The arXiv PDF contains zero `LMMono*-Italic` spans.
- The artifact-root key is defined once in Section 3.5; Table 12 and the
  Appendix cross-reference it. Long path parentheticals were shortened, and
  italic note lead-ins became bold run-in labels.
- The revision changed no claim, number, reference, table datum, figure, or
  H4/H7 status. At that revision the abstract remained 222 words and the
  reference list remained eight entries.

## Visual review

The 28 October build was visually reviewed on pages 1, 7, 13, 16, 18, 27, and
28; the title page, the Table 2/Table 3 page, the SentinelAgent and boundary
reconciliation notes, Figure 2 and Table 12, the Appendix A/Table A1 page, and
the reference list showed no clipping, overlap, missing glyph, or broken table.
The 31 October build was checked mechanically on all 32 pages for page count,
text presence, text bounds, embedded fonts, metadata, and zero raster images;
no text block falls outside its page.

## Packaging checks

- The last generated arXiv source package is
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip` (26 October; historical),
  160,358 bytes, SHA-256
  `615962B8590C830E92625EED88F40D42F3D6C1F4A8031B6975599A95192C030A`.
  At that time it contained `main.tex` and the two vector figures, and extracted
  cleanly to 28 pages. It predates the 31 October rebuild and was not
  regenerated.
- The last review package is `dist/seam-conformance-kit-20261027-review.zip`
  (27 October; historical). It predates the 31 October review-correction pass;
  no new package has been generated.
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
