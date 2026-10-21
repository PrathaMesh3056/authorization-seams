# Working artifact snapshot - 21 Oct 2026

This is a working snapshot, not the release manifest. It records the current
manuscript, figures, build, and standalone LaTeX export after the readability,
font, vector-PDF, reference-integration, and factual/traceability correction
passes. It does not replace `paper\hashes.txt` (the six Table 15 hashes) or any
frozen source map.

## Current artifacts

| Artifact | SHA-256 |
|---|---|
| `paper\MANUSCRIPT_REVISED.md` | `D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D` |
| `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf` | `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494` |
| `paper\build\manuscript_build_wide.tex` | `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24` |
| `paper\build\manuscript_build_wide.pdf` | `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494` |
| `paper\latex_export\main.tex` | `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24` |
| `paper\latex_export\main.pdf` | `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA` |
| `paper\drafts\seam_manuscript_latex_2026-10-21.zip` | `D64FD1D46ED0C2A70BF10B2CD1D753DBD130BB4E9B52D247EBAB03B60AD670A2` |
| `paper\figures\figure_1_handoff_anatomy.svg` | `035902B00D700869806BF038F4CE6CBF0B30017BCDB50D3760C4D23F72B9A23C` |
| `paper\figures\figure_1_handoff_anatomy.pdf` | `0AA8A365135AA4E11C5A0D7194FEB3C27947D00FAD8FEA703A1612987C3B90B1` |
| `paper\figures\figure_2_repair_loci.svg` | `F80E70F44958BED3003CE42E7038685B9A66D368D47B9E9F063329B5C3BEBC4A` |
| `paper\figures\figure_2_repair_loci.pdf` | `5ABCDD261C156CDFFF979B313131411FC811C9CFBF3FF4DE5CC95545A7F2C758` |

## Build status

- 24 pages, letter paper, 10 pt, 0.75 in margins.
- 0 missing glyphs, 0 LaTeX errors, 0 overfull hboxes.
- Three cosmetic underfull hboxes remain (one existing paragraph plus two
  table/list transitions); no text loss or overflow. They are not build
  blockers.
- One stable `Label(s) may have changed` warning remains in the build log;
  there is no unresolved-reference warning and no missing glyph. The warning
  does not indicate a missing citation or figure.
- All PDF fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Figure 1: 239.76 x 171.828 pt, vector.
- Figure 2: 504 x 300.24 pt, vector.
- `pdfimages` reports zero raster images in the manuscript and in both figures.
- Standalone `paper\latex_export\main.tex` compiles independently with
  XeLaTeX, producing a 24-page PDF.
- The packaged zip was extracted to a clean directory and compiled
  independently: 24 pages, 0 errors, 0 missing glyphs, 0 overfull hboxes.

## References

- The manuscript now contains a static seven-entry reference list after
  Section 9: `[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, Noma
  Security, the IETF individual Internet-Draft, and arXiv:2605.05440.
- Progent is positioned as a close related work on monotonic confinement
  inside one privilege-control layer, not as an experimental baseline. Its
  reported results are not re-measured or compared here.
- Bibliographic identities were checked on 20 October 2026; the works were
  not reproduced and their claims are not verified inputs.
- The list is style-neutral. Venue-specific reference style remains open.

## Notes

- The current manuscript includes the spelled-out `Section` cross-references,
  the one-sentence star definition at first use, both figure includes, and the
  reference list.
- The build preamble maps the source star to the Latin Modern Math `\star`
  glyph. The PDF shows a star, not a platform symbol-font glyph.
- The figures use Arial for labels and Cambria Math for the subset glyph only;
  no Lucida or Segoe fallback remains.
- References are set ragged-right to avoid stretched interword gaps.
- The placeholder email is not printed in the PDF. The author affiliation is
  the one supplied; city/country and final email remain open.
- `paper\MANUSCRIPT.md`, `paper\CONSOLIDATED_CLAIMS.md`, `paper\hashes.txt`,
  locks, traces, and frozen artifacts remain untouched.
- `paper\CONSOLIDATED_CLAIMS.md` is frozen but now contains superseded
  Progent/APC/SentinelAgent characterizations. It is not the current wording
  authority; the correction record is
  `paper\agent_reports\REVIEW_CORRECTIONS_2026-10-21.md`.
- The proposed future full-paper build is separate at
  `future_paper\FUTURE_PAPER_BUILD.md`; it is not part of this snapshot or the
  current submission package.
