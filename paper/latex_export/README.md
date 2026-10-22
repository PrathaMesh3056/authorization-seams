# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 23 October 2026 named-author draft of the
seam-research manuscript. It is a working preprint source, not a
submission-ready package.

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
- Manuscript SHA-256: `1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510`
- Canonical draft PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-23.pdf`
- Canonical draft PDF SHA-256: `086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC`
- Standalone `main.tex` SHA-256: `28EA541F13643026DA05BCC906CCC2649C08ED1BDA630DCBCF8FF6495B00A8DB`
- Reference PDF SHA-256: `9F781FEC64797AD1D6412D3485DE385D3566FF348C657E3C9747488A2628C0B0`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Draft date in the PDF: 23 October 2026

## References

The manuscript now contains a static list of eight entries: `[APC]`,
`[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma Security,
the IETF individual Internet-Draft, and arXiv:2605.05440. Bibliographic
identities were checked on 20 October 2026 for the first seven entries and on
22 October 2026 for MasDrift (arXiv:2608.07556v3); the works were not
reproduced, and their claims are not treated as verified inputs. The list is
style-neutral and must be adapted only after the target venue is selected.

## Known gates

- The title page and PDF metadata are named-author (`Prathamesh Patil`); a
  double-blind venue would require re-anonymizing this build.
- The author email is intentionally not printed. The recorded placeholder must
  not appear on a public PDF; the final public address is still needed.
- Venue, page limit, anonymity rule, reference style, license, repository URL,
  archival DOI, and release sanitization remain open.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are part of this package.
- The paper remains a workshop/short-paper or arXiv candidate, not a main-track
  submission. No merge into `paper\MANUSCRIPT.md` and no submission has
  occurred.

## QA of the reference PDF

- 24 pages, letter paper.
- Zero missing glyphs, zero LaTeX errors, zero overfull hboxes in the build.
- Three cosmetic underfull hboxes and one stable `Label(s) may have changed`
  warning remain; both are non-blocking. The reference PDF has zero unresolved
  references.
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- Table 15's caption and table body both appear on page 23 in the canonical
  build; the caption orphan reported against the older 21 October snapshot is
  resolved.
- The static eight-entry reference list appears after Section 9 and is set
  ragged-right to avoid stretched interword gaps.
