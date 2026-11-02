# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 31 October 2026 named-author preprint of the
seam-research manuscript, refreshed on 31 October 2026 for the five-seat
review correction pass. It is a
preprint source, not a peer-reviewed publication.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Complete single-file LaTeX source (Pandoc-generated body plus build preamble) |
| `figures/figure_1_handoff_anatomy.pdf` | Canonical Figure 1, vector PDF |
| `figures/figure_2_repair_loci.pdf` | Canonical Figure 2, vector PDF |
| `main.pdf` | Reference compile of this package |
| `README.md` | This file |

## Build

Run XeLaTeX twice from this directory:

```powershell
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The compile may print a stable `Label(s) may have changed` warning; the
reference build has zero unresolved references and should be checked by the
page-count and text QA below rather than by warning count alone.

No BibTeX run is required. References are a static, verified 8-entry list
embedded in `main.tex`; `references.bib` is not needed for this compile. The
source uses a single-column `article` class, 10 pt, letter paper, 0.75 in
margins. Figure 1 is included at 3.33 in wide; Figure 2 is included at 7.0 in
wide, so the 0.75 in margin is required.

The main text uses Latin Modern. The figure PDFs already embed Arial for
labels and Cambria Math for symbols; those fonts are contained in the figure
files and are not needed to compile the body.

## Provenance

- Manuscript source: `paper\MANUSCRIPT_REVISED.md`
- Manuscript SHA-256: `79CB8E608CD516B18077943E10433A8F22C834B05AD5D19156330B53B258A876`
- Canonical PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-31.pdf`
- Canonical PDF SHA-256: `F2A3AB17565AF888D23687C5D207DC86C7A6BFE4B58E249608AEF43B607EBE9D`
- Standalone `main.tex` SHA-256: `0EDEC38B19B0836B5E52B0626C60CECCD7533665CD69BFDB19D5C6CCA468A1BA`
- Reference PDF: 29 pages, 337,847 bytes
- Reference PDF SHA-256: `31F45A48ADFD4B0E16EA87727FEB740A22D33A4362C57D6161DF1E46F379E45A`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Manuscript date in the PDF: 31 October 2026

The 23 October 2026 canonical PDF and its export remain archived under
`paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf` and
`paper\backups\latex_export_2026-10-23\`; neither is overwritten.

## References

The manuscript now contains a static list of eight entries: `[APC]`,
`[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma Security,
the IETF individual Internet-Draft, and arXiv:2605.05440. Bibliographic
identities were checked on 20 October 2026 for the first seven entries and on
22 October 2026 for MasDrift (arXiv:2608.07556v3); the works were not
reproduced, and their claims are not treated as verified inputs. The list is
style-neutral and must be adapted only after the target venue is selected.

## Release notes

- The title page and PDF metadata are named-author (`Prathamesh Patil`); a
  double-blind venue would require re-anonymizing this build.
- Public contact information is intentionally omitted from this build; the
  final public address is still needed.
- Venue, page limit, anonymity rule, reference style, license, repository URL,
  archival DOI, and release sanitization are pending.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are part of this package.
- The manuscript is prepared for workshop/short-paper or arXiv submission; no
  peer-reviewed venue is asserted.

## QA of the reference PDF

- 29 pages, letter paper.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  build.
- Three cosmetic underfull hboxes, four ignored infinite-glue-shrinkage
  diagnostics, and one stable `Label(s) may have changed` warning remain; all
  are non-blocking. The reference PDF has zero unresolved references.
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 12 cross-references the Section 3.5 artifact-root key; Appendix
  Table A1 remains intact in the canonical build.
- The static eight-entry reference list appears after Section 9 and is set
  ragged-right to avoid stretched interword gaps.
