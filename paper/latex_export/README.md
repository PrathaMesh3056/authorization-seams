# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 21 October 2026 draft of the seam-research
manuscript. It is a working preprint source, not a submission-ready package.

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

No BibTeX run is required. References are a static, verified 7-entry list
embedded in `main.tex`; `references.bib` is not needed for this compile. The
source uses a single-column `article` class, 10 pt, letter paper, 0.75 in
margins. Figure 1 is included at 3.33 in wide; Figure 2 is included at 7.0 in
wide, so the 0.75 in margin is required.

The main text uses Latin Modern. The figure PDFs already embed Arial for
labels and Cambria Math for symbols; those fonts are contained in the figure
files and are not needed to compile the body.

## Provenance

- Manuscript source: `paper\MANUSCRIPT_REVISED.md`
- Manuscript SHA-256: `D1A7AA9E3119AE3850FBA1C012B12ED528F6BF2B0CA0A794BC2A63310E06AF1D`
- Canonical draft PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf`
- Canonical draft PDF SHA-256: `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`
- Standalone `main.tex` SHA-256: `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24`
- Reference PDF SHA-256: `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Draft date in the PDF: 21 October 2026

## References

The manuscript now contains a static list of seven entries: `[APC]`,
`[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, Noma Security, the IETF
individual Internet-Draft, and arXiv:2605.05440. Bibliographic identities were
checked on 20 October 2026; the works were not reproduced, and their claims are
not treated as verified inputs. The list is style-neutral and must be adapted
only after the target venue is selected.

## Known gates

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
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- The static reference list appears after Section 9 and is set ragged-right to
  avoid stretched interword gaps.
