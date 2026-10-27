# arXiv metadata candidate

Status: prepared 26 October 2026. Not submitted. License, endorsement, and
public contact information remain owner decisions.

## Core metadata

| Field | Value |
|---|---|
| Title | The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry |
| Author | Prathamesh N Patil |
| Affiliation | Department of Computer Engineering, Sardar Patel Institute of Technology |
| Primary category | `cs.CR` (proposed) |
| Cross-list | `cs.AI` (proposed) |
| Comments | 28 pages, 2 figures, 16 tables. Artifact release pending. |
| Journal reference | None |
| DOI | arXiv-issued DOI after announcement; do not fabricate |
| License | `TBD` - author choice; arXiv licenses are irrevocable per version |
| Endorsement | `TBD` - check the current arXiv policy before starting the submission |

## Abstract (verbatim from the frozen manuscript)

Agent authorization rarely stops at a mechanism boundary. A sender narrows its authority, a bridge translates the narrowed decision into a record the receiver can read, and the receiver applies its own admission rules. Each component can behave correctly in isolation while the composed system admits a call the sender never authorized. This paper studies that cross-mechanism handoff as a measurement problem. We describe a locked-artifact method: predictions, cases, arms, and hashes are frozen before execution; runs are sequential, offline, and deterministic; discrepancies are reconciled verbatim; and reported values are generated from stored artifacts rather than transcribed by hand. Across the mechanism pairs, the action-narrowing extension, and the boundary study of bridge variants, we test whether composition adds authorization failures beyond those a receiving mechanism already exhibits standalone. On the frozen case families, the answer is scoped: under narrowing-preserving bridge mappings, composition adds no admission beyond the receiver's own, with a measured exception in an action-narrowing family whose attribution depends on the scoring convention. The exception is bounded to its design point and case family. We distinguish receiver-side and bridge-side repair loci: consumption or evidence carriage when the narrowed fact crosses intact, and derivation repair when the bridge itself widens authority. We close with the conformance kit prepared for others to run these seam tests against their own bridge and mechanism pairs.

Abstract word count: 222. Abstract SHA-256: `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.

## Source package

The arXiv source package should contain:

```text
main.tex
figures/figure_1_handoff_anatomy.pdf
figures/figure_2_repair_loci.pdf
```

`main.tex` uses a static eight-entry reference list; no BibTeX run is required.
The PDF is a reference compile, not a substitute for the source package.

## Pre-upload checks

- Confirm the arXiv license choice; it cannot be changed for an announced
  version.
- Confirm endorsement status for `cs.CR`.
- Decide whether to include a public repository URL. If included, the URL must
  resolve publicly; the current repository is private.
- Do not add a public email unless it is an address the author is willing to
  display.
- Keep the named-author build separate from any future double-blind venue
  submission.
