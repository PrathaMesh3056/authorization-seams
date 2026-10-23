# Research status - 23 Oct 2026

## Current position

The manuscript source is `paper\MANUSCRIPT_REVISED.md` (SHA-256
`84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66`; 557
lines, 111,335 bytes). The reference list has eight entries: the seven frozen
identities checked on 20 October 2026 plus MasDrift, added 22 October 2026
after arXiv identity verification. The abstract remains 222 words and
byte-identical to the frozen version
(`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).

The canonical build is the 24-page single-column named-author preprint
`paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` (SHA-256
`D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE`): 24
pages, 321,409 bytes, 0 missing glyphs, 0 LaTeX errors, 0 overfull hboxes. The
title page and PDF metadata name Prathamesh Patil; this is the authorized
named-author build, not a double-blind submission. Three cosmetic underfull
hboxes and one stable `Label(s) may have changed` warning remain; they are not
blockers. The Table 15 caption and table body both appear on page 23, so the
caption orphan reported against the older 21 October snapshot does not persist.
The four expected divergences listed in the older preflight report (the 16-case
H5 signature-family structure, the `tests\` path prefix, the eight-case family
wording, and the eighth reference) are resolved in this build. F2, F3, F6, F9,
F13, and F14 are resolved. F4 and F5 are corrected here (the handoff-norm
sentence says "kept the 4 leaks", and the Table 12 H6 row is scoped to the
measured pairs with the disclosed E1 action-family exception). The 638
non-vacuity count is corrected to the full 96-case matrix scope. F1 remains a
minor identifier line-break residual in Table 4: the full identifiers are
recoverable, but the PDF breaks some of them at underscores. The remaining
review items (F7, F8, F10-F12, and the listed NITs) are minor or cosmetic and
are not blockers; F15 is an optional editorial note, and the model disclosure is
present.

The standalone export is refreshed to the same source:
`paper\latex_export\main.tex` (SHA-256
`107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A`) and
reference PDF `paper\latex_export\main.pdf` (SHA-256
`1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF`), 24
pages, 0 errors, 0 overfull. Both figures are vector PDFs and are included. The
pre-638 23 October build remains archived at
`paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_638fix.pdf` (SHA-256
`086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC`), with
its export zip at
`paper\drafts\seam_manuscript_latex_2026-10-23_pre_638fix.zip` (SHA-256
`9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3`) and its
source at `paper\backups\MANUSCRIPT_REVISED_pre_638fix_20261023.md` (SHA-256
`1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510`). The
pre-F4F5 23 October build remains archived at
`paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_F4F5.pdf` (SHA-256
`5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B`), with
its export zip at
`paper\drafts\seam_manuscript_latex_2026-10-23_pre_F4F5.zip` (SHA-256
`3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0`).

The repository was refreshed on 23 October 2026 with the corrected source,
canonical PDF, export, state docs, and regenerated manifest. The pre-638
23 October build, the pre-F4F5 23 October build, and the old 21 October
PDF/export/revision remain archived.

The authorized factual/traceability correction pass is applied, including the
23 October named-author finalization (F1-F13), the F4/F5 wording corrections,
and the 638 non-vacuity wording correction. It changed no claims, experiments,
references, or H4/H7 status. The corrections
and their provenance are recorded in
`paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md` and
`paper\agent_reports\FINAL_BUILD_QA.md`.

The 21 October recheck reconciliation applied three further in-line corrections
with the same scope: the H5 signature-family sample size, the Task D path
prefix, and the arm-5 confusion-matrix scoping. It is recorded in
`paper\agent_reports\RECHECK_RECONCILIATION_2026-10-21.md`.

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
  96-case matrix scope and the non-vacuity count (488 admissions plus 150
  token-attached denials; 638 counted events; 40 native P6/P7, 42
  attestation-stage, and 68 pre-presentation denials). The canonical PDF,
  export, and zip were rebuilt; the pre-638 build is archived.
- Six Table 15 hashes verified; `paper\hashes.txt` remains untouched.
- Table 15 truncation gate closed (22 Oct 2026): all six printed fragments are
  exact substrings of the full 64-character values, including the 7-character
  row-3 suffix (`65d47f0`) and the 9-character row-6 suffix (`790814af4`); the
  variable-length truncation is disclosed by the Table 15 suffix note at
  `MANUSCRIPT_REVISED.md` line 521. No hash correction is required or applied.
  This closes the item recorded as approval-pending in
  `paper\manuscript_crosscheck_reconciliation.md` (proposed 8-character rewrite,
  not applied) and as the sole unresolved blocker in
  `paper\MANUSCRIPT_FIX_REPORT.md`; both are historical records and are not
  edited.
- 22 Oct 2026 external content check of the reviewed-round standalone
  `latex_export\main.tex`: the execution ledger, status tokens, Table 15
  fragments, arm-7 26/28 non-additivity, and spot-checked frozen numbers were
  reported consistent; no content correction was required. Exhaustive
  table-cell verification remains the 21 Oct recheck (all 15 tables match raw
  metrics cell-for-cell); the 22 Oct pass spot-checked Tables 4, 8, and 12 only.
- Figure 1 v2 promoted to canonical; Figure 1 v1 archived.
- Both figures converted to vector PDF; Figure 1 at 239.76 x 171.828 pt and
  Figure 2 at 504 x 300.24 pt; zero raster images.
- Figure includes applied to the manuscript.
- All 109 source section-sign glyphs replaced by 71 `Section`/`Sections`
  expressions.
- Abstract remains 222 words and byte-identical to the frozen version
  (`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).
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
  Soundness) cited; C1-C6, the complete restriction set, serialized
  admission, static X, and intra-session scope stated.
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
  and `comparison.overall_ok=false`, with `sa\reconciliation.json` cited.
- Pilot-1 zero-seam pointer corrected to
  `tests\seam_pilot_v2\RESULTS_FOR_COAUTHOR.md` Section 1, derived from the
  arm2 = arm5 identity. All three forced identities are stated.
- Table 6 uses case IDs and arm numbers; Table 8 uses compact metric headers;
  Table 9 uses compact code cells and a control list. Table 4 still line-breaks
  some identifiers at underscores; the full identifiers are recoverable from
  the text layer, and this is recorded as a minor readability residual (F1).
- Zero-seam caveat and scope-of-positioning paragraph added.
- Canonical PDF (23 Oct named-author build):
  `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf`, SHA-256
  `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE`;
  24 pages, 321,409 bytes.
- Archived pre-638 23 Oct PDF:
  `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_638fix.pdf`, SHA-256
  `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC`;
  source at `paper\backups\MANUSCRIPT_REVISED_pre_638fix_20261023.md`, SHA-256
  `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510`.
- Archived pre-F4F5 23 Oct PDF:
  `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_F4F5.pdf`, SHA-256
  `5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B`.
- Standalone source (23 Oct export):
  `paper\latex_export\main.tex`, SHA-256
  `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A`;
  reference PDF `paper\latex_export\main.pdf`, SHA-256
  `1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF`;
  24 pages.
- Build output: `paper\build\manuscript_build_wide.pdf`, SHA-256
  `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE`
  (same as the canonical copy for this build).
- Packaged export: `paper\drafts\seam_manuscript_latex_2026-10-23.zip`
  (SHA-256 `9252C9953074AD8301E67FF63EC62E014E2B18AC7EF0A0FF39D42759EC3E5E35`),
  independently extracted and compiled to 24 pages with 0 errors, 0 missing
  characters, and 0 overfull hboxes. The pre-638 zip remains archived at
  `paper\drafts\seam_manuscript_latex_2026-10-23_pre_638fix.zip` (SHA-256
  `9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3`). The
  pre-F4F5 zip remains archived at
  `paper\drafts\seam_manuscript_latex_2026-10-23_pre_F4F5.zip` (SHA-256
  `3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0`). The
  21 October zip remains archived at
  `paper\drafts\seam_manuscript_latex_2026-10-21.zip` (SHA-256
  `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2`).
- Proposed future full-paper build recorded separately in
  `future_paper\FUTURE_PAPER_BUILD.md`; it is not part of the current paper.

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
5. **Frozen authority.** `paper\CONSOLIDATED_CLAIMS.md` remains frozen and now
   contains superseded Progent/APC/SentinelAgent characterizations. It must not
   be used as the current wording authority until separately reconciled.
6. **Deferred expansions.** Classic-literature expansion, the 40-50 percent
   length cut, and any new data figure need explicit approval and new
   verification. The MasDrift citation was authorized and added on 22 October
   2026 after arXiv verification; further new references still require explicit
   approval and verification.

## Frozen constraints

- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are authorized.
- Do not alter `paper\CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`, locks,
  traces, pre-revision files, or frozen artifacts.
- Figure 1 v1 must never be embedded; Figure 1 v2 is canonical.
- Figure 2 must remain vector and 7.0 in wide; the dashed stub must enter the
  X without crossing into `V_read`.
- The paper target is a workshop/short paper, tool track, or arXiv preprint,
  not main-track.
- Public release is gated on the pending metadata and release checks above.

## Next actions

1. Choose the final public contact address, venue/CFP, license, repository URL,
   and archival DOI.
2. If a double-blind venue is chosen, re-anonymize the named-author build before
   submission; do not send the named-author PDF to a double-blind track.
3. Add venue metadata only after a specific CFP is chosen.
4. The 23 October rebuild, export refresh, and repository refresh are complete.
   Leave `dist\sanitized` untouched; publication is a separate owner decision.
5. Do not submit to a public venue until the relevant release checks close.
