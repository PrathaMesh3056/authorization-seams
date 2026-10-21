# Repository build and QA record

Recorded 2026-10-21 on Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12
XeLaTeX). This is a local validation record; no remote is configured and
nothing has been pushed.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (staging copy; `RPaper` working archive untouched) |
| Local commit | `69586d5` on `main` (root commit) |
| Tracked files | 294 (+ `artifacts/sha256sums.txt`, `artifacts/manifest.json`) |
| Tracked bytes | 15,460,113 (per `artifacts/manifest.json`) |
| Remote | none |

## Integrity

| Check | Result |
|---|---|
| `python scripts/verify_artifacts.py` | 294 files, all hashes match |
| `python -m pytest -q qa` | 9 passed |
| TraceGrant Task D tests (`pytest -q tests`) | 52 passed |
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

A fresh build is 320,078 bytes; the canonical draft is 320,076 bytes. PDF
generation is not byte-identical across directories, so the canonical hash is
verified on the tracked PDF, not on the fresh build. Page count and log counts
are the build acceptance criteria.

## Release helpers

| Artifact | Result |
|---|---|
| `dist/sanitized/` | 296 files; own manifest verifies; 9 QA tests pass |
| `dist/seam-conformance-kit-20261021-review.zip` | 2,101,313 bytes; SHA-256 `DCB85AB69AA8C403366CC8B7430856EDAC8108E75EF7758EB2D5EB5A48094C46` |
| Zip extraction check | manifest verifies; 9 QA tests pass; paper builds to 24 pages |

## Fresh-clone check

A local `git clone` of the repository checked out byte-identical content: the
manifest verified, all 9 QA tests passed, and the paper built to 24 pages with
the same log counts. This confirms the `* -text` attribute and the frozen
artifacts survive a normal clone.

## Gate reminder

This record does not close the publication gates. License, final public email,
venue metadata, repository URL, archival DOI, and public sanitization review
remain open (`RELEASE_CHECKLIST.md`). H4 and H7 remain `UNTESTED`.
