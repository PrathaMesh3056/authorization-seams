# arXiv build QA - 7 November 2026

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

The canonical 7 November PDF is a 33-page, single-column, named-author build
with **0.75-inch margins**. arXiv requires a **minimum 1-inch page margin** and
10-14 pt type. Uploading the canonical PDF as-is would risk a format
correction. The canonical PDF and standalone LaTeX export were refreshed for
the 7 November external-review reconciliation, but the arXiv layout remains a
separate candidate generated from that export. The 6 November 35-page,
5 November 31-page, and 31 October 29-page PDFs remain archived.

The same review also confirmed that arXiv is named-author (no anonymity), while
CODASPY 2027 requires a 12-page double-column anonymized research submission
(abstract 16 November 2026; paper 23 November 2026). The current 33-page
single-column paper is not a CODASPY-ready submission.

## Inputs and build

| Item | Value |
|---|---|
| Current manuscript | `paper/MANUSCRIPT_REVISED.md` |
| Manuscript SHA-256 | `117A229932806A7E4D6205581A7E90FC276C838867BEEBFF7F972E561ABF7722` |
| Current LaTeX source | `paper/latex_export/main.tex` |
| LaTeX source SHA-256 | `FC2618112D3CE711FEE9B327665527E66664DFE9FF1D8A21AE96BAD327008F32` |
| Build script | `paper/build/build_arxiv.py` |
| Output source | `paper/arxiv_export/main.tex` |
| Output PDF | `paper/arxiv_export/main.pdf` |
| Toolchain | Pandoc 3.12.1 (source export) + XeLaTeX 4.16 / MiKTeX 25.12 |

The build script verifies the pinned source hash and the unified author name
before writing anything. It applies only the following changes:

1. `margin=0.75in` to `margin=1in`;
2. Figure 2 from a fixed 7-inch width to `\linewidth`, so it fits the 1-inch
   text measure.

A line-level diff against the current source export shows exactly those two
changed content lines plus the generated-file header. No sentence, number,
table, reference, figure, or hypothesis status changed. The author display
name and PDF metadata are already `Prathamesh N Patil` in the pinned source;
the script verifies that form and rejects the older `Prathamesh Patil`
variant.

## Output checks

| Check | Result |
|---|---|
| Pages | 37 |
| Page size | 612 x 792 pt (US Letter) |
| Body type | 10 pt |
| Margins | 1-inch geometry; text line boxes at 72 pt |
| PDF SHA-256 | `3FB05353E40CE4E504D384A68B8F8FE524F3546D4B32C498C12D03736FBE8F3A` |
| PDF size | 363,591 bytes |
| Source SHA-256 | `299EB14C9730AF5D22E44AB2E743E690649EDA659BA71B254E0EEE7F86BBBE9C` |
| Source size | 181,289 bytes |
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

The page count increased from 36 to 37 because the external-review
reconciliation added the E1 identical-decision and post-data-lock disclosure,
the Pilot 1 8/40 reconciliation note, the corrected H1 resource-clause wording,
the Table 12 denominator note, and the `hashes.txt` renumbering note. That is
deliberate content and layout change, not a regression. The prior 7 November
style revision had grown from 35 to 36 pages when it completed the Declarations
and acknowledgments text and bracketed all 21 reference keys. The 6 November
build had grown from 34 to 35 pages because that revision expanded Section 6
with ten verified references and added a design-space paragraph in Section 7.3.
The 5 November build had grown from 32 to 34 pages for the Declarations
section, falsification/stop conditions, adjacent-work paragraph, and Appendix
Table A2.

Some text bounding boxes report an x-coordinate a few points below 72 pt
because of glyph side bearings (for example, italic or table glyphs). The
geometry package still sets the line boxes at the 1-inch margin; no line or
table overflows the page.

## Content-preservation checks

- Abstract: 222 words; SHA-256
  `B93412AC45C73A9692F33E6B765959C581231BF93DE65F0D6C2BC8CBC460AF38`.
- Static reference list: 21 entries, all with bracketed keys.
- H4 and H7: `UNTESTED` in the source and the PDF.
- Progent: related work only; no reproduced figure or comparison.
- The 6 November 35-page, 5 November 31-page, and 31 October 29-page PDFs
  remain archived.
- Both arXiv figures are byte-identical copies of the canonical vector PDFs.
- No internal placeholder email, local Windows path, or token-shaped secret
  appears in the generated source or PDF text.
- No line numbers or watermark.
- No printed line ends with a trailing underscore.

## 7 November external-review reconciliation

An external review of public HEAD `b3c0c15` scored the package arXiv 5.0,
workshop 4.0, main track 2.0, and future full paper 6.0 on its 10-point rubric;
the scores describe the reviewed HEAD, not this tree, and no re-review has
occurred. The review confirmed the artifact discipline and hash reproduction
but rejected the composition-specific claim as written. The build reflects
these fixes:

- E1 arms 2 and 5 decide identically on all eight cases; the arm-native norm
  was locked at `2026-10-19T12:52:51Z` after the E1 run began at
  `2026-10-19T07:12:26Z`. E1 is now candidate/scoring-dependent, not evidence
  that composition adds an admission.
- Pilot 1 reports 8/40 falsified arm-5 attack predictions and 32/40 matched,
  naming the four `resource_widen` and four `unsatisfiable_verify` cases.
- H1's resource clause is "not supported" per the frozen authority (C1a
  falsified on 4/4 cases), not `UNTESTED`.
- Table 12's boundary denominator is 32/48 attack cases (28 + 4), not 32/96.
- The Section 3.7/3.8 cross-reference, `hashes.txt` "Table 15" note, Table 17
  report-only label, and lock-before-run wording are corrected.

The repository/license/data-availability contradiction remains an owner
decision, and no URL, license, DOI, or public email was invented. H4/H7 remain
`UNTESTED`. The canonical, standalone, and arXiv builds are 33, 33, and 37
pages; the package is 171,996 bytes with SHA-256
`F6BD655B5C3F3CBA7F48EE2F09CCD786D874A6C1886311AACCB22B18AA41DCCF`.

## 7 November writing-style and audit revision (historical, pre-review)

- All 21 references now use bracketed keys; the hybrid name-only style is
  superseded. No reference was added or removed.
- The Pandey entry reports acceptance at IEEE TPS 2026, explicitly marked as
  "acceptance reported, not independently verified here"; the unregistered DOI
  was dropped.
- Declarations completed: no external funding, no competing interests, full
  single-author CRediT roles, author-retained data availability, and an
  acknowledgments note.
- Author unified to `Prathamesh N Patil` in the source, canonical build, arXiv
  build, and `CITATION.cff`.
- Table 5 headers are `SA`/`M0`/`Retained` with an explicit column key. The
  body voice is impersonal; the abstract's closing "We" was left unchanged to
  preserve the 222-word abstract.
- No measured claim, count, sum, effective sample size, status, or frozen
  artifact changed in that revision. H4 and H7 remain `UNTESTED`.
- The generated source and PDF described in this section were the pre-review
  build; the external-review reconciliation above superseded them.

## 6 November positioning and related-work revision (historical)

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
pages. The pre-review 7 November build was checked on all 36 pages. The current
7 November build was checked the same way on all 37 pages, including the Table
5 header/key, the Table 12 reconciliation notes, and the Table 13 column
rebalance; no text block falls outside its page.

## Packaging checks

- **Current source package:** `dist/arxiv/authorization-seams-arxiv-2026-11-07.zip`,
  171,996 bytes, SHA-256
  `F6BD655B5C3F3CBA7F48EE2F09CCD786D874A6C1886311AACCB22B18AA41DCCF`.
  It contains only `main.tex` (181,289 bytes; pinned SHA-256
  `299EB14C9730AF5D22E44AB2E743E690649EDA659BA71B254E0EEE7F86BBBE9C`) and
  the two byte-identical vector figures under `figures/`. The archive contains
  those three entries in fixed order and no build artifacts.
- **Clean-room test (7 November 2026):** the zip was extracted into an empty
  temporary directory and compiled three times with XeLaTeX 4.16
  (MiKTeX 25.12), using `-interaction=nonstopmode -halt-on-error`. All three
  runs exited 0. The resulting PDF is 37 pages, US Letter (612 x 792 pt),
  10 pt, with 0 fatal errors, 0 overfull hboxes, 4 cosmetic underfull hboxes,
  0 missing characters, and embedded subset fonts. Page 1 carries the title,
  `Prathamesh N Patil`, the SPIT affiliation, and the 222-word abstract;
  `UNTESTED` still appears for H4/H7; extracted text contains no public email,
  repository URL, or local Windows path.
- The clean-room PDF is a test artifact and is not committed. arXiv receives
  source only. `paper/arxiv_export/main.pdf` remains the XeLaTeX reference
  build (`3FB05353E40CE4E504D384A68B8F8FE524F3546D4B32C498C12D03736FBE8F3A`).
- **Historical:** `dist/arxiv/authorization-seams-arxiv-2026-11-06.zip`
  (169,835 bytes; SHA-256
  `DED4065954CFE8538D58057D8948F66A65BBCA978C738801320514733C083483`)
  was the last package before the 7 November revision. It extracted cleanly to
  35 pages.
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
- Repository visibility, license, and data-availability reconciliation: a
  public repository is reachable at the reviewed HEAD while the release
  documents described a private repository, and `LICENSE` grants no
  redistribution rights. This is an owner decision; do not assert a URL,
  license, or public release until it is recorded.
- CODASPY 2027, if pursued: separate 12-page double-column anonymized build,
  abstract by 16 November 2026, paper by 23 November 2026.
- Any double-blind venue requires a separate anonymized PDF and metadata.
- A workshop/short/tool-track cut must be rebuilt from the current source; the
  old 13-page CODASPY cut predates the 7 November revision.

## Gate reminder

This build does **not** close the release checklist. Repository visibility and
license remain unresolved, and no public email, license, repository URL,
archival DOI, or arXiv submission has been created. H4 and H7 remain
`UNTESTED`.
