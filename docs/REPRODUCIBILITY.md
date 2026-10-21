# Reproducibility

Two separate activities:

1. **Verify the frozen evidence and rebuild the paper** — cheap, offline,
   deterministic, and the default.
2. **Rerun an experiment set from its locked inputs** — slower, needs the
   pinned upstream checkouts, and must be done in a scratch copy so the frozen
   results are not overwritten.

## 1. Verify and rebuild

```powershell
python scripts/verify_artifacts.py
python -m pytest -q qa
pwsh -File paper/build/build.ps1
```

```bash
python scripts/verify_artifacts.py
python -m pytest -q qa
bash paper/build/build.sh
```

Expected:

- `verify_artifacts.py` reports every tracked file matching
  `artifacts/sha256sums.txt`.
- QA checks the manuscript and canonical PDF hashes, the page count, the
  abstract word count, the reference entry count, banned placeholder strings,
  and `UNTESTED` status for H4/H7.
- The paper build produces a 24-page PDF with zero missing glyphs, zero
  LaTeX errors, and zero overfull hboxes.

Toolchain used for the reference build is recorded in `docs/TOOLCHAIN.md`
(Pandoc 3.12.1, MiKTeX 25.12 with XeLaTeX, Python 3.12.7).

## 2. Rerun an experiment set

First fetch the pinned upstream code (network required once):

```powershell
python scripts/bootstrap_vendor.py
```

This clones the APC and Progent commits from
`tests/authorization_pilot/pins.json` into `tests/authorization_pilot/vendor/`.
The clones are ignored by Git. The SentinelAgent prototype used by the second
pilot is already vendored as a small MIT-licensed excerpt.

Then make a scratch copy of the set you want to rerun:

```powershell
Copy-Item -Recurse tests\seam_pilot_v2 $env:TEMP\seam_pilot_v2_rerun
```

| Set | Writer command | Non-destructive check |
|---|---|---|
| APC → TraceGrant pilot | `python run_v2.py all` | none; compare regenerated files by hand |
| E1 action extension | `python run_extension_e1.py` | `python run_extension_e1.py --check` |
| APC → SentinelAgent pilot | `python run_sa.py` | `python run_sa.py --check` |
| Boundary run | `python run_boundary.py` | `python run_boundary.py --check` |
| Discriminating tests | `python discriminating_tests/run_discriminating.py` | none |

The writers overwrite files under `results/`. Never run them against the frozen
tree in this repository.

Experiment execution is offline. The APC pilot blocks socket connections during
runs; the SentinelAgent audit used a loopback-only offline entry point. Setup
steps that need network access are separated from evaluation.

## Dependencies

The pilot sets have their own recorded dependency sets:

- `tests/authorization_pilot/requirements.lock`
- `tests/tracegrant_task_d_20261014/requirements.lock`
- `tests/tracegrant_task_d_20261014/pins.json` (full inherited package inventory)

The repository QA tools need only `requirements-dev.txt`
(`pytest`, `pypdf`).

## What "deterministic" covers

- The frozen cases and locks are content-addressed.
- Runs are strictly sequential; no concurrent arms.
- Randomness is either seeded or recorded; replay checks compare semantic
  output, including the recorded replay hash.
- Discrepancies between predictions and observations are reconciled verbatim
  into stored files that are never edited afterward.

## Known deviations

- Test 2's runner hash differs from its mini-lock after a crash during
  reconciliation; the manuscript discloses this in Section 4.2. Cases, arms,
  and predictions were unchanged, and no measurement or reported count changes.
- Two SentinelAgent-pair prediction overrides, covering two case families, are
  recorded in `tests/seam_pilot_sentinelagent/results/SA_RESULTS.md` with their
  frozen-set justification.

## Third-party inputs not included

- APC and Progent upstream checkouts (fetched by the bootstrap script).
- The TraceGrant paper PDF and extracted page text
  (`tests/tracegrant_task_d_20261014/sources/`) are not redistributed. The
  independent implementation and its provenance inventory are included.
- Large virtual environments and model files from the SentinelAgent audit are
  not included.
