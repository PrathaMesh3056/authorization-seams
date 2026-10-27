# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 26 October 2026 named-author preprint of the
seam-research manuscript. It is a preprint source, not a peer-reviewed
publication.

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
- Manuscript SHA-256: `1732872C36D4AC5EAE349450ACA946120F0EA21A2C48235F58985167A414CCC2`
- Canonical PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-26.pdf`
- Canonical PDF SHA-256: `B3D39ED0D5F26CB42C1B436D43B9D5FFCC3C6FE613461C860561A0DBEBB788D3`
- Standalone `main.tex` SHA-256: `4C27CB582582473B961C9DD7E7574D67BD2ECB9C00CA55E6AFDDA493044D8602`
- Reference PDF SHA-256: `5901ED2B13AC24C9536E41F313BD2A4BBF161F4BDF46E8A9D7D6FC11500492AE`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Manuscript date in the PDF: 26 October 2026

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

- 25 pages, letter paper.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  build.
- Three cosmetic underfull hboxes, six ignored infinite-glue-shrinkage
  diagnostics, and one stable `Label(s) may have changed` warning remain; all
  are non-blocking. The reference PDF has zero unresolved references.
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 12 spans pages 16-17 with its alias note; Appendix Table A1
  spans pages 24-25 in the canonical build.
- The static eight-entry reference list appears after Section 9 and is set
  ragged-right to avoid stretched interword gaps.
