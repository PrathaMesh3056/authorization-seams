# Working artifact snapshot - 23 Oct 2026

This is a working snapshot, not the release manifest. It records the current
manuscript, figures, build, and standalone LaTeX export after the readability,
font, vector-PDF, reference-integration, factual/traceability, and 23 October
2026 finalization passes, including the F4/F5 wording corrections and the 638
non-vacuity wording correction. It does not replace `paper\hashes.txt` (the six
Table 15 hashes) or any frozen source map.

## Current artifacts

| Artifact | SHA-256 |
|---|---|
| `paper\MANUSCRIPT_REVISED.md` | `84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` | `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE` |
| `paper\build\manuscript_build_wide.tex` | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| `paper\build\manuscript_build_wide.pdf` | `D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE` |
| `paper\latex_export\main.tex` | `107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A` |
| `paper\latex_export\main.pdf` | `1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF` |
| `paper\drafts\seam_manuscript_latex_2026-10-23.zip` | `9252C9953074AD8301E67FF63EC62E014E2B18AC7EF0A0FF39D42759EC3E5E35` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_638fix.pdf` (archived) | `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC` |
| `paper\drafts\seam_manuscript_latex_2026-10-23_pre_638fix.zip` (archived) | `9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3` |
| `paper\backups\MANUSCRIPT_REVISED_pre_638fix_20261023.md` (archived) | `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23_pre_F4F5.pdf` (archived) | `5C9DB3F375F92A4E9A93DDBA64E38960CF25F91CBE20D217EBCDBDCE03BFB82B` |
| `paper\drafts\seam_manuscript_latex_2026-10-23_pre_F4F5.zip` (archived) | `3FCF7B7ABE52D0F20F91C94CB2FC3899778DA11AB13E640B5BC64E8A8E69DDF0` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf` (archived) | `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494` |
| `paper\drafts\seam_manuscript_latex_2026-10-21.zip` (archived) | `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2` |
| `paper\figures\figure_1_handoff_anatomy.svg` | `035902B00D700869806BF038F4CE6CBF0B30017BCDB50D3760C4D23F72B9A23C` |
| `paper\figures\figure_1_handoff_anatomy.pdf` | `0AA8A365135AA4E11C5A0D7194FEB3C27947D00FAD8FEA703A1612987C3B90B1` |
| `paper\figures\figure_2_repair_loci.svg` | `F80E70F44958BED3003CE42E7038685B9A66D368D47B9E9F063329B5C3BEBC4A` |
| `paper\figures\figure_2_repair_loci.pdf` | `5ABCDD261C156CDFFF979B313131411FC811C9CFBF3FF4DE5CC95545A7F2C758` |

## Build status

- 24 pages, letter paper, 10 pt, 0.75 in margins; 321,409 bytes.
- 0 missing glyphs, 0 LaTeX errors, 0 overfull hboxes.
- Three cosmetic underfull hboxes remain; no text loss or overflow. They are
  not build blockers.
- One stable `Label(s) may have changed` warning remains in the build log;
  there is no unresolved-reference warning and no missing glyph. The warning
  does not indicate a missing citation or figure.
- Named-author build: the title page and PDF metadata name Prathamesh Patil.
  The placeholder email is not printed. A double-blind venue would require
  re-anonymization.
- Table 15's caption and table body both appear on page 23; Table 12 spans
  pages 16-17; Figure 1 is on page 3; Figure 2 is on page 16.
- All PDF fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Figure 1: 239.76 x 171.828 pt, vector.
- Figure 2: 504 x 300.24 pt, vector.
- `pdfimages` reports zero raster images in the manuscript and in both figures.
- Standalone `paper\latex_export\main.tex` compiles independently with
  XeLaTeX, producing a 24-page PDF.
- The current 23 October zip was extracted to a clean directory and compiled
  independently: 24 pages, 0 errors, 0 missing glyphs, 0 overfull hboxes.
- The pre-638 23 October PDF/zip/source, the pre-F4F5 23 October PDF/zip, and
  the 21 October PDF/zip remain archived.

## References

- The manuscript contains a static eight-entry reference list after Section 9:
  `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma
  Security, the IETF individual Internet-Draft, and arXiv:2605.05440.
- MasDrift (arXiv:2608.07556v3) was added on 22 October 2026 after arXiv
  identity verification. It is confined to Section 6 and the reference list; it
  introduces no comparison and changes no claim or experiment.
- Progent is positioned as a close related work on monotonic confinement inside
  one privilege-control layer, not as an experimental baseline. Its reported
  results are not re-measured or compared here.
- Bibliographic identities were checked on 20 October 2026 for the first seven
  entries and on 22 October 2026 for MasDrift; the works were not reproduced and
  their claims are not verified inputs.
- The list is style-neutral. Venue-specific reference style remains open.

## Notes

- The current manuscript includes the spelled-out `Section` cross-references,
  the one-sentence star definition at first use, both figure includes, the
  H1-H7 status key, the eight-entry reference list, the corrected handoff-norm
  sentence ("kept the 4 leaks"), the H6 row scoped to the disclosed E1
  exception, and the corrected 638 non-vacuity count (488 admissions plus 150
  token-attached denials over the full 96-case matrix).
- The Table 15 suffix note is at `MANUSCRIPT_REVISED.md` line 521. It discloses
  the 7-character row-3 suffix and the 9-character row-6 suffix; the full
  values remain in `paper\hashes.txt`.
- F2, F3, F6, F9, F13, and F14 are resolved in this build. F1 remains a minor
  identifier line-break residual in Table 4: full identifiers are recoverable,
  but the PDF breaks some of them at underscores. F4, F5, and the 638 wording
  are corrected. F7, F8, F10-F12, and the listed NITs are accepted
  minor/cosmetic residuals. F15 is an optional editorial note; the model
  disclosure is already present.
- The pre-638 source is preserved at
  `paper\backups\MANUSCRIPT_REVISED_pre_638fix_20261023.md`; its rendered PDF
  and zip are preserved in `paper\drafts` as the `_pre_638fix` files above.
- The pre-F4F5 source and export are preserved in local commit `31843d3`; the
  pre-F4F5 rendered PDF and zip are preserved in `paper\drafts` as the
  `_pre_F4F5` files above.
- The build preamble maps the source star to the Latin Modern Math `\star`
  glyph. The PDF shows a star, not a platform symbol-font glyph.
- The figures use Arial for labels and Cambria Math for the subset glyph only;
  no Lucida or Segoe fallback remains.
- References are set ragged-right to avoid stretched interword gaps.
- The placeholder email is not printed in the PDF. The named author affiliation
  is the one supplied; city/country and the final public email remain open.
- `paper\MANUSCRIPT.md`, `paper\CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`,
  locks, traces, and frozen artifacts remain untouched.
- `paper\CONSOLIDATED_CLAIMS.md` is frozen but contains superseded
  Progent/APC/SentinelAgent characterizations. It is not the current wording
  authority; the correction record is
  `paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`.
- The proposed future full-paper build is separate at
  `future_paper\FUTURE_PAPER_BUILD.md`; it is not part of this snapshot or the
  current submission package.
