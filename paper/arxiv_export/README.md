# arXiv-compliant named-author export

This directory is the **arXiv submission candidate** for the manuscript. It is
not a public release and it has not been submitted.

It is generated from the current standalone LaTeX export by
`paper/build/build_arxiv.py`. The canonical build remains
`paper/latex_export/` and `paper/drafts/MANUSCRIPT_DRAFT_2026-11-08.pdf`; neither
is modified by this export. The export was rebuilt on 8 November 2026 for the
second external-review correction pass.

## Files

| File | Purpose |
|---|---|
| `main.tex` | Generated arXiv source: 1-inch margins, 10 pt, named author |
| `main.pdf` | 40-page reference compile of this source |
| `figures/figure_1_handoff_anatomy.pdf` | Canonical Figure 1, vector PDF, byte-identical copy |
| `figures/figure_2_repair_loci.pdf` | Canonical Figure 2, vector PDF, byte-identical copy |
| `ARXIV_METADATA.md` | Proposed arXiv metadata and remaining author decisions |
| `README.md` | This file |

## Build

From the repository root:

```powershell
python paper/build/build_arxiv.py
```

The script verifies the pinned `paper/latex_export/main.tex` SHA-256
(`FC2618112D3CE711FEE9B327665527E66664DFE9FF1D8A21AE96BAD327008F32`), applies
only these changes, and compiles with XeLaTeX three times:

- `margin=0.75in` becomes `margin=1in` (arXiv minimum);
- Figure 2 is fitted to `\linewidth` instead of a fixed 7-inch width.

The author display name and PDF metadata are already `Prathamesh N Patil` in
the pinned source; the script verifies that form and rejects the older
`Prathamesh Patil` variant. This export changes no manuscript sentence, number,
table, reference, figure, or hypothesis status. The generated `main.tex`
differs from the source export only in those two content lines plus the build
header.

## Verified output

- 40 pages, 376,744 bytes, US Letter (612 x 792 pt), 10 pt body type, 1-inch
  geometry.
- 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- 4 cosmetic underfull hboxes and 1 stable `Label(s) may have changed` warning.
- All fonts embedded; both figures are vector; `pdfimages` reports zero raster
  images.
- Inline code and artifact paths are upright monospace, including spans inside
  notes; zero `LMMono*-Italic` spans remain; no printed line ends with a
  trailing underscore.
- Title-page and PDF metadata author: `Prathamesh N Patil`.
- Abstract: 248 words, SHA-256
  `7378BB42967D994DF547DF3E860D2AE213F6244F8FB2E244BED0C778B646F768`.
- Twenty-one pipe tables (19 numbered, including Appendix Tables A1 and A2);
  twenty-one static bracketed reference entries; H4 and H7 remain `UNTESTED`.
- No public email, repository URL, DOI, or license is printed.
- Generated source: 194,829 bytes, SHA-256
  `CE72A7F50D18DAFAAC0B50981226D64A663E41899811AFDA28F7AF5804358E67`.
- Reference PDF: 376,744 bytes, SHA-256
  `85E287E55A5187BE3652F7D0173ACCF8326AA69338356141D88B5164CBCF6AF9`.

Both the canonical build and the arXiv candidate now use the unified
`Prathamesh N Patil` form recorded in `CITATION.cff`.

## Source package

The previous upload candidate,
`dist/arxiv/authorization-seams-arxiv-2026-11-07.zip`, is archived and predates
this correction pass. A new zip must be generated from the 8 November source
before submission; no new archive is committed here.

## 8 November 2026 correction pass

The manuscript was corrected after a second external review (independent 3/10;
panel 4,4,4,5,4). E1 is now a scoring-only/bridge-construction illustration:
the receiver contracts are byte-identical in arms 2 and 5 on all eight cases,
and the 4/4 count appears only under a norm recorded after the E1 run. Test 2 is
reported as a receiver-side pre-synthesis check over `snapshot.actions`,
decision-equivalent to restricting the contract's MAY set, not as a bridge-side
contract repair. The two pair-pilot zeroes are attributed to the author-built
translation layers. Tables 16 and 17 disclose the pre-run commitments that were
not met and the eight failed boundary cells. No experiment, frozen artifact,
count, sum, or effective sample size changed; H4 and H7 remain `UNTESTED`.
Abstract: 248 words with SHA-256
`7378BB42967D994DF547DF3E860D2AE213F6244F8FB2E244BED0C778B646F768`.

## 7 November 2026 external-review reconciliation (superseded)

The manuscript was revised after an external review of public HEAD `b3c0c15`.
The revision reports E1 as candidate/scoring-dependent, discloses that arms 2
and 5 decide identically on all eight cases and that the arm-native norm was
locked after the E1 run, reports Pilot 1's 8/40 falsified predictions, restores
H1's resource clause to "not supported", corrects the Table 12 boundary
denominator to 32/48, and adds the lock-before-run and `hashes.txt` renumbering
notes. No experiment, frozen artifact, count, sum, or effective sample size
changed; H4 and H7 remain `UNTESTED`. The abstract remains 222 words with
SHA-256 `B93412AC45C73A9692F33E6B765959C581231BF93DE65F0D6C2BC8CBC460AF38`.
The source and PDF above reflect the later rebuild.

## 7 November 2026 writing-style revision (historical, pre-review)

- All 21 references now use bracketed keys; no reference was added or removed.
  The Pandey entry reports acceptance at IEEE TPS 2026, marked as reported and
  not independently verified here.
- Declarations completed: no external funding, no competing interests, full
  single-author CRediT roles, author-retained data availability, and an
  acknowledgments note.
- Author unified to `Prathamesh N Patil`; Table 5 headers are
  `SA`/`M0`/`Retained` with an explicit column key; body voice is impersonal.
- Typography fixes removed the last Table 13 overfull hbox at the arXiv
  measure. No experiment, count, claim, status, or frozen artifact changed.
- Abstract unchanged at 222 words; H4 and H7 remain `UNTESTED`.
- The source and PDF in this section were the pre-review build; the
  external-review reconciliation above superseded them.

## 6 November 2026 revision (historical)

- Section 6 restructured and deduplicated. Ten verified references added:
  RFC 9396, RFC 2693, Miller's *Robust Composition*, Blaze et al., Appel and
  Felten, Fong, Parisel, ChainCaps, Overlaying Governance, and Local Allow,
  Global Deny. The reference list grew from eleven to twenty-one entries.
- The Introduction's scope paragraph now matches the expanded positioning;
  Section 7.3 gained a design-space rationale.
- Abstract unchanged at 222 words; no new experiment, count, claim, status, or
  frozen artifact changed. H4 and H7 remain `UNTESTED`.

## 5 November 2026 revision (historical)

- Abstract trimmed from 278 to 222 words; no new number, claim, status, or
  citation was added.
- Added mandatory Declarations: data availability, ethics, author
  contributions/CRediT, competing interests, funding, limitations. Author-specific
  CRediT, competing-interest, and funding confirmations remain pending rather
  than invented.
- Added three verified adjacent pointers (RFC 8693, Zanzibar, Macaroons) and a
  falsification/stop-condition paragraph; added effective-witness Appendix
  Table A2; added `report-only` qualifiers to the E1 8/8 `EVIDENCE-VERIFIED`
  cells; added an explicit H4/H7 gate.
- The reference list grew from eight to eleven entries. No frozen artifact was
  edited.

## 31 October review-correction pass (historical)

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and the zero-novelty finding are `REFINED`; H1's resource clause is
  `UNTESTED`; H4 and H7 remain `UNTESTED`.
- The abstract was 278 words at that point.

## Remaining submission gates

arXiv endorsement, license selection, public contact email, ORCID (optional),
repository visibility/URL, archival DOI, and release sanitization remain owner
decisions. A double-blind venue would require a separate anonymized build; this
one is named-author.
