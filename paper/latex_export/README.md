# The Handoff Nobody Owns - standalone LaTeX source

This package reproduces the 7 November 2026 named-author preprint of the
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
- Manuscript SHA-256: `117A229932806A7E4D6205581A7E90FC276C838867BEEBFF7F972E561ABF7722`
- Canonical PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-11-07.pdf`
- Canonical PDF SHA-256: `D8F80E8B9384BB352C440E48EDB0BD3534CBD38CEEE55D942CF8C8F07D7A348F`
- Standalone `main.tex` SHA-256: `FC2618112D3CE711FEE9B327665527E66664DFE9FF1D8A21AE96BAD327008F32`
- Reference PDF: 33 pages, 360,637 bytes
- Reference PDF SHA-256: `A56FF2B9CEC2EABFC92D0C7ECEBB26FBD7401473BF91FA97074A76989FEF9413`
- Build: Pandoc 3.12.1 + XeLaTeX (MiKTeX 25.12)
- Manuscript date in the PDF: 7 November 2026

The 6 November, 5 November, 31 October, and 23 October 2026 canonical PDFs and
their exports remain archived under `paper\drafts\` and `paper\backups\`; none
is overwritten. The pre-review 7 November canonical PDF is archived at
`paper\backups\MANUSCRIPT_DRAFT_2026-11-07_pre_review_fixes.pdf`.

## References

The manuscript now contains a static list of twenty-one bracketed entries:
`[APC]`, `[TraceGrant]`, `[SentinelAgent]`, `[Progent]`, `[MasDrift]`, Noma
Security, the IETF individual Internet-Draft, arXiv:2605.05440, RFC 8693,
Zanzibar, Macaroons, RFC 9396, RFC 2693, Miller, Blaze et al., Appel and
Felten, Fong, Parisel, ChainCaps, Overlaying Governance, and Local Allow,
Global Deny.
Bibliographic identities were checked on 20 October 2026 for the first seven
entries, on 22 October 2026 for MasDrift (arXiv:2608.07556v3), on 5 November
2026 for RFC 8693, Zanzibar, and Macaroons, and on 6 November 2026 for the ten
entries added in that revision; the works were not reproduced, and their claims
are not treated as verified inputs. The Pandey entry reports acceptance at
IEEE TPS 2026 and is marked "acceptance reported, not independently verified
here." The list is style-neutral and must be adapted only after the target
venue is selected.

## Release notes

- The title page and PDF metadata are named-author (`Prathamesh N Patil`); a
  double-blind venue would require re-anonymizing this build.
- Public contact information is intentionally omitted from this build; the
  final public address is still needed.
- Venue, page limit, anonymity rule, reference style, license, repository URL,
  archival DOI, and release sanitization are pending.
- H4 and H7 remain `UNTESTED`; no H4/H7 experiments are part of this package.
- The manuscript is prepared for workshop/short-paper or arXiv submission; no
  peer-reviewed venue is asserted.
- The Declarations section states no external funding, no competing interests,
  full single-author CRediT roles, author-retained data availability, and an
  acknowledgments note.

## QA of the reference PDF

- 33 pages, letter paper.
- Zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes in the
  build.
- Six cosmetic underfull hboxes, six ignored infinite-glue-shrinkage
  diagnostics, and one stable `Label(s) may have changed` warning remain; all
  are non-blocking. The reference PDF has zero unresolved references.
- All fonts embedded; no Segoe UI Symbol or Lucida Sans Unicode fallback.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain. No printed line ends with a
  trailing underscore.
- Both figures are vector; `pdfimages` reports zero raster images.
- Figure 1 is 239.76 x 171.828 pt; Figure 2 is 504 x 300.24 pt.
- Table 2's caption and body are together; Table 3's Total row stays with the
  ledger; Table 5 carries the `SA`/`M0`/`Retained` header and column key; Table
  12 cross-references the Section 3.5 artifact-root key; Appendix Tables A1
  and A2 remain intact in the canonical build.
- The static twenty-one-entry bracketed reference list appears after Section 9
  and is set ragged-right to avoid stretched interword gaps.

## 7 November external-review reconciliation

The manuscript was revised after an external review of public HEAD `b3c0c15`.
The revision reports E1 as a candidate/scoring-dependent result, discloses that
arms 2 and 5 decide identically on all eight E1 cases and that the arm-native
norm was locked after the E1 run, reports Pilot 1's 8/40 falsified predictions,
restores H1's resource clause to "not supported" per the frozen authority,
corrects the Table 12 boundary denominator to 32/48, and adds the
lock-before-run and `hashes.txt` renumbering notes. No experiment, frozen
artifact, count, sum, or effective sample size changed; H4 and H7 remain
`UNTESTED`. The abstract remains 222 words with SHA-256
`B93412AC45C73A9692F33E6B765959C581231BF93DE65F0D6C2BC8CBC460AF38`.
