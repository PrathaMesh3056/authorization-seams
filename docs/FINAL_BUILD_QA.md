# Final build QA - 23 Oct 2026

## Source

- Manuscript: `paper\MANUSCRIPT_REVISED.md`
- SHA-256: `6EC07C5A2FBCD423E8BEEA235187366ED74644977E8AE8A4A277FCE577DACC9B`
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
  Noma/IETF softening. F14 and F15 remain optional and unapplied.
- Table 15 suffix note: `MANUSCRIPT_REVISED.md` line 521.

## Built PDF

- Path: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf`
- SHA-256: `5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B`
- Pages: 24
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
- Page 17: Figure 2 is legible; the dashed stub enters the X without crossing
  into `V_read`.
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
- Visual QA checked pages 1, 2, 3, 8, 9, 10, 17, 18, 19, 20, 22, 23, and 24;
  Tables 4-7 are clean, the H1-H7 key is readable, and the Section 6 softening
  is visible.
- The older snapshot's four expected divergences are resolved in this build:
  the 16-case H5 signature-family structure, the `tests\` Task D path prefix,
  the eight-case family confusion-matrix wording, and the eight-reference list
  including MasDrift.

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
- SHA-256: `29E9861ED0866671FB2C8C795E3AD8981451BB7B920B08C2AD5530A22F7540ED`
- Reference PDF: `paper\latex_export\main.pdf`
- SHA-256: `86456E83B99E42D14FAC96BF6E29C00634437C9A5A9F75390285DB001A5EFD06`
- Independent XeLaTeX compile: 24 pages, 0 errors, 0 missing characters,
  0 overfull hboxes. The same stable label warning appears.
- Package: `paper\drafts\seam_manuscript_latex_2026-10-23.zip`
- Package SHA-256: `3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0`
- The zip was extracted to a clean directory and compiled independently; it
  produced 24 pages with 0 errors, 0 missing characters, and 0 overfull
  hboxes.
- The 21 October PDF and zip remain archived; they are not overwritten.

## Remaining gates

- Final public email, venue, page limit, anonymity rule, reference style,
  license, repository URL, archival DOI, and release sanitization remain open.
- The build is named-author; a double-blind venue requires re-anonymization.
- Classic-literature expansion, the 40-50 percent length cut, and any new data
  figure are deferred pending separate approval.
- No merge into `paper\MANUSCRIPT.md`; no submission.
- H4/H7 remain unauthorized and `UNTESTED`.
