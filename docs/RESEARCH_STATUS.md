# Research status - 28 October 2026

## Current position

The manuscript source is `paper\MANUSCRIPT_REVISED.md` (SHA-256
`5B85155C8A58185D1EE715A6F38150EFDA121F263E0C826984D0AF0A0CF2EF32`;
590 lines, 115,399 bytes). The reference list has eight entries: the seven
frozen identities checked on 20 October 2026 plus MasDrift, added 22 October
2026 after arXiv identity verification. The abstract remains 222 words and
byte-identical to the frozen version
(`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).

The canonical build is the 25-page single-column named-author preprint
`paper\drafts\MANUSCRIPT_DRAFT_2026-10-26.pdf` (SHA-256
`92A3945281EC5155E2567232F3BA184C33554DD4FB02CCB80F8C793A139540F3`):
25 pages, 321,999 bytes, 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull
hboxes, 3 cosmetic underfull hboxes, 6 ignored infinite-glue-shrinkage
diagnostics, and 1 stable `Label(s) may have changed` warning. The title page
and PDF metadata name Prathamesh Patil; this is the authorized named-author
build, not a double-blind submission. The 23 October 24-page PDF remains
archived and unchanged.

The standalone export is refreshed to the same source:
`paper\latex_export\main.tex` (SHA-256
`A632B591801FA6E80D203E8D4D7085E2866A4EACF62F8C3CDF2908F08B0A68DA`) and
reference PDF `paper\latex_export\main.pdf` (SHA-256
`1430E2DBFF0A4658C72504731AA28F04B127BA4C6D4F7C04AAC0C59282916EDD`), 25
pages, 322,001 bytes, 0 fatal errors, 0 overfull, 3 underfull, and 6 ignored
glue diagnostics. Both figures are vector PDFs and are included.

The separate arXiv-compliant named-author candidate is
`paper\arxiv_export\main.pdf` (SHA-256
`E2939B632D2A5FAB2AC9BEAECC5084D0C556AFADE6BFFC97994532D310083430`):
28 pages, 323,588 bytes, US Letter, 10 pt, 1-inch margins, 0 missing glyphs,
0 fatal LaTeX errors, 0 overfull hboxes, 4 cosmetic underfull hboxes, and 1
stable label warning. Its source SHA-256 is
`F1E614CE592CDDC058F90FDCCEF4651F42663DD164FD59FC02FD935FBC17F032`.

## 26 October correction pass

The audit-driven correction pass changed no claims, experiments, references, or
H4/H7 status. It applied these corrections:

- H3 is narrowed to state/identity vocabulary gaps. Caught recipient/default
  cases, the E1 action-family consumption failure, and the V1/V2 derivation
  widening are reported under H1/H6 and the measured findings, not H3.
- Section 1, Section 4.5, and Section 9 disclose that two of the three
  pair-level zeroes are construction-forced and that E1 is the only genuine
  composition-specific test.
- The zero-seam construction-forced disclosure is stated where the finding is
  reported; the bounded zero is not presented as a theorem.
- Progent is positioned as close related work on monotonic confinement inside
  one privilege-control layer, not as an experimental baseline. The legacy
  `tests\seam_pilot_v2\results\claims_update.md` old-H6 Progent block is
  directional-only and is not used as evidence.
- Appendix A and Table A1 record the hypothesis-label lineage, including the
  old-H4/H6 labels used by the frozen artifacts.
- The 638 non-vacuity wording is stated against the full 7-arm, 96-case matrix
  (756 evaluated events): 488 admissions plus 150 token-attached denials
  (638 counted events; 40 native P6/P7 denials, 42 attestation-stage denials in
  arm 6, 68 pre-presentation refusals in arm 7). The 230 admitted events without
  a token key are inside the 488; the 118 denials without a token key are
  outside the 638.
- Table 12 uses display-only artifact-root abbreviations; full paths remain in
  the artifact tree. Table 2's caption/body and Table 3's Total row stay with
  their tables.
- Figure 2's Locus B connector points to the bridge-translation step; Locus A
  points to the carried-record/read-set gap. The caption and SVG description
  match the drawing.

The pre-edit manuscript, export, and Figure 2 copies are archived under
`paper\backups\` and `paper\figures\superseded\`.

## 28 October path-format and disclosure revision

The revision changed no claims, experiments, references, table data, or H4/H7
status. It applied these presentation and disclosure fixes:

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- Inline code and artifact paths now render upright monospace, including spans
  inside notes. The build header forces upright `\texttt` and `\path` shapes;
  all three PDFs contain zero `LMMono*-Italic` spans.
- The artifact-root key is defined once in Section 3.5: `v2` is the
  `tests\seam_pilot_v2\results` root, `dt` is the discriminating-tests results
  root, `sa` is the SentinelAgent results root, and `b` is the boundary results
  root. Table 12 and the Appendix cross-reference that key.
- Long path parentheticals were shortened, and italic note lead-ins became bold
  run-in labels. The Section 3.5 key is a bullet list so long roots start at
  the left margin and do not break mid-segment.
- The canonical PDF, standalone export, and arXiv candidate were regenerated.
  The abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`;
  the reference list remains eight entries.

## Completed

- Run 6 QA, section assembly, cross-checks, reconciliation, targeted model
  pass, and independent fixer/verifier.
- 21 Oct 2026 recheck reconciliation applied: H5 signature-family sample size
  corrected to 16 cases (2 pairs x 4 document parameters x 2 variants; 8 attack
  + 8 benign), Task D path prefix, and arm-5 confusion-matrix scoping; the
  abstract was re-verified byte-identical.
- 22 Oct 2026 MasDrift added as the eighth reference after arXiv identity
  verification (arXiv:2608.07556v3, revised 15 October 2026; DOI
  10.48550/arXiv.2608.07556). The addition is confined to Section 6 and the
  reference list; it states a scale/design distinction, introduces no
  comparison, changes no claim or experiment, and leaves H4/H7 `UNTESTED`.
- 23 Oct 2026 finalization applied the F1-F13 correction pass: exporter `\path`
  to `\texttt`, terminology cleanup, `ATT-OK` alias, H1-H7 status key, the 638
  non-vacuity count, the named author block, reset-control note, T1 fractions,
  six-control ledger note, SentinelAgent P1/P3-P7 TLA+ qualifier, and
  Noma/IETF softening. F14 is resolved in this build; F15 remains an optional
  editorial note.
- 23 Oct 2026 F4/F5 correction: the handoff-norm sentence now says "kept the 4
  leaks", and the Table 12 H6 row is scoped to the measured pairs with the
  disclosed E1 action-family exception. The canonical PDF, export, and zip were
  rebuilt; the pre-F4F5 build is archived.
- 23 Oct 2026 638 correction: the denominator wording now states the full
  96-case matrix scope and the non-vacuity count. The canonical PDF, export,
  and zip were rebuilt; the pre-638 build is archived.
- 26 Oct 2026 audit correction pass applied as listed above; canonical,
  standalone export, and arXiv candidate rebuilt and rechecked.
- 28 Oct 2026 path-format and AI-disclosure revision applied: upright inline
  code/paths, Section 3.5 artifact-root key, shortened path parentheticals,
  bold note labels, and an experiment/artifact-scoped Section 3.7 disclosure;
  canonical, export, and arXiv candidate rebuilt and rechecked.
- Six Table 15 hashes verified; `paper\hashes.txt` remains untouched.
- Table 15 truncation gate closed (22 Oct 2026): all six printed fragments are
  exact substrings of the full 64-character values, including the 7-character
  row-3 suffix (`65d47f0`) and the 9-character row-6 suffix (`790814af4`); the
  variable-length truncation is disclosed by the Table 15 suffix note. No hash
  correction is required or applied.
- Figure 1 v2 promoted to canonical; Figure 1 v1 archived.
- Both figures converted to vector PDF; Figure 1 at 239.76 x 171.828 pt and
  Figure 2 at 504 x 300.24 pt; zero raster images.
- All 109 source section-sign glyphs replaced by 71 `Section`/`Sections`
  expressions.
- Body star has a one-sentence definition at first use.
- Body font fallback removed: no Segoe UI Symbol. Figures use Arial plus
  Cambria Math for the subset glyph; no Lucida Sans Unicode.
- Progent replacement applied and the false 4/20 attribution removed. Progent
  is a close related work, not a baseline; no Progent number is reproduced,
  re-measured, or compared.
- Reference list: the seven entries' bibliographic identities were checked on
  20 October 2026; MasDrift was added as the eighth entry on 22 October 2026
  after arXiv verification. Claims remain unverified and none is treated as a
  verified input.
- APC correction: Agentic Principal Chain expanded; Theorem 4.7 (Composition
  Soundness) cited; C1-C6, the complete restriction set, serialized admission,
  static X, and intra-session scope stated.
- SentinelAgent correction: Theorem 4 is Composition Safety with Write-Impact
  Notification, stated for two chains satisfying P1-P7 within its framework;
  the false "same mechanism" condition was removed.
- Composition senses clarified: APC composition is intra-session
  action-sequence composition, not cross-mechanism composition.
- Seam predicate now includes arms 5, 6, and 7; E1 arm-5 form is identified.
- Mapping taxonomy M0, M2, M2-auth, M0-A, T0, V1, and V2 added.
- Implementation provenance added for the pinned APC commit, SentinelAgent
  prototype, TraceGrant Task D implementation, and bridge mappings.
- SentinelAgent reconciliation flags disclosed: `expected_vs_observed_ok=false`
  and `comparison.overall_ok=false`, with `sa\sa\reconciliation.json` cited.
- Pilot-1 zero-seam pointer corrected to
  `tests\seam_pilot_v2\RESULTS_FOR_COAUTHOR.md` Section 1, derived from the
  arm2 = arm5 identity. All three forced identities are stated.
- Table 6 uses case IDs and arm numbers; Table 8 uses compact metric headers;
  Table 9 uses compact code cells and a control list. Table 4 still line-breaks
  some identifiers at underscores; the full identifiers are recoverable from
  the text layer, and this is recorded as a minor readability residual (F1).

## Historical artifacts (unchanged)

| Artifact | SHA-256 |
|---|---|
| `paper\backups\MANUSCRIPT_REVISED_pre_audit_20261026.md` | `84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` | `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_638fix.pdf` | `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_F4F5.pdf` | `5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B` |
| `paper\backups\MANUSCRIPT_REVISED_pre_638fix_20261023.md` | `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510` |
| `paper\backups\latex_export_2026-10-23\main.tex` | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| `paper\backups\latex_export_2026-10-23\main.pdf` | `1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF` |
| `paper\drafts\seam_manuscript_latex_2026-10-23.zip` | `9252C9953074AD8301E67FF63EC62E014E2B18AC7EF0A0FF39D42759EC3E5E35` |
| `paper\drafts\seam_manuscript_latex_2026-10-23_pre_638fix.zip` | `9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3` |
| `paper\drafts\seam_manuscript_latex_2026-10-23_pre_F4F5.zip` | `3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0` |
| `paper\drafts\seam_manuscript_latex_2026-10-21.zip` | `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.svg` | `F80E70F44958BED3003CE42E7038685B9A66D368D47B9E9F063329B5C3BEBC4A` |
| `paper\figures\superseded\figure_2_repair_loci_pre_audit_20261026.pdf` | `5ABCDD261C156CDFFF979B313131411FC811C9CFBF3FF4DE5CC95545A7F2C758` |

## Release decisions

1. **Author block and public contact.** The named-author block is printed
   (Prathamesh Patil; Department of Computer Engineering, Sardar Patel
   Institute of Technology), and the PDF metadata carries the same author. The
   final public contact address is still needed; the internal placeholder must
   not appear on the PDF (it does not). A double-blind venue would require
   re-anonymizing this build.
2. **Venue metadata.** Venue, page limit, anonymity rule, reference style,
   license, repository URL, archival DOI, and release sanitization are pending.
3. **Release package.** The repository manifest is regenerated and verified;
   `dist\sanitized` remains intentionally untouched. Public-release
   sanitization, license, repository URL, and DOI are pending.
4. **Merge/submission.** The manuscript remains separate from the frozen
   predecessor; no peer-reviewed submission has occurred.
5. **Frozen authority.** The archived `CONSOLIDATED_CLAIMS.md` remains frozen
   and contains superseded Progent/APC/SentinelAgent characterizations. It must
   not be used as the current wording authority until separately reconciled.
6. **Deferred expansions.** Classic-literature expansion, the 40-50 percent
   length cut, and any new data figure need explicit approval and new
   verification. The MasDrift citation was authorized and added on 22 October
   2026 after arXiv verification; further new references still require explicit
   approval and verification.

## Frozen constraints

- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are authorized.
- Do not alter the archived `CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`,
  locks, traces, pre-revision files, or frozen artifacts.
- Figure 1 v1 must never be embedded; Figure 1 v2 is canonical.
- Figure 2 must remain vector and 7.0 in wide in the canonical build; the
  dashed stub must enter the X without crossing into `V_read`. In the arXiv
  build it is fitted to the 6.5-inch text measure with `\linewidth`, preserving
  aspect ratio and content.
- The paper target is a workshop/short paper, tool track, or arXiv preprint,
  not main-track.
- Public release is gated on the pending metadata and release checks above.

## Next actions

1. Choose the final public contact address, venue/CFP, license, repository URL,
   and archival DOI.
2. If a double-blind venue is chosen, re-anonymize the named-author build before
   submission; do not send the named-author PDF to a double-blind track.
3. Add venue metadata only after a specific CFP is chosen.
4. The 28 October path-format and disclosure rebuild, export refresh, arXiv
   candidate, and repository refresh are complete. Leave `dist\sanitized` untouched;
   publication is a separate owner decision.
5. Do not submit to a public venue until the relevant release checks close.
