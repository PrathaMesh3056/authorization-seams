# Final build QA - 23 Oct 2026

## Source

- Manuscript: `paper\MANUSCRIPT_REVISED.md`
- SHA-256: `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510`
- Bytes: 111,322 (557 lines)
- Abstract: 222 words, byte-identical to the frozen abstract
  (`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).
- Section sign: 0 occurrences in the source. All cross-references are spelled
  out as `Section` or `Sections`.
- Star marker: 5 status uses plus 1 definitional use at first occurrence.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments were run.
- References: static eight-entry list after Section 9; no BibTeX dependency.
  The first seven identities were checked on 20 October 2026; MasDrift
  (arXiv:2608.07556v3) was checked and added on 22 October 2026.
- Progent: close related-work positioning applied; no stale "unread" claim,
  and no Progent number is reproduced or compared.
- Correction pass: the earlier APC/SentinelAgent/Progent, seam-predicate,
  mapping, provenance, reconciliation, and zero-seam corrections remain in
  place. The 23 October finalization adds F1-F13: exporter `\path` to
  `\texttt`, terminology cleanup, `ATT-OK` alias, H1-H7 status key, the 638
  token-event denominator, named author, reset-control note, T1 fractions,
  six-control ledger note, SentinelAgent P1/P3-P7 TLA+ qualifier, and
  Noma/IETF softening. The independent-review F4/F5 correction changes the
  handoff-norm sentence to "kept the 4 leaks" and scopes the Table 12 H6 row to
  the measured pairs with the disclosed E1 action-family exception. F14 and F15
  remain optional and unapplied.
- Table 15 suffix note: `MANUSCRIPT_REVISED.md` line 521.

## Built PDF

- Path: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf`
- SHA-256: `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC`
- Pages: 24
- File size: 321,386 bytes
- Page size: 612 x 792 pt (US Letter)
- Title, author, keywords, and date metadata present.
- Author metadata: `Prathamesh Patil`; title page also prints the author block.
- Public email: absent. The recorded placeholder is not printed.
- Missing glyphs: 0
- LaTeX errors: 0
- Overfull hboxes: 0
- Underfull hboxes: 3 cosmetic cases; no text loss or overflow. They are not
  blockers and do not affect the reference list.
- Label warning: one stable `Label(s) may have changed` warning remains after
  the three-pass build. There is no unresolved-reference warning and no
  missing glyph. The warning is treated as a build-tooling artifact, not a
  factual defect.
- Fonts: Latin Modern text/math/mono; Arial labels plus Cambria Math subset
  glyph in the figures. No Segoe UI Symbol or Lucida Sans Unicode.
- All fonts embedded and subset.
- Raster images: 0 in the manuscript and in both figure PDFs.
- Figure 1: 239.76 x 171.828 pt, vector.
- Figure 2: 504 x 300.24 pt, vector.
- Page 1: title, named author block, abstract, and keywords; no public email
  printed.
- Page 2: Figure 1 and the star definition are legible; no clipped or
  overlapping text.
- Page 16: Figure 2 is legible; the dashed stub enters the X without crossing
  into `V_read`. The dashed "Fail-closed refusal" box remains a cosmetic
  callout near the Locus A border (review F13).
- Pages 16-17: Table 12 begins on page 16 and continues on page 17 with the
  header repeated; the scoped H6 row is legible.
- Pages 23-24: closing status line present; H1/H2/H3/H5/H6 plus the
  cross-cutting star; H4 and H7 `UNTESTED`. The eight references follow the
  conclusion and are set ragged-right; all entries are legible.
- Table QA: Table 6 uses arm numbers and case-ID references; Table 8 uses
  abbreviated metric headers; Table 9 uses compact code cells and a control
  list. No mid-token underscore wrapping remains in the checked table cells.
  The `SIG-INVALID`, `ATT-SIG-BAD`, `ATT-BIND-MISMATCH`, and `ATT-OK`
  abbreviations are defined in place.
- Table 15: the caption and table body both appear on page 23; the caption
  orphan reported against the older 21 October snapshot is resolved. The
  suffix note is at line 521.
- Visual QA checked pages 1, 2, 3, 8, 9, 10, 16, 17, 18, 19, 20, 22, 23, and
  24; Tables 4-7 are clean, the H1-H7 key is readable, Table 12's header
  repeats on page 17, and the Section 6 softening is visible.
- The older snapshot's four expected divergences are resolved in this build:
  the 16-case H5 signature-family structure, the `tests\` Task D path prefix,
  the eight-case family confusion-matrix wording, and the eight-reference list
  including MasDrift.

## Independent-review reconciliation - 23 Oct 2026

The independent review was run against the archived 21 October PDF
(`5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`), not
this build. Rechecked against the current 23 October build:

| Review ID | Current status |
|---|---|
| F1 Table 4 identifier breaks | Resolved: Tables 4-7 are clean; full identifiers are present. |
| F2 Table 15 caption orphan | Resolved: caption and body both on page 23. |
| F3 `{[}...{]}` escape | Resolved: no brace-escape artifact; the action set prints as `[read_public, save_internal]`. |
| F4 "kept the 4 denials" | Corrected to "kept the 4 leaks". |
| F5 H6 row | Corrected: the Table 12 H6 row is scoped to the measured pairs with the disclosed E1 action-family exception. Table 12 spans pages 16-17 with the header repeated. |
| F6 `send_externalnotinscope` | Resolved: prints as `action send_external not in scope`. |
| F7 SentinelAgent hyphenation | Remains cosmetic ("Sen-tinelAgent" at the Section 2 heading); no claim impact. |
| F8 `apc_apc_preserved`/`apc_apc_reset` row labels | Minor row-label clarity; accepted for this working preprint. |
| F9 488/150 denominator | Resolved: "out of 638 token-event calls" with the component breakdown. |
| F10 24/28 case-event wording | Minor clarity; accepted for this working preprint. |
| F11 POEC/DAS/SA expansions | Minor; accepted for this working preprint. |
| F12 Table 5 caption scope | Minor; accepted for this working preprint. |
| F13 Figure 2 callout collision | Cosmetic; the dashed "Fail-closed refusal" box remains close to the Locus A border. |
| F14 Section 3.1 block split | Cosmetic page-break layout; accepted. |
| NITs | Non-blocking: Table 9 caption hyphen, Table 13 row label, Section 5 capitalization, Section 7.4 wording, Section 9 antecedent, Tallam reference-status note, no public email, untagged PDF, 3 underfull hboxes. |

No unresolved MAJOR finding remains. F7, F8, and F10-F14 and the NITs are
recorded as minor/cosmetic residuals; none changes a measured claim, number,
status, table hash, or frozen artifact.

## References

- `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, and `[MasDrift]` are
  present as bracketed keys.
- Noma Security, the IETF individual Internet-Draft, and arXiv:2605.05440 are
  present as descriptive pointer entries.
- The status note distinguishes arXiv preprints from the industry blog and the
  Internet-Draft. It states that identities were checked, claims were not
  reproduced, and none is a verified input to the measurements.
- No peer-reviewed venue is asserted for APC, TraceGrant, SentinelAgent, or
  Progent. SentinelAgent remains arXiv-only.

## Standalone export

- Source: `paper\latex_export\main.tex`
- SHA-256: `28EA541F13643026DA05BCC906CCC2649C08ED1BDA630DCBCF8FF6495B00A8DB`
- Reference PDF: `paper\latex_export\main.pdf`
- SHA-256: `9F781FEC64797AD1D6412D3485DE385D3566FF348C657E3C9747488A2628C0B0`
- Independent XeLaTeX compile: 24 pages, 0 errors, 0 missing characters,
  0 overfull hboxes. The same stable label warning appears.
- Package: `paper\drafts\seam_manuscript_latex_2026-10-23.zip`
- Package SHA-256: `9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3`
- The zip was extracted to a clean directory and compiled independently; it
  produced 24 pages with 0 errors, 0 missing characters, and 0 overfull
  hboxes.
- The pre-F4F5 23 October PDF and zip remain archived at
  `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_F4F5.pdf` (SHA-256
  `5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B`) and
  `paper\drafts\seam_manuscript_latex_2026-10-23_pre_F4F5.zip` (SHA-256
  `3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0`). The
  21 October PDF and zip also remain archived; they are not overwritten.

## Remaining gates

- Final public email, venue, page limit, anonymity rule, reference style,
  license, repository URL, archival DOI, and release sanitization remain open.
- The build is named-author; a double-blind venue requires re-anonymization.
- Classic-literature expansion, the 40-50 percent length cut, and any new data
  figure are deferred pending separate approval.
- No merge into `paper\MANUSCRIPT.md`; no submission.
- H4/H7 remain unauthorized and `UNTESTED`.
