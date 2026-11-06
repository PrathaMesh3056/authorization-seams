# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 6 November 2026 named-author preprint of the
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

No BibTeX run is required. References are a static, verified 21-entry list
embedded in `main.tex`; `references.bib` is not needed for this compile. The
source uses a single-column `article` class, 10 pt, letter paper, 0.75 in
margins. Figure 1 is included at 3.33 in wide; Figure 2 is included at 7.0 in
wide, so the 0.75 in margin is required.

The main text uses Latin Modern. The figure PDFs already embed Arial for
labels and Cambria Math for symbols; those fonts are contained in the figure
files and are not needed to compile the body.

## Provenance

- Manuscript source: `paper\MANUSCRIPT_REVISED.md`
- Manuscript SHA-256: `76E9E8F6F7233121277B97C0363DF38AC05284F71CD52D26E33D6A8E098B1A98`
- Canonical PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-11-06.pdf`
- Canonical PDF SHA-256: `08752FEED7AA766DA8D4ABDF7FCBDD7907F35A6C53D2E235D57C0A8B6B51C256`
- Standalone `main.tex` SHA-256: `C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139`
- Reference PDF: 32 pages, 355,310 bytes
- Reference PDF SHA-256: `F13D7EA29D4136101CFA44D07F31A1F4C56B09F05AC48CE0E7122AC06FCDB7BC`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Manuscript date in the PDF: 6 November 2026

The 5 November, 31 October, and 23 October 2026 canonical PDFs and their exports
remain archived under `paper\drafts\` and `paper\backups\`; none is overwritten.

## References

The manuscript now contains a static list of twenty-one entries: `[APC]`,
`[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma Security,
the IETF individual Internet-Draft, arXiv:2605.05440, RFC 8693, Zanzibar,
Macaroons, RFC 9396, RFC 2693, Miller, Blaze et al., Appel and Felten, Fong,
Parisel, ChainCaps, Overlaying Governance, and Local Allow, Global Deny.
Bibliographic identities were checked on 20 October 2026 for the first seven
entries, on 22 October 2026 for MasDrift (arXiv:2608.07556v3), on 5 November
2026 for RFC 8693, Zanzibar, and Macaroons, and on 6 November 2026 for the ten
entries added in this revision; the works were not reproduced, and their claims
are not treated as verified inputs. The list is style-neutral and must be
adapted only after the target venue is selected.

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
- Author-specific CRediT, competing-interest, and funding confirmations remain
  pending and are marked as such in the Declarations section.

## QA of the reference PDF

- 32 pages, letter paper.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  build.
- Three cosmetic underfull hboxes, six ignored infinite-glue-shrinkage
  diagnostics, and one stable `Label(s) may have changed` warning remain; all
  are non-blocking. The reference PDF has zero unresolved references.
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 12 cross-references the Section 3.5 artifact-root key; Appendix
  Tables A1 and A2 remain intact in the canonical build.
- The static twenty-one-entry reference list appears after Section 9 and is set
  ragged-right to avoid stretched interword gaps.
