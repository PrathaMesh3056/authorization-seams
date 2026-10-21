# Font consistency and PDF QA report

**Date:** 21 October 2026

**Scope:** body typography and figure typography for the 24-page
single-column draft. No manuscript claim, number, status, table data, or frozen
artifact was changed by the font pass. The current-build values below were
refreshed after the separate factual/traceability correction pass; the font
inventory itself is unchanged.

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

- PDF: `paper\drafts\MANUSCRIPT_DRAFT_2026-10-21.pdf`
- SHA-256: `5635F9DDA3A9D75B56C791939F80DC3ACBF5254619661131A6E80AB47F2FB494`
- Pages: 24
- Page size: 612 x 792 pt (US Letter)
- Missing glyphs: 0
- LaTeX errors: 0
- Overfull hboxes: 0
- All fonts embedded and subset.
- `pdfimages`: zero raster images.
- Figure 1: 239.76 x 171.828 pt.
- Figure 2: 504 x 300.24 pt.

## Visual checks

- Page 1: title, author block, abstract, keywords; no public email printed.
- Page 2: Figure 1 at final width; labels and subset glyph coherent; no clipped
  or overlapping text.
- Page 17: Figure 2 at 7.0 in; labels and subset glyph coherent; dashed stub
  enters the X without crossing into `V_read`.
- Pages 23-24: closing status line intact; the seven-entry reference list
  follows it and introduces no new font family.

## Standalone export

`paper\latex_export\main.tex` was compiled independently with XeLaTeX twice.
It produced a 24-page PDF with no errors and no missing characters. The export
contains only `main.tex`, `figures/`, `main.pdf`, and `README.md`; no Poppler
or QA tooling is bundled. The current export uses the same Latin Modern body
and Arial/Cambria Math figures.

- `main.tex` SHA-256: `73CDBEF4E38721D50FB4CCA6973D7E4A0FB8818D86D3C74F06D67384BF049A24`
- `main.pdf` SHA-256: `163CBD7D5D771C6B751DBB6B6A8C63B85E2CE039AA043C9B66951524F8B58BFA`

## Remaining font-related caveat

The figure labels are Arial and the body is Latin Modern. That is an intentional
sans-label/serif-body pairing, not an automatic fallback. The only serif glyph
inside the figures is the subset symbol, set in Cambria Math; all other figure
text remains Arial.
