# arXiv metadata candidate

Status: prepared 26 October 2026; build refreshed 31 October 2026 for the
five-seat review correction pass. Not submitted. License, endorsement, and
public contact information remain owner decisions.

## Core metadata

| Field | Value |
|---|---|
| Title | The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry |
| Author | Prathamesh N Patil |
| Affiliation | Department of Computer Engineering, Sardar Patel Institute of Technology |
| Primary category | `cs.CR` (proposed) |
| Cross-list | `cs.AI` (proposed) |
| Comments | 32 pages, 2 figures, 18 labeled tables. Artifact release pending. |
| Journal reference | None |
| DOI | arXiv-issued DOI after announcement; do not fabricate |
| License | `TBD` - author choice; arXiv licenses are irrevocable per version |
| Endorsement | `TBD` - check the current arXiv policy before starting the submission |

## Abstract (verbatim from the frozen manuscript)

Agent authorization rarely stops at a mechanism boundary. A sender narrows its authority, a bridge translates the narrowed decision into a record the receiver can read, and the receiver applies its own admission rules. Each component can behave correctly in isolation while the composed system admits a call the sender never authorized. This paper treats that handoff as a measurement problem and separates two questions that are often conflated: whether the composed system commits a sender-relative violation, and whether composition adds a failure the standalone receiver does not already exhibit. We describe a locked-artifact method: predictions, cases, arms, and hashes are frozen before execution; runs are sequential, offline, and deterministic; discrepancies are reconciled verbatim; and reported values are generated from stored artifacts. Across three pilots and a boundary study totaling 2,446 executions, the composed arms admit 24/40 and 28/48 sender-unauthorized calls in the two pair pilots, but the standalone receivers admit the same calls; receiver-relative novelty is zero in both pair pilots, and both zeroes are construction-forced. The one genuine composition-specific test, an action-narrowing family, yields receiver-relative novelty of 4/4 under arm-native scoring and 0/4 under the frozen family-wide convention, while the composed arm admits 4/4 attacks under both; making the receiver consume the carried action set denies 4/4 attacks and allows 4/4 benign calls. Non-narrowing-preserving bridge derivations leak four new cases per variant both standalone and composed, locating that fault at the bridge. We close with a replication package and a repair taxonomy: consumption or evidence carriage when the narrowed fact crosses intact, and derivation repair when the bridge itself widens. The zero is a recorded property of narrowing-preserving mappings on the frozen cases, not a theorem.

Abstract word count: 278. Abstract SHA-256: `060C2D9F7A78D8E346DC4B8A3BA8278BFD5A34883E6B33CED33CAC90A0D57CD7`.

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
