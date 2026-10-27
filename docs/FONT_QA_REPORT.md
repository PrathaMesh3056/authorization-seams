# Font consistency and PDF QA report

**Date:** 28 October 2026

**Scope:** body typography and figure typography for the 25-page
single-column named-author draft. No manuscript claim, number, status, table
data, or frozen artifact was changed by the font pass. The current-build values
below were refreshed for the 28 October path-format correction; the font
inventory itself is unchanged from the earlier font pass.

## Problem found

The PDF embedded more than one visual system:

- Latin Modern for body text, math, and monospace;
- Segoe UI Symbol for the body `★` fallback;
- Arial plus Lucida Sans Unicode in the figure PDFs, with Lucida appearing as
  an automatic fallback for glyphs Arial lacks (notably `⊆`).

That mixture produced the visible irregularities: the body star did not match
the body font, and the figure math glyphs did not match the figure labels.

## Fix applied

### Body

- Kept Latin Modern as the official body, math, and mono family.
- Mapped the source `★` to the Latin Modern Math `\star` glyph through the
  build preamble. The PDF now shows a star typeset from the body math font,
  not a platform symbol font.
- Added one definitional sentence at first use: the star marks the frozen
  cross-cutting claim, not a significance test. This adds no number, status,
  claim, or citation.
- No Segoe UI Symbol fallback remains.
- Inline code and artifact paths are forced to upright monospace, including
  spans inside italic notes. `\texttt` and `\path` are redefined to use upright
  shapes, and all three PDFs contain zero `LMMono*-Italic` spans.

### Figures

- Kept Arial as the figure label font, preserving the hand-authored geometry
  and text metrics.
- Set the subset glyph `⊆` explicitly in Cambria Math in both SVGs, instead of
  letting the renderer substitute Lucida Sans Unicode.
- Re-exported both figures to vector PDF with Inkscape.
- No Lucida Sans Unicode or Segoe UI Symbol remains.
- Figure geometry, colors, captions, dashed stub, X barrier, and vector output
  are unchanged.

## Before / after font inventory

| Before | After |
|---|---|
| Latin Modern Roman/Math/Mono | Latin Modern Roman/Math/Mono |
| Segoe UI Symbol (body `★`) | none |
| Arial / Arial Bold / Arial Italic (figures) | Arial / Arial Bold / Arial Italic (figures) |
| Lucida Sans Unicode (figure fallback) | none |
| - | Cambria Math (figure subset glyph) |

## Build QA

- PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-26.pdf`
- SHA-256: `BC6AB2C5A82654D7FC3831AE4B7CEA66EE4A4C38A5ABF5924BC8EC65F236C544`
- Pages: 25
- File size: 321,990 bytes
- Page size: 612 x 792 pt (US Letter)
- Named-author build: `Prathamesh Patil`; the placeholder email is not printed.
- Missing glyphs: 0
- Fatal LaTeX errors: 0
- Overfull hboxes: 0
- Three cosmetic underfull hboxes, six ignored infinite-glue-shrinkage
  diagnostics, and one stable `Label(s) may have changed` warning remain; none
  is a blocker.
- All fonts embedded and subset.
- `pdfimages`: zero raster images.
- Figure 1: 239.76 x 171.828 pt.
- Figure 2: 504 x 300.24 pt.

## Visual checks

- Page 1: title, named author block, abstract, keywords; no public email
  printed.
- Page 3: Figure 1 at final width; labels and subset glyph coherent; no clipped
  or overlapping text.
- Page 18: Figure 2 at 7.0 in; labels and subset glyph coherent; dashed stub
  enters the X without crossing into `V_read`. The dashed "Fail-closed refusal"
  callout is close to the Locus A border but does not collide with it; the text
  is legible. Locus B's connector points to the bridge-translation step and
  Locus A's connector points to the carried-record/read-set gap.
- Pages 16-17: Table 12 begins on page 16 and continues on page 17 with the
  header repeated; the scoped H6 row and the display-only artifact-root
  cross-reference to Section 3.5 are legible.
- Pages 24-25: Appendix A/Table A1 and the closing status line are intact; the
  eight-entry reference list follows and introduces no new font family. The
  Table 15 caption and table body are both on page 23.

## Standalone export

`paper\latex_export\main.tex` was compiled independently with XeLaTeX twice.
It produced a 25-page PDF with no fatal errors and no missing characters. The
export contains only `main.tex`, `figures/`, `main.pdf`, and `README.md`; no
Poppler or QA tooling is bundled. The current export uses the same Latin Modern
body and Arial/Cambria Math figures.

- `main.tex` SHA-256: `ED7970DFA49DB36B3759B3ED59700679C81EED91BFA326723503C5670E9A8515`
- `main.pdf` 25 pages, 321,988 bytes, SHA-256:
  `9B569A258F2510DC0823BDB839FFE9511CE4DE34171E5670EF30D35A17E20B7D`

## Remaining font-related caveat

The figure labels are Arial and the body is Latin Modern. That is an intentional
sans-label/serif-body pairing, not an automatic fallback. The only serif glyph
inside the figures is the subset symbol, set in Cambria Math; all other figure
text remains Arial.
