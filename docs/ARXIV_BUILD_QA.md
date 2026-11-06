# arXiv build QA - 6 November 2026

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

The canonical 6 November PDF is a 32-page, single-column, named-author build
with **0.75-inch margins**. arXiv requires a **minimum 1-inch page margin** and
10-14 pt type. Uploading the canonical PDF as-is would risk a format
correction. The canonical PDF and standalone LaTeX export were refreshed for
the 6 November positioning and related-work revision, but the arXiv layout
remains a separate candidate generated from that export. The 5 November 31-page
and 31 October 29-page PDFs remain archived.

The same review also confirmed that arXiv is named-author (no anonymity), while
CODASPY 2027 requires a 12-page double-column anonymized research submission
(abstract 16 November 2026; paper 23 November 2026). The current 32-page
single-column paper is not a CODASPY-ready submission.

## Inputs and build

| Item | Value |
|---|---|
| Current manuscript | `paper/MANUSCRIPT_REVISED.md` |
| Manuscript SHA-256 | `76E9E8F6F7233121277B97C0363DF38AC05284F71CD52D26E33D6A8E098B1A98` |
| Current LaTeX source | `paper/latex_export/main.tex` |
| LaTeX source SHA-256 | `C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139` |
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
| Pages | 35 |
| Page size | 612 x 792 pt (US Letter) |
| Body type | 10 pt |
| Margins | 1-inch geometry; text line boxes at 72 pt |
| PDF SHA-256 | `84DADE9A8B83EB5C8D0DCEED975A15984B63DC0CCBB7BC07E471067D18DEDAF0` |
| PDF size | 358,240 bytes |
| Source SHA-256 | `2E0C4C858E3CD941D0FEDE1E0FB78CF6C607547BFA49738DB2886C151D298D25` |
| Source size | 175,158 bytes |
| Missing glyphs | 0 |
| Fatal LaTeX errors | 0 |
| Overfull hboxes | 0 |
| Underfull hboxes | 4 cosmetic |
| Label warning | 1 stable `Label(s) may have changed` warning |
| Embedded fonts | All fonts embedded |
| Raster images | 0; both figures are vector |
| PDF metadata author | `Prathamesh N Patil` |
| Title page author | `Prathamesh N Patil` |
| Public email printed | No |
| Repository URL printed | No |
| Manuscript DOI printed | No; the reference list cites external DOIs |
| License printed | No |

The page count increased from 34 to 35 because the 6 November revision expanded
Section 6 with ten verified references and added a design-space paragraph in
Section 7.3. That is deliberate content growth, not a layout regression. The
5 November build had grown from 32 to 34 pages for the Declarations section,
falsification/stop conditions, adjacent-work paragraph, and Appendix Table A2.

Some text bounding boxes report an x-coordinate a few points below 72 pt
because of glyph side bearings (for example, italic or table glyphs). The
geometry package still sets the line boxes at the 1-inch margin; no line or
table overflows the page.

## Content-preservation checks

- Abstract: 222 words; SHA-256
  `35C17A00CBB3A15B5C67298F45E37FE7D663275A65A1CB38DA78BB84FDF89F45`.
- Static reference list: 21 entries.
- H4 and H7: `UNTESTED` in the source and the PDF.
- Progent: related work only; no reproduced figure or comparison.
- The 5 November 31-page and 31 October 29-page PDFs remain archived.
- Both arXiv figures are byte-identical copies of the canonical vector PDFs.
- No internal placeholder email, local Windows path, or token-shaped secret
  appears in the generated source or PDF text.
- No line numbers or watermark.

## 6 November positioning and related-work revision

- Section 6 restructured and deduplicated; ten verified references added
  (RFC 9396, RFC 2693, Miller, Blaze et al., Appel and Felten, Fong, Parisel,
  ChainCaps, Overlaying Governance, Local Allow, Global Deny).
- The Introduction's scope paragraph now matches the expanded positioning, and
  Section 7.3 gained a design-space rationale.
- Abstract unchanged at 222 words; no measured claim, count, status, or frozen
  artifact changed. H4 and H7 remain `UNTESTED`.
- References: 21 entries.
- The generated source and PDF above reflect this build.

## 5 November declarations and positioning revision (historical)

## 31 October review-correction pass (historical)

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and ★ are `REFINED`; H1's resource clause is `UNTESTED`; H4 and H7
  remain `UNTESTED`.
- Abstract: 278 words; eight references.
- The 31 October build reflected that revision.

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
no text block falls outside its page. The 5 November build was checked the same
way on all 34 pages. The 6 November build was checked the same way on all 35
pages; no text block falls outside its page.

## Packaging checks

- **Current source package:** `dist/arxiv/authorization-seams-arxiv-2026-11-06.zip`,
  169,835 bytes, SHA-256
  `DED4065954CFE8538D58057D8948F66A65BBCA978C738801320514733C083483`.
  It contains only `main.tex` (175,158 bytes; pinned SHA-256
  `2E0C4C858E3CD941D0FEDE1E0FB78CF6C607547BFA49738DB2886C151D298D25`) and
  the two byte-identical vector figures under `figures/`. The archive is
  deterministic: sorted entries, fixed 6 November 2026 timestamps, no build
  artifacts.
- **Clean-room test (7 November 2026):** the zip was extracted into an empty
  temporary directory and compiled three times with pdfTeX 1.40.28
  (MiKTeX 25.12), using `-interaction=nonstopmode -halt-on-error`. All three
  runs exited 0. The resulting PDF is 35 pages, US Letter (612 x 792 pt),
  10 pt, with 0 fatal errors, 0 overfull hboxes, 2 cosmetic underfull hboxes,
  0 missing characters, and embedded subset fonts. Page 1 carries the title,
  `Prathamesh N Patil`, the SPIT affiliation, and the 222-word abstract;
  `UNTESTED` still appears for H4/H7; extracted text contains no public email,
  repository URL, or local Windows path.
- The clean-room PDF is a test artifact and is not committed. arXiv receives
  source only. `paper/arxiv_export/main.pdf` remains the XeLaTeX reference
  build (`84DADE9A8B83EB5C8D0DCEED975A15984B63DC0CCBB7BC07E471067D18DEDAF0`).
- **Historical:** `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip`
  (160,358 bytes; SHA-256
  `615962B8590C830E92625EED88F40D42F3D6C1F4A8031B6975599A95192C030A`)
  was the last package before the 6 November revision. It extracted cleanly to
  28 pages and predates the 31 October and 5 November rebuilds.
- The last review package is `dist/seam-conformance-kit-20261027-review.zip`
  (27 October; historical). It predates the 31 October review-correction pass
  and the 5 November declarations revision; no new package has been generated.
- The review package is **not** a public-release package: frozen evidence and
  toolchain notes still contain machine-local paths. The sanitized tree remains
  the release path.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files.

## Remaining gates

- arXiv endorsement: the 21 January 2026 policy requires **both** an
  institutional email and prior arXiv authorship for automatic endorsement;
  otherwise personal endorsement is needed. `cs.CR` is **not** a separate
  endorsement domain: every `cs.*` category maps to `cs`, whose threshold is
  three papers. Prof. Sudhir Dhage (SPIT, HOD Computer) has four countable
  `cs.*` papers and is the first ask; confirm with the logged-in "Which authors
  of this paper are endorsers?" link before sending.
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
