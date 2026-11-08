# arXiv metadata candidate

Status: prepared 26 October 2026; rebuilt 8 November 2026 for the second
external-review correction pass. Not submitted. License, endorsement, repository
visibility, and public contact information remain owner decisions.

## Core metadata

| Field | Value |
|---|---|
| Title | The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry |
| Author | Prathamesh N Patil |
| Affiliation | Department of Computer Engineering, Sardar Patel Institute of Technology |
| Primary category | `cs.CR` (proposed) |
| Cross-list | `cs.AI` (proposed) |
| Comments | 40 pages, 2 figures, 19 numbered tables plus Appendix Tables A1 and A2. Artifact release pending. |
| Journal reference | None |
| DOI | arXiv-issued DOI after announcement; do not fabricate |
| License | `TBD` - author choice; arXiv licenses are irrevocable per version |
| Endorsement | `TBD` - check the current arXiv policy before starting the submission |

## Abstract (verbatim from the frozen manuscript)

Agent authorization rarely stops at a mechanism boundary: a sender narrows authority, a bridge translates it into a record the receiver can read, and the receiver applies admission rules. Each can be correct alone while the composition admits a call the sender never authorized. This paper treats that handoff as a measurement problem, separating two questions: whether the composed system commits a sender-relative violation, and whether composition adds a failure the receiver-only arm does not exhibit. Predictions, cases, arms, and hashes are recorded in internal locks before execution; values are script-checked against stored artifacts. Across 2,446 executions, the composed arms admit 24/40 and 28/48 sender-unauthorized calls in the two pair pilots, but the receiver-only arms admit the same calls; receiver-relative novelty is zero in both, and both zeroes are forced by our translation layers: the TraceGrant-side contract is built per call from the requested tool, and the SentinelAgent-side token is minted directly into a fresh registry. An action-narrowing family illustrates the limit: the receiver contracts are byte-identical in the receiver-only and composed arms, and a 4/4 receiver-relative count appears only under a scoring rule recorded after the data. Non-narrowing-preserving derivations leak four new cases per variant, standalone and composed, locating the fault at the bridge. We close with a replication package and a repair taxonomy: consumption or evidence carriage when the narrowed fact reaches the decision, derivation repair when the bridge widens. The zero is a recorded property of narrowing-preserving mappings on the frozen cases, not a theorem.

Abstract word count: 248. Abstract SHA-256: `7378BB42967D994DF547DF3E860D2AE213F6244F8FB2E244BED0C778B646F768`.

## Source package

The arXiv source package should contain:

```text
main.tex
figures/figure_1_handoff_anatomy.pdf
figures/figure_2_repair_loci.pdf
```

`main.tex` uses a static twenty-one-entry bracketed reference list; no BibTeX
run is required. The PDF is a reference compile, not a substitute for the source
package.

## Pre-upload checks

- Confirm the arXiv license choice; it cannot be changed for an announced
  version.
- Confirm endorsement status for `cs.CR`.
- Confirm the public contact email (not printed in the current PDF) and
  optional ORCID.
- Decide whether to include a public repository URL. Repository visibility and
  URL are unresolved: the external review found a public repository reachable
  at the reviewed HEAD while the reviewed release documents described a private
  repository. Resolve the contradiction before asserting either state. If a URL
  is included, it must resolve publicly.
- Do not add a public email unless it is an address the author is willing to
  display.
- Keep the named-author build separate from any future double-blind venue
  submission.
- A workshop/short/tool-track cut must be rebuilt from the 8 November source;
  the old 13-page CODASPY cut predates this revision.
