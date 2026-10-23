# Repository build and QA record

Recorded 2026-10-21; refreshed 2026-10-23 after the F4/F5 and 638
corrections. Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This
is a local validation record; no remote is configured and nothing has been
pushed.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (staging copy; `RPaper` working archive untouched) |
| Local branch | `main` (local only; see `git log` for the current commit) |
| Tracked files | 297 (see `artifacts/manifest.json`) |
| Tracked bytes | 15,826,372 (see `artifacts/manifest.json`) |
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

A fresh 23 October 638-correction build is 321,409 bytes; the canonical draft
is also 321,409 bytes and the hashes match for this build. Only page 13 changed
relative to the pre-638 build. PDF generation is not byte-identical across
directories, so the standalone export PDF is 321,417 bytes and is verified
separately. Page count and log counts are the build acceptance criteria.

## Release helpers

| Artifact | Result |
|---|---|
| `dist/sanitized/` | 298 files; own manifest verifies; 9 QA tests pass. Not regenerated for the F4/F5 or 638 corrections; left untouched. |
| `dist/seam-conformance-kit-*-review.zip` | Built earlier from tracked files; SHA-256 recorded in the `.sha256` sidecar. Not regenerated for the F4/F5 or 638 corrections. |
| Current standalone package | `paper/drafts/seam_manuscript_latex_2026-10-23.zip` extracted to a clean directory and compiled to 24 pages with 0 errors, 0 missing characters, and 0 overfull hboxes. The package is archived in the working archive, not tracked here. |

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

## 23 October 2026 638 correction

The F9 wording was corrected without changing a number: the 638 is a
non-vacuity count over the full 96-case matrix, not a "token-event call"
denominator and not the 16-case signature family. It is 488 admissions plus
150 token-attached denials; the 150 decomposes as 40 native P6/P7, 42
attestation-stage arm-6, and 68 pre-presentation arm-7 denials. The raw run has
756 events; the remaining 230 admissions and 118 denials lack a token key and
are outside the count.

The source (`84648BDFF4CADF06DB8055EC2A51BC1D1A37FB9E12882BD506530349F0C2DB66`),
canonical PDF (`D2F01F8F80BB9DCC43F59E6CF1763DDACEEA6341AAC0569B18B36C27DD1EA9CE`,
24 pages, 321,409 bytes), standalone `main.tex`
(`107BEF375982BF0120167F59F4C64662151C04B2CCB79AD0BDE3614E15EB786A`), reference
PDF (`1BBAD8114A771F710CDE01903ED4ECC2135F27E8ED13BF1DC99A24BA21500DAF`,
321,417 bytes), and package
(`9252C9953074AD8301E67FF63EC62E014E2B18AC7EF0A0FF39D42759EC3E5E35`) were
rebuilt. The pre-638 PDF
(`086F0F6D451060644DA1C9A8F22DDA985A0F2B16D90A4B9D4BDDF22638BD67AC`), package
(`9F4958FCE4D26492F3B5F4055D6437A59C4CECB5AEB1AECD34762FF42ED704C3`), and source
(`1F82A0ED02CF02405FD8076EDAD74B9ADD2130F154D38F87CE493F80D00E6510`) are archived
in the working archive. The manifest verifies 297 files / 15,826,372 bytes;
`pytest -q qa` is 9 passed; TraceGrant Task D is 52 passed; the E1,
SentinelAgent, and boundary lock checks pass. No claim, experiment, reference,
abstract, or H4/H7 status changed.

## Gate reminder

This record does not close the publication gates. License, final public email,
venue metadata, repository URL, archival DOI, and public sanitization review
remain open (`RELEASE_CHECKLIST.md`). H4 and H7 remain `UNTESTED`.
