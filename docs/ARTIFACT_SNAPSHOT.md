# Working artifact snapshot - 28 October 2026

This is a working snapshot, not the release manifest. It records the current
manuscript, figures, builds, and standalone LaTeX export after the 28 October
2026 path-format correction and AI-use disclosure revision to the 26 October
2026 audit-corrected draft. It
does not replace `paper\hashes.txt` (the six Table 15 hashes) or any frozen
source map. The 23 October 2026 canonical PDF and the pre-edit
manuscript/export copies remain archived and unchanged.

## Current artifacts

| Artifact | SHA-256 |
|---|---|
| `paper\MANUSCRIPT_REVISED.md` | `5B85155C8A58185D1EE715A6F38150EFDA121F263E0C826984D0AF0A0CF2EF32` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-26.pdf` | `92A3945281EC5155E2567232F3BA184C33554DD4FB02CCB80F8C793A139540F3` |
| `paper\build\manuscript_build_wide.tex` | `A632B591801FA6E80D203E8D4D7085E2866A4EACF62F8C3CDF2908F08B0A68DA` |
| `paper\build\manuscript_build_wide.pdf` | `92A3945281EC5155E2567232F3BA184C33554DD4FB02CCB80F8C793A139540F3` |
| `paper\latex_export\main.tex` | `A632B591801FA6E80D203E8D4D7085E2866A4EACF62F8C3CDF2908F08B0A68DA` |
| `paper\latex_export\main.pdf` | `1430E2DBFF0A4658C72504731AA28F04B127BA4C6D4F7C04AAC0C59282916EDD` |
| `paper\arxiv_export\main.tex` | `F1E614CE592CDDC058F90FDCCEF4651F42663DD164FD59FC02FD935FBC17F032` |
| `paper\arxiv_export\main.pdf` | `E2939B632D2A5FAB2AC9BEAECC5084D0C556AFADE6BFFC97994532D310083430` |
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

- Canonical 26 October build, refreshed 28 October: 25 pages, letter paper,
  10 pt, 0.75 in margins; 321,999 bytes.
- arXiv candidate, refreshed 28 October: 28 pages, letter paper, 10 pt, 1 in
  margins; 323,588 bytes.
- Canonical build: 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes,
  3 cosmetic underfull hboxes, 6 ignored infinite-glue-shrinkage diagnostics,
  and 1 stable `Label(s) may have changed` warning.
- arXiv build: 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes, and
  4 cosmetic underfull hboxes; 1 stable label warning.
- Zero `LMMono*-Italic` spans remain in all three PDFs; code and paths render
  upright monospace even inside notes.
- Named-author build: the canonical title page and PDF metadata name
  Prathamesh Patil; the arXiv candidate names Prathamesh N Patil. A double-blind
  venue would require re-anonymization.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 12 spans pages 16-17 and cross-references the Section 3.5
  artifact-root key; Appendix Table A1 spans pages 24-25 in the canonical
  build.
- All PDF fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Figure 1: 239.76 x 171.828 pt, vector. Figure 2: 504 x 300.24 pt, vector.
- `pdfimages` reports zero raster images in the manuscript and in both figures.
- Standalone `paper\latex_export\main.tex` compiles independently with
  XeLaTeX, producing a 25-page, 322,001-byte PDF with 0 overfull hboxes.

## References and statuses

- The manuscript contains a static eight-entry reference list after Section 9:
  `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma
  Security, the IETF individual Internet-Draft, and arXiv:2605.05440.
- Abstract: 222 words, SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are part of this package.
- Progent is positioned as a close related work on monotonic confinement inside
  one privilege-control layer, not as an experimental baseline. Its reported
  results are not re-measured or compared here.
- The legacy `tests\seam_pilot_v2\results\claims_update.md` old-H6 Progent
  block is directional-only and is not used as evidence; Appendix Table A1
  records the hypothesis-label lineage.

## 28 October path-format and disclosure revision

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
- The abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.
- The canonical and arXiv builds were regenerated, and the standalone export
  was recompiled. `dist\sanitized` remains untouched.

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
