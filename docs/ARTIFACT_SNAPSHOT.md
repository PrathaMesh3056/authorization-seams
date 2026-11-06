# Working artifact snapshot - 5 November 2026

This is a working snapshot, not the release manifest. It records the current
manuscript, figures, builds, and standalone LaTeX export after the 5 November
2026 declarations and positioning revision. It
does not replace `paper\hashes.txt` (the six Table 15 hashes) or any frozen
source map. The 31 October, 23 October, and 21 October canonical PDFs and the
pre-edit manuscript/export copies remain archived and unchanged.

## Current artifacts

| Artifact | SHA-256 |
|---|---|
| `paper\MANUSCRIPT_REVISED.md` | `E7C3F227F4E79F2CCB0A162DF3411D7633130550C930897395795E91D161B854` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-11-05.pdf` | `7CF87221C4DA167074893FBCCA90EE236577C4BCAAD85DF3BCB50DFE7944815F` |
| `paper\build\manuscript_build_wide.tex` | `6E17B5407C9BEC96F69BF011ED535014024C7BF89A1CAD2688FD7628016AECD8` |
| `paper\build\manuscript_build_wide.pdf` | `7CF87221C4DA167074893FBCCA90EE236577C4BCAAD85DF3BCB50DFE7944815F` |
| `paper\latex_export\main.tex` | `6E17B5407C9BEC96F69BF011ED535014024C7BF89A1CAD2688FD7628016AECD8` |
| `paper\latex_export\main.pdf` | `11FB860DF6398176735174B91F05C7C834F90523D1E77981ED3347F228D455E3` |
| `paper\arxiv_export\main.tex` | `B803242D7A54C6260CE94A0D638384E053B3BF95D17B981198E1612AA42A9AA2` |
| `paper\arxiv_export\main.pdf` | `C67939B0F2F4F9E6F4E2A59953CB45FC838A101FF8AC2811A53E44B0DD09AF28` |
| `paper\figures\figure_1_handoff_anatomy.svg` | `035902B00D700869806BF038F4CE6CBF0B30017BCDB50D3760C4D23F72B9A23C` |
| `paper\figures\figure_1_handoff_anatomy.pdf` | `0AA8A365135AA4E11C5A0D7194FEB3C27947D00FAD8FEA703A1612987C3B90B1` |
| `paper\figures\figure_2_repair_loci.svg` | `B4C641CE07FB789C4E6D74D55E2092A698E256E374C87173D532A138066F3F88` |
| `paper\figures\figure_2_repair_loci.pdf` | `43172412D0AE892C40B18C619EECD03F5A0DA863933E0523E6DFB4195D33867B` |
| `paper\backups\MANUSCRIPT_REVISED_pre_audit_20261026.md` (archived) | `84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66` |
| `paper\backups\latex_export_2026-10-23\main.tex` (archived) | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| `paper\backups\latex_export_2026-10-23\main.pdf` (archived) | `1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.svg` (archived) | `F80E70F44958BED3003CE42E7038685B9A66D368D47B9E9F063329B5C3BEBC4A` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.pdf` (archived) | `5ABCDD261C156CDFFF979B313131411FC811C9CFBF3FF4DE5CC95545A7F2C758` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` (historical) | `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE` |

## Build status

- Canonical 5 November build: 31 pages, letter paper, 10 pt, 0.75 in margins;
  348,663 bytes.
- arXiv candidate: 34 pages, letter paper, 10 pt, 1 in margins; 351,679 bytes.
- Canonical build: 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes,
  3 cosmetic underfull hboxes, 7 ignored infinite-glue-shrinkage diagnostics,
  and 1 stable `Label(s) may have changed` warning.
- arXiv build: 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes, and
  4 cosmetic underfull hboxes; 1 stable label warning.
- Zero `LMMono*-Italic` spans remain in all three PDFs; code and paths render
  upright monospace even inside notes.
- Named-author build: the canonical title page and PDF metadata name
  Prathamesh Patil; the arXiv candidate names Prathamesh N Patil. A double-blind
  venue would require re-anonymization.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 12 cross-references the Section 3.5 artifact-root key; Appendix
  Tables A1 and A2 remain intact in the canonical build.
- All PDF fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Figure 1: 239.76 x 171.828 pt, vector. Figure 2: 504 x 300.24 pt, vector.
- `pdfimages` reports zero raster images in the manuscript and in both figures.
- Standalone `paper\latex_export\main.tex` compiles independently with
  XeLaTeX, producing a 31-page, 348,668-byte PDF with 0 overfull hboxes.

## References and statuses

- The manuscript contains a static eleven-entry reference list after Section 9:
  `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma
  Security, the IETF individual Internet-Draft, arXiv:2605.05440, RFC 8693,
  Zanzibar, and Macaroons.
- Abstract: 222 words, SHA-256
  `35C17A00CBB3A15B5C67298F45E37FE7D663275A65A1CB38DA78BB84FDF89F45`.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are part of this package.
- Progent is positioned as a close related work on monotonic confinement inside
  one privilege-control layer, not as an experimental baseline. Its reported
  results are not re-measured or compared here.
- The legacy `tests\seam_pilot_v2\results\claims_update.md` old-H6 Progent
  block is directional-only and is not used as evidence; Appendix Table A1
  records the hypothesis-label lineage.
- The E1 8/8 `EVIDENCE-VERIFIED` cell remains report-only; the raw
  `extension_e1\metrics.json` does not carry that field.

## 5 November declarations and positioning revision

- Abstract trimmed from 278 to 222 words with no new number, claim, status, or
  citation.
- Added the mandatory Declarations section: data availability, ethics, author
  contributions/CRediT, competing interests, funding, and limitations.
  Author-specific CRediT, competing-interest, and funding confirmations are
  explicitly pending rather than invented.
- Added falsification/stop conditions in Section 3.3 and an explicit H4/H7 gate
  in Section 7.5; no H4 or H7 experiment was designed, locked, or run.
- Added three verified adjacent pointers in Section 6: RFC 8693, Zanzibar, and
  Macaroons. They are definitions/contrast only and not baselines.
- Added Appendix Table A2, restating the effective witness sets behind the
  reported counts without introducing a new measurement.
- Added `report-only` qualifiers to the two Section 5 references to the E1 8/8
  `EVIDENCE-VERIFIED` cell.
- Canonical, standalone, and arXiv builds regenerated: 31, 31, and 34 pages.
- `dist\sanitized` remains untouched.

## 28 October path-format and disclosure revision (historical)

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- Inline code and artifact paths now render upright monospace in all three
  PDFs, including spans inside italic notes. The build header forces `\texttt`
  and `\path` to upright shapes; no `LMMono*-Italic` span remains.
- The artifact-root key is defined once in Section 3.5: `v2` is the
  `tests\seam_pilot_v2\results` root, `dt` is the discriminating-tests results
  root, `sa` is the SentinelAgent results root, and `b` is the boundary results
  root. Table 12 and the Appendix cross-reference that key; full roots remain
  in the artifact tree.
- Long path parentheticals were shortened, and italic note lead-ins were
  converted to bold run-in labels. No claim, number, reference, table datum, or
  H4/H7 status changed.
- At that revision the abstract remained 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- The canonical and arXiv builds were regenerated, and the standalone export
  was recompiled. `dist\sanitized` remains untouched.

## 31 October review-correction pass (historical)

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and ★ are `REFINED`; H1's resource clause is `UNTESTED`; H4 and H7
  remain `UNTESTED`.
- Abstract: 278 words, SHA-256
  `060C2D9F7A78D8E346DC4B8A3BA8278BFD5A34883E6B33CED33CAC90A0D57CD7`.
- Canonical, standalone, and arXiv builds regenerated: 29, 29, and 32 pages.

## 26 October correction-pass notes

- H3 is narrowed to state/identity vocabulary gaps. Caught recipient/default
  cases, the E1 action-family consumption failure, and the V1/V2 derivation
  widening are reported under H1/H6 and the measured findings, not H3.
- Section 1, Section 4.5, and Section 9 disclose that two of the three
  pair-level zeroes are construction-forced and that E1 is the only genuine
  composition-specific test.
- The 638 non-vacuity count is stated against the 7-arm, 96-case matrix
  (756 evaluated events): 488 admissions plus 150 token-attached denials, with
  the no-token admitted and denied events identified separately.
- Figure 2's Locus B connector points to the bridge-translation step; Locus A
  points to the carried-record/read-set gap. The caption and SVG description
  match the drawing.
- `dist\sanitized` remains the stale 21 October 298-file tree and was not
  regenerated or edited. The review package is not a public-release package.

## Notes

- The frozen predecessor `MANUSCRIPT.md` and claim authority
  `CONSOLIDATED_CLAIMS.md` remain in the project archive, not this repository;
  they were not edited. `paper\hashes.txt`, locks, traces, and frozen artifacts
  remain untouched.
- The archived `CONSOLIDATED_CLAIMS.md` is frozen but contains superseded
  Progent/APC/SentinelAgent characterizations. It is not the current wording
  authority; the correction records are in `docs\`.
- The pre-edit source and export copies are under `paper\backups\`; the old
  Figure 2 SVG/PDF are under `paper\figures\superseded\`.
- The 23 October canonical PDF remains at
  `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` and is not overwritten.
