# The Handoff Nobody Owns

**A locked-artifact study of cross-mechanism authorization seams**

Research preprint and reproduction package for a measurement study of what
happens when one authorization mechanism hands a narrowed decision to another.

> **Status:** research preprint; not peer reviewed. The canonical manuscript is
> a 33-page, single-column named-author build. A separate 37-page
> arXiv-compliant candidate uses 1-inch margins and the `Prathamesh N Patil`
> display name. Both are prepared for workshop/short-paper or tool-track
> review. Hypotheses H4 and H7 remain `UNTESTED`. The builds print the author
> name and affiliation; a double-blind venue would require re-anonymization.

## Overview

The repository contains the manuscript, its canonical PDF, the standalone LaTeX
export, and the frozen experiment evidence behind the reported measurements.
The experiments use a locked-prediction protocol: cases, arms, inputs, and
hashes are fixed before execution; runs are local and deterministic;
discrepancies are reconciled verbatim; and reported values are generated from
stored artifacts.

## What is included

- The manuscript source and the canonical 7 November 2026 named-author PDF,
  rebuilt after the external-review reconciliation.
- The locked-artifact harnesses for the APC → TraceGrant, APC → SentinelAgent,
  and bridge-boundary experiments, with their frozen cases, locks, and stored
  results.
- The independent TraceGrant Task D implementation and the SentinelAgent
  prototype pinned for the SentinelAgent pilot.
- Build, manifest, and integrity-check tooling for the paper and artifacts.

## Scope and non-claims

- This is **not** a claim that any third-party mechanism is broken or secure.
  The paper measures composition under explicit bridge mappings.
- Progent is related work, not a baseline. Its published numbers are its
  authors' self-report and are not reproduced, re-measured, or compared here.
- H4 and H7 are not tested. No result in this repository should be read as
  evidence for or against them.
- The repository does not redistribute the large local archive, virtual
  environments, upstream clones, or third-party PDFs. Those are fetched or
  referenced by the bootstrap and provenance documentation.

## Repository layout

| Path | Contents |
|---|---|
| `paper/` | Manuscript, canonical PDF, figures, Pandoc/XeLaTeX build |
| `paper/latex_export/` | Current standalone single-file LaTeX export of the manuscript |
| `paper/arxiv_export/` | 37-page arXiv-compliant named-author build (1-inch margins) |
| `tests/` | Frozen experiment evidence: cases, locks, harnesses, and stored results |
| `artifacts/` | Generated SHA-256 manifest and integrity metadata |
| `docs/` | Method overview, reproducibility notes, project status, and QA records |
| `future_paper/` | Proposed SeamBench full-paper program; not part of this manuscript |
| `scripts/` | Build, verify, bootstrap, sanitize, and package entry points |
| `qa/` | Repository-level integrity checks |

The `tests/` layout is deliberate. The frozen scripts resolve their inputs from
sibling directories, so the directory names must stay exactly as they are. These
are experiment records, not a conventional unit-test suite.

## Quick start

Requirements: Python 3.10+ (3.12 recommended), Git, and for the paper build
Pandoc 3.12+ with XeLaTeX.

```powershell
# integrity and repository QA
python scripts/verify_artifacts.py
python -m pytest -q qa

# paper build (Windows)
pwsh -File paper/build/build.ps1

# paper build (Linux/macOS)
bash paper/build/build.sh

# arXiv-compliant candidate (1-inch margins, 37 pages)
python paper/build/build_arxiv.py
```

The build writes generated files under `paper/build/`. The canonical PDF is
`paper/drafts/MANUSCRIPT_DRAFT_2026-11-07.pdf`; the build does not overwrite it.
The 6 November, 5 November, 31 October, and 23 October PDFs remain archived. The
arXiv candidate is `paper/arxiv_export/main.pdf`; its QA record is
`docs/ARXIV_BUILD_QA.md`.

To rerun the experiments, first fetch the two pinned upstream repositories:

```powershell
pwsh -File scripts/bootstrap_vendor.ps1   # clones into tests/authorization_pilot/vendor
```

Then follow `docs/REPRODUCIBILITY.md`. The stored results are the frozen
evidence; rerunning is a verification activity, not a prerequisite for reading
the paper.

## Integrity model

- `paper/MANUSCRIPT_REVISED.md` is hash-checked by `paper/build/preprocess.py`
  before any build.
- `scripts/verify_artifacts.py` checks the manuscript, canonical PDF, LaTeX
  export, figures, and the selected frozen result/lock files against
  `artifacts/sha256sums.txt`.
- Any mismatch is a hard failure. Do not edit the manifest to make a mismatch
  disappear without recording why in `CHANGELOG.md`.

## Release status

Repository visibility is unresolved: a public repository is reachable at the
reviewed HEAD while the reviewed release documents described a private
repository, and `LICENSE` currently grants no redistribution rights. The
arXiv-compliant build is prepared, but arXiv endorsement, license selection,
public contact information, target venue, repository URL, and archival DOI are
not yet assigned. The release checklist is maintained in
`docs/RELEASE_CHECKLIST.md`; the build-specific record is
`docs/ARXIV_BUILD_QA.md`.

## Citation

See `CITATION.cff`. No archival DOI is assigned; cite the repository as an
unpublished preprint until a DOI exists.

## License

No license is granted for redistribution. `LICENSE` records the current
all-rights-reserved status; a release license is still pending.
