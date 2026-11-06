# Working artifact snapshot - 6 November 2026

This is a working snapshot, not the release manifest. It records the current
manuscript, figures, builds, and standalone LaTeX export after the 6 November
2026 positioning and related-work revision. It
does not replace `paper\hashes.txt` (the six Table 15 hashes) or any frozen
source map. The 5 November, 31 October, 23 October, and 21 October canonical PDFs
and the pre-edit manuscript/export copies remain archived and unchanged.

## Current artifacts

| Artifact | SHA-256 |
|---|---|
| `paper\MANUSCRIPT_REVISED.md` | `76E9E8F6F7233121277B97C0363DF38AC05284F71CD52D26E33D6A8E098B1A98` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-11-06.pdf` | `08752FEED7AA766DA8D4ABDF7FCBDD7907F35A6C53D2E235D57C0A8B6B51C256` |
| `paper\build\manuscript_build_wide.tex` | `C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139` |
| `paper\build\manuscript_build_wide.pdf` | `08752FEED7AA766DA8D4ABDF7FCBDD7907F35A6C53D2E235D57C0A8B6B51C256` |
| `paper\latex_export\main.tex` | `C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139` |
| `paper\latex_export\main.pdf` | `F13D7EA29D4136101CFA44D07F31A1F4C56B09F05AC48CE0E7122AC06FCDB7BC` |
| `paper\arxiv_export\main.tex` | `2E0C4C858E3CD941D0FEDE1E0FB78CF6C607547BFA49738DB2886C151D298D25` |
| `paper\arxiv_export\main.pdf` | `84DADE9A8B83EB5C8D0DCEED975A15984B63DC0CCBB7BC07E471067D18DEDAF0` |
| `paper\figures\figure_1_handoff_anatomy.svg` | `035902B00D700869806BF038F4CE6CBF0B30017BCDB50D3760C4D23F72B9A23C` |
| `paper\figures\figure_1_handoff_anatomy.pdf` | `0AA8A365135AA4E11C5A0D7194FEB3C27947D00FAD8FEA703A1612987C3B90B1` |
| `paper\figures\figure_2_repair_loci.svg` | `B4C641CE07FB789C4E6D74D55E2092A698E256E374C87173D532A138066F3F88` |
| `paper\figures\figure_2_repair_loci.pdf` | `43172412D0AE892C40B18C619EECD03F5A0DA863933E0523E6DFB4195D33867B` |
| `paper\backups\MANUSCRIPT_REVISED_pre_positioning_20261106.md` (archived) | `E7C3F227F4E79F2CCB0A162DF3411D7633130550C930897395795E91D161B854` |
| `paper\backups\MANUSCRIPT_REVISED_pre_audit_20261026.md` (archived) | `84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66` |
| `paper\backups\latex_export_2026-10-23\main.tex` (archived) | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| `paper\backups\latex_export_2026-10-23\main.pdf` (archived) | `1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.svg` (archived) | `F80E70F44958BED3003CE42E7038685B9A66D368D47B9E9F063329B5C3BEBC4A` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.pdf` (archived) | `5ABCDD261C156CDFFF979B313131411FC811C9CFBF3FF4DE5CC95545A7F2C758` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-11-05.pdf` (historical) | `7CF87221C4DA167074893FBCCA90EE236577C4BCAAD85DF3BCB50DFE7944815F` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` (historical) | `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE` |

## Build status

- Canonical 6 November build: 32 pages, letter paper, 10 pt, 0.75 in margins;
  355,310 bytes.
- arXiv candidate: 35 pages, letter paper, 10 pt, 1 in margins; 358,240 bytes.
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
  ledger; Table 12 cross-references the Section 3.5 artifact-root key; Appendix
  Tables A1 and A2 remain intact in the canonical build.
- All PDF fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Figure 1: 239.76 x 171.828 pt, vector. Figure 2: 504 x 300.24 pt, vector.
- `pdfimages` reports zero raster images in the manuscript and in both figures.
- Standalone `paper\latex_export\main.tex` compiles independently with
  XeLaTeX, producing a 32-page, 355,310-byte PDF with 0 overfull hboxes.

## References and statuses

- The manuscript contains a static twenty-one-entry reference list after
  Section 9: `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`,
  `[MasDrift]`, Noma Security, the IETF individual Internet-Draft,
  arXiv:2605.05440, RFC 8693, Zanzibar, Macaroons, RFC 9396, RFC 2693, Miller,
  Blaze et al., Appel and Felten, Fong, Parisel, ChainCaps, Overlaying
  Governance, and Local Allow, Global Deny.
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

## 6 November positioning and related-work revision

- Section 6 was restructured into (i) upstream formal spines, (ii) standards and
  credential vocabularies, (iii) systems and foundations, (iv) recent 2026
  agent-delegation work, (v) industry pointers, (vi) Progent, and (vii)
  MasDrift. The duplicated restatement of the three upstream guarantees was
  removed.
- Ten verified references were added: RFC 9396, RFC 2693, Miller's *Robust
  Composition*, Blaze et al., Appel and Felten, Fong, Parisel's least-autonomy
  theory, ChainCaps, Overlaying Governance, and Local Allow, Global Deny.
  Identities were checked against the RFC Editor, the JHU scholarship record,
  Crossref, and arXiv on 6 November 2026.
- The Introduction's scope paragraph now matches the expanded positioning.
  The defensive "deliberately bounded / not a survey" wording in Section 6 was
  replaced with a positive statement of the positioning sample.
- Section 7.3 gained a design-space rationale explaining the one-sender,
  two-receiver design, why the receivers were selected, and what does and does
  not generalize.
- No experiment, frozen artifact, count, sum, effective sample size, hypothesis
  status, abstract word, or measured claim changed. H4 and H7 remain `UNTESTED`.
- Canonical, standalone, and arXiv builds regenerated: 32, 32, and 35 pages.
- `dist\sanitized` remains untouched.

## 5 November declarations and positioning revision (historical)

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
