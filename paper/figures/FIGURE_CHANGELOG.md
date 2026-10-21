# Figure change log — 20 Oct 2026

Scope: figure-only QA fixes after the camera-ready SVG review.

No manuscript, frozen claim, lock, trace, evidence file, or Table 15 hash was changed.
`paper\hashes.txt` was not touched.

## Pre-edit hashes

| File | SHA-256 |
|---|---|
| `figure_1_handoff_anatomy_v2.svg` | `1AF4F31590354001D0EE317549F1F3D0479F2A1B82102A4522EDADDCDB946882` |
| `figure_1_handoff_anatomy.svg` (v1, superseded; do not embed) | `AB3FE86490390D58EEA8937F203CD4DB40C27EDFAAF2EC7F292D3187724C47F4` |
| `figure_2_repair_loci.svg` | `B4600FCC478DB91E4294A0CABC4B5BD3E476C13431BD621CDC352EB53092B252` |

## Changes applied

### Figure 1 — `figure_1_handoff_anatomy_v2.svg`

- Changed the small bridge/receiver labels from orange `#E69F00` and green `#009E73` to `#333333`: `ρ_R =`, `B(A′, state)`, `M_R =`, `(V_R, admit_R)`, `read set V_read`, `fields the decision reads`, and `consumes V_read`.
- Kept orange and green on the party box strokes; kept the accessible blue labels.
- Removed `textLength="166" lengthAdjust="spacingAndGlyphs"` from `fields the decision reads`.
- Set that explanatory line to `font-size="15"` (7.5 pt at 3.33 in) so it retains a visible margin inside the read-set box after removing `textLength`.
- Did not enlarge the 16-unit body labels; 8 pt is within the brief’s 8–9 pt target and avoids overflow.

### Figure 2 — `figure_2_repair_loci.svg`

- Added a 6-unit dashed gray stub from the carried-record right edge into the X barrier, with no arrowhead and no crossing into `V_read`.
- Updated the `<desc>` to state that the short dashed stub terminates at the X barrier.
- Re-stroked the `narrowed manifest` box from receiver green `#009E73` to neutral `#666666`.
- Set the step-3 `ρ_R` label from `font-size="18"` to `font-size="16"`.
- Raised `repair at the bridge`, `bridge derivation`, and `narrowed manifest` from 14 to 15 units (7.5 pt).
- Kept the X barrier, bracket tips, labels, and content unchanged.

## Post-edit hashes

| File | SHA-256 |
|---|---|
| `figure_1_handoff_anatomy_v2.svg` | `799B1B9101F95323881B7A7330B9BF84BA3BAE671D35D2F719B0CF48EAC48497` |
| `figure_1_handoff_anatomy.svg` (canonical, promoted from v2) | `799B1B9101F95323881B7A7330B9BF84BA3BAE671D35D2F719B0CF48EAC48497` |
| `figure_2_repair_loci.svg` | `F8E5FBDAF662E30176109CAA9745FF229982697577B0363C4A472D0E6E294452` |
| `superseded/figure_1_handoff_anatomy_v1.svg` (archived) | `AB3FE86490390D58EEA8937F203CD4DB40C27EDFAAF2EC7F292D3187724C47F4` |
| `figure_1_handoff_anatomy.pdf` (vector) | `5343A821F16F846C4645F73FCE036E1176F603070E5BFF89750E34E659D36AD9` |
| `figure_2_repair_loci.pdf` (vector) | `96D0A84161EFF6DABF1F484FCF42802EC723B63CA4A98FE53FBD1ABBEB135E1A` |

## Render checks

- Both SVGs parse as XML with the expected viewBoxes.
- Chrome headless renders at 2× and 3× at the intended print widths: Figure 1 at 3.33 in, Figure 2 at 7.0 in.
- No edge clipping observed. Figure 1’s read-set explanatory line now has visible side margins. Figure 2’s stub is visible entering the X; the X still marks the unread stop.
- No labels, numbers, claim-status tokens, or captions were changed.

## Vector PDF conversion

- Converted with Inkscape 1.4.4 (`dcaf3e7`) at 18:16 on 20 Oct 2026, using `--export-area-page`.
- Figure 1 PDF: `239.76 x 171.828 pt` = `3.33 x 2.386 in`; Figure 2 PDF: `504 x 300.24 pt` = `7.0 x 4.17 in`.
- `pdffonts` reports all fonts embedded and subsetted; `pdfimages -list` reports zero images (no rasterization) for both PDFs.
- `pdftotext` extracts the exact aphorism from both PDFs; no `UNTESTED`/`SUPPORTED`/`REFINED` tokens appear.
- 300-dpi previews are under `pdf_preview/`; visual inspection confirms no edge clipping and the Figure 2 dashed stub entering the X without crossing into `V_read`.

## Status

- Figure 1 v2 was promoted to canonical `figure_1_handoff_anatomy.svg`; the two files are byte-identical.
- The superseded v1 is preserved at `superseded/figure_1_handoff_anatomy_v1.svg` and must not be embedded.
- Figure 2 remains at its canonical path.
- Vector PDF conversion is complete. Manuscript integration remains pending.
