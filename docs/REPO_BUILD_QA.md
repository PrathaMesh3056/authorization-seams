# Repository build and QA record

Recorded 2026-10-21; refreshed 2026-10-23 after the F4/F5 correction. Windows
(Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This is a local validation
record; no remote is configured and nothing has been pushed.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (staging copy; `RPaper` working archive untouched) |
| Local branch | `main` (local only; see `git log` for the current commit) |
| Tracked files | 297 (see `artifacts/manifest.json`) |
| Tracked bytes | see `artifacts/manifest.json` |
| Remote | none |

## Integrity

| Check | Result |
|---|---|
| `python scripts/verify_artifacts.py` | 297 files, all hashes match |
| `python -m pytest -q qa` | 9 passed |
| TraceGrant Task D tests (`cd tests/tracegrant_task_d_20261014 && python -m pytest -q tests`) | 52 passed |
| E1 lock check (`run_extension_e1.py --check`) | dataset/lock SHA match, OK |
| SentinelAgent check (`run_sa.py --check`) | 672 rows, upstream and lock hashes match, OK |
| Boundary check (`run_boundary.py --check`) | 1,152 rows, harness and case hashes match, OK |

## Paper build

`paper/build/build.ps1` completed:

- 24 pages;
- 0 missing glyphs;
- 0 LaTeX errors;
- 0 overfull hboxes;
- 3 underfull hboxes (cosmetic);
- 1 stable `Label(s) may have changed` warning (cosmetic).

A fresh 23 October correction build is 321,386 bytes; the canonical draft is
also 321,386 bytes and the hashes match for this build. PDF generation is not
byte-identical across directories, so the standalone export PDF is 321,387
bytes and is verified separately. Page count and log counts are the build
acceptance criteria.

## Release helpers

| Artifact | Result |
|---|---|
| `dist/sanitized/` | 298 files; own manifest verifies; 9 QA tests pass. Not regenerated for the F4/F5 correction. |
| `dist/seam-conformance-kit-*-review.zip` | Built earlier from tracked files; SHA-256 recorded in the `.sha256` sidecar. Not regenerated for the F4/F5 correction. |
| Zip extraction check | Prior check; manifest verifies, 9 QA tests pass, paper builds to 24 pages. Not rerun for the F4/F5 correction. |

## Fresh-clone check

A local `git clone` of the 21 October state checked out byte-identical content:
the manifest verified, all 9 QA tests passed, and the paper built to 24 pages
with the same log counts. This confirms the `* -text` attribute and the frozen
artifacts survive a normal clone. The 23 October correction state has been
verified in place; a fresh clone of the new commit is optional release QA.

## 23 October 2026 refresh

The named-author finalization refreshed `paper/MANUSCRIPT_REVISED.md`, the
canonical 23 October PDF, the standalone LaTeX export, the build guard, and the
current-state docs. `artifacts/sha256sums.txt` was regenerated after the
refresh; `python scripts/verify_artifacts.py` and `python -m pytest -q qa`
pass. The build remains 24 pages with 0 missing glyphs, 0 LaTeX errors, and
0 overfull hboxes; one stable label warning and three cosmetic underfull
hboxes remain. `dist/sanitized` was not regenerated. The current tracked-file
count is recorded in `artifacts/manifest.json`.

## 23 October 2026 F4/F5 correction

The independent PDF review's two remaining major findings were corrected:
the handoff-norm sentence now says "kept the 4 leaks" (F4), and the Table 12
H6 row is scoped to the measured pairs with the disclosed E1 action-family
exception (F5). The source, canonical PDF, standalone export, package, QA
pins, and current-state docs were refreshed. The build remains 24 pages with
0 missing glyphs, 0 LaTeX errors, and 0 overfull hboxes. The pre-F4F5 23
October PDF/zip are archived in the working archive; the previous local commit
(`31843d3`) preserves the pre-correction repository state.

## Gate reminder

This record does not close the publication gates. License, final public email,
venue metadata, repository URL, archival DOI, and public sanitization review
remain open (`RELEASE_CHECKLIST.md`). H4 and H7 remain `UNTESTED`.
