# The Handoff Nobody Owns — locked-artifact study of cross-mechanism authorization seams

Working preprint and reproduction package for a measurement study of what
happens when one authorization mechanism hands a narrowed decision to another.

> **Status:** prepared locally, **no remote configured and nothing pushed**.
> The manuscript is a 24-page single-column arXiv-style named-author draft for a
> workshop/short-paper or tool-track submission. It is not peer reviewed, it
> has not been merged into the frozen `MANUSCRIPT.md`, and it has not been
> submitted anywhere. Hypotheses H4 and H7 remain `UNTESTED`. The 23 October
> build prints the author name and affiliation; a double-blind venue would
> require re-anonymization.

## What this repository is

- The corrected manuscript source and the canonical 23 October 2026 named-author
  PDF.
- The locked-artifact harnesses for the APC → TraceGrant, APC → SentinelAgent,
  and bridge-boundary experiments, with their frozen cases, locks, and stored
  results.
- The independent TraceGrant Task D implementation and the SentinelAgent
  prototype pinned for the SentinelAgent pilot.
- Build, manifest, and integrity-check tooling for paper and artifacts.

## What this repository is not

- It is **not** a claim that any third-party mechanism is broken or secure. The
  paper measures composition it can observe under explicit bridge mappings.
- Progent is related work, not a baseline. Its published numbers are its
  authors' self-report and are not reproduced, re-measured, or compared here.
- It does not contain the large working archive (local virtual environments,
  upstream clones, third-party PDFs). Those are fetched or referenced by the
  bootstrap and provenance docs.
- H4 and H7 are not tested. No result in this repository should be read as
  evidence for or against them.

## Repository layout

| Path | Contents |
|---|---|
| `paper/` | Corrected manuscript, canonical PDF, figures, Pandoc/XeLaTeX build |
| `paper/latex_export/` | Standalone single-file LaTeX export of the same draft |
| `tests/` | Frozen experiment trees, pinned inputs, locks, stored results |
| `artifacts/` | Generated SHA-256 manifest and integrity metadata |
| `docs/` | Method overview, reproducibility notes, internal status and QA records |
| `future_paper/` | Proposed SeamBench full-paper program; not part of this submission |
| `scripts/` | Build, verify, bootstrap, sanitize, and package entry points |
| `qa/` | Repository-level integrity tests |

The `tests/` layout is deliberate. The frozen scripts resolve their inputs from
sibling directories, so the directory names must stay exactly as they are.

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
```

The build writes generated files under `paper/build/`. The canonical PDF is
`paper/drafts/MANUSCRIPT_DRAFT_2026-10-23.pdf`; the build does not overwrite it.

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
- Any mismatch is a hard failure. Do not "fix" a hash by editing the manifest
  without recording why in `CHANGELOG.md`.

## Publication gates

These remain open and are tracked in `docs/RELEASE_CHECKLIST.md`:

- final public author email;
- target venue/CFP, page limit, anonymity rule, reference style;
- license selection (code and manuscript);
- repository URL and archival DOI;
- release sanitization of machine-local paths and third-party inputs.

## Citation

See `CITATION.cff`. Until the preprint is posted, cite the repository as an
unpublished working artifact; do not cite a DOI that does not exist.

## License

**No license has been granted yet.** `LICENSE` is a release gate, not a grant.
Do not redistribute this repository until the owner replaces it with an
explicit code license and an explicit manuscript license.
