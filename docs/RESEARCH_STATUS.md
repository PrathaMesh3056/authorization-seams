# Research status - 21 Oct 2026

## Current position

The manuscript is a 24-page single-column arXiv-style draft built from
`paper\MANUSCRIPT_REVISED.md` (SHA-256
`D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D`).
The build is clean: 24 pages, 0 missing glyphs, 0 LaTeX errors, 0 overfull
hboxes. Three cosmetic underfull hboxes remain; they are not blockers. One
stable `Label(s) may have changed` warning remains in the build log, with no
unresolved-reference warning and no missing glyph. Both figures are vector
PDFs and are included. The static seven-entry reference list remains fixed.

The authorized factual/traceability correction pass is applied. It changed no
claims, experiments, references, or H4/H7 status. The corrections and their
provenance are recorded in
`paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`.

## Completed

- Run 6 QA, section assembly, cross-checks, reconciliation, targeted model
  pass, and independent fixer/verifier.
- Six Table 15 hashes verified; `paper\hashes.txt` remains untouched.
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
- Static seven-entry reference list maintained; bibliographic identities
  checked on 20 October 2026. Claims remain unverified and none is treated as
  a verified input.
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
  Table 9 uses compact code cells and a control list. No mid-token underscore
  wrapping remains in the checked cells.
- Zero-seam caveat and scope-of-positioning paragraph added.
- Current PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf`, SHA-256
  `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`.
- Standalone source: `paper\latex_export\main.tex`, SHA-256
  `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24`;
  reference PDF `paper\latex_export\main.pdf`, SHA-256
  `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA`.
- Packaged export: `paper\drafts\seam_manuscript_latex_2026-10-21.zip`
  (SHA-256 `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2`),
  independently extracted and compiled to 24 pages with 0 errors, 0 missing
  characters, and 0 overfull hboxes.
- Proposed future full-paper build recorded separately in
  `future_paper\FUTURE_PAPER_BUILD.md`; it is not part of the current paper.

## Open gates

1. **Public email.** The placeholder must not appear on the draft PDF (it does
   not). The final public address is still needed.
2. **Venue metadata.** Venue, page limit, anonymity rule, reference style,
   license, repository URL, archival DOI, and release sanitization remain open.
3. **Release package.** The artifact tree is not yet sanitized or manifested
   for public release.
4. **Merge/submission.** No merge into `paper\MANUSCRIPT.md` and no submission
   has occurred.
5. **Frozen authority.** `paper\CONSOLIDATED_CLAIMS.md` remains frozen and now
   contains superseded Progent/APC/SentinelAgent characterizations. It must not
   be used as the current wording authority until separately reconciled.
6. **Deferred expansions.** Classic-literature expansion, the 40-50 percent
   length cut, and any new data figure need explicit approval and new
   verification.

## Frozen constraints

- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are authorized.
- Do not alter `paper\CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`, locks,
  traces, pre-revision files, or frozen artifacts.
- Figure 1 v1 must never be embedded; Figure 1 v2 is canonical.
- Figure 2 must remain vector and 7.0 in wide; the dashed stub must enter the
  X without crossing into `V_read`.
- The paper target is a workshop/short paper, tool track, or arXiv preprint,
  not main-track.
- The paper is not submission-ready until the open metadata and release gates
  close.

## Next actions

1. Obtain the final public email and venue/license/repository decisions.
2. Add venue metadata only after a specific CFP is chosen.
3. Complete release sanitization and the full artifact manifest.
4. Do not merge or submit until every open gate closes.
