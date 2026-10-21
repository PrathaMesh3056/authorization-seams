# Final build QA - 21 Oct 2026

## Source

- Manuscript: `paper\MANUSCRIPT_REVISED.md`
- SHA-256: `D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D`
- Abstract: 222 words, byte-identical to the frozen abstract
  (`CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`).
- Section sign: 0 occurrences in the source. All cross-references are spelled
  out as `Section` or `Sections`.
- Star marker: 5 status uses plus 1 definitional use at first occurrence.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments were run.
- References: static seven-entry list after Section 9; no BibTeX dependency.
- Progent: close related-work positioning applied; no stale "unread" claim,
  and no Progent number is reproduced or compared.
- Correction pass: APC expansion and Theorem 4.7 (Composition Soundness);
  SentinelAgent Theorem 4 (Composition Safety with Write-Impact Notification);
  Progent 4/20 attribution removed; seam predicate includes arms 5/6/7;
  mapping taxonomy M0/M2/M2-auth/M0-A/T0/V1/V2; implementation provenance;
  SentinelAgent reconciliation flags disclosed; Pilot-1 pointer and forced
  identities corrected; zero-seam caveat and scope-of-positioning paragraph
  added. See `paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`.

## Built PDF

- Path: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf`
- SHA-256: `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`
- Pages: 24
- Page size: 612 x 792 pt (US Letter)
- Title, author, keywords, and date metadata present.
- Public email: absent. The recorded placeholder is not printed.
- Missing glyphs: 0
- LaTeX errors: 0
- Overfull hboxes: 0
- Underfull hboxes: 3 cosmetic cases (one existing paragraph plus two
  table/list transitions); no text loss or overflow. They are not blockers
  and do not affect the reference list.
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
- Page 2: Figure 1 and the star definition are legible; no clipped or
  overlapping text.
- Page 17: Figure 2 is legible; the dashed stub enters the X without crossing
  into `V_read`.
- Pages 23-24: closing status line present; H1/H2/H3/H5/H6 plus the
  cross-cutting star; H4 and H7 `UNTESTED`. The seven references follow the
  conclusion and are set ragged-right; all entries are legible.
- Table QA: Table 6 uses arm numbers and case-ID references; Table 8 uses
  abbreviated metric headers; Table 9 uses compact code cells and a
  control list. No mid-token underscore wrapping remains in the checked table
  cells. The `SIG-INVALID`, `ATT-SIG-BAD`, `ATT-BIND-MISMATCH`, and `ATT-OK`
  abbreviations are defined in place.

## References

- `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, and `[Progent]` are present as
  bracketed keys.
- Noma Security, the IETF individual Internet-Draft, and arXiv:2605.05440 are
  present as descriptive pointer entries.
- The status note distinguishes arXiv preprints from the industry blog and the
  Internet-Draft. It states that identities were checked, claims were not
  reproduced, and none is a verified input to the measurements.
- No peer-reviewed venue is asserted for APC, TraceGrant, SentinelAgent, or
  Progent. SentinelAgent remains arXiv-only.

## Standalone export

- Source: `paper\latex_export\main.tex`
- SHA-256: `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24`
- Reference PDF: `paper\latex_export\main.pdf`
- SHA-256: `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA`
- Independent XeLaTeX compile: 24 pages, 0 errors, 0 missing characters,
  0 overfull hboxes. The same stable label warning appears.
- Package: `paper\drafts\seam_manuscript_latex_2026-10-21.zip`
- Package SHA-256: `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2`
- The zip was extracted to a clean directory and compiled independently; it
  produced 24 pages with 0 errors, 0 missing characters, and 0 overfull
  hboxes.

## Remaining gates

- Final public email, venue, page limit, anonymity rule, reference style,
  license, repository URL, archival DOI, and release sanitization remain open.
- Classic-literature expansion, the 40-50 percent length cut, and any new data
  figure are deferred pending separate approval.
- No merge into `paper\MANUSCRIPT.md`; no submission.
- H4/H7 remain unauthorized and `UNTESTED`.
