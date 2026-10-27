# Repository build and QA record - 26 October 2026

Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This is a local
validation record. The repository has a private `origin` remote and the current
state is pushed to `origin/main`; no public release has occurred.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (working copy; `RPaper` archive untouched) |
| Local branch | `main` |
| Tracked files | 312 |
| Tracked bytes | 17,434,650 |
| Remote | private `origin` |
| Canonical PDF | `paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf` |
| Canonical PDF SHA-256 | `B3D39ED0D5F26CB42C1B436D43B9D5FFCC3C6FE613461C860561A0DBEBB788D3` |
| arXiv candidate | `paper/arxiv_export/main.pdf` |
| arXiv PDF SHA-256 | `7022C36250F5E690E574CB2AF814A2BFD8C538FFBF2812AD156188192FE514D1` |

## Integrity

| Check | Result |
|---|---|
| `python scripts/verify_artifacts.py` | all tracked files match; no missing or unexpected files |
| `python -m pytest -q qa` | 15 passed |
| TraceGrant Task D tests (`cd tests/tracegrant_task_d_20261014 && python -m pytest -q tests`) | 52 passed |
| E1 lock check (`run_extension_e1.py --check`) | dataset/lock SHA match, OK |
| SentinelAgent check (`run_sa.py --check`) | 672 rows, upstream and lock hashes match, OK |
| Boundary check (`run_boundary.py --check`) | 1,152 rows, harness and case hashes match, OK |

## Paper build

`paper/build/build.ps1` completed:

- 25 pages;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 3 cosmetic underfull hboxes;
- 6 ignored infinite-glue-shrinkage diagnostics;
- 1 stable `Label(s) may have changed` warning.

Canonical PDF:
`paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf`, 327,382 bytes, SHA-256
`B3D39ED0D5F26CB42C1B436D43B9D5FFCC3C6FE613461C860561A0DBEBB788D3`.

Standalone export:

- `paper/latex_export/main.tex` SHA-256
  `4C27CB582582473B961C9DD7E7574D67BD2ECB9C00CA55E6AFDDA493044D8602`;
- `paper/latex_export/main.pdf` 25 pages, 327,383 bytes, SHA-256
  `5901ED2B13AC24C9536E41F313BD2A4BBF161F4BDF46E8A9D7D6FC11500492AE`;
- independent XeLaTeX compile: 0 fatal errors, 0 overfull hboxes, 3 underfull
  hboxes, 6 ignored infinite-glue diagnostics, and 1 stable label warning.

## arXiv candidate

`python paper/build/build_arxiv.py` completed:

- 28 pages, US Letter, 10 pt, 1-inch margins;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 4 cosmetic underfull hboxes;
- 1 stable label warning;
- source SHA-256
  `82DF6A9A2E7AD7B59946C90D7878C8D0E26C9B3BF07FD98790A7C4C5DC83C934`;
- PDF SHA-256
  `7022C36250F5E690E574CB2AF814A2BFD8C538FFBF2812AD156188192FE514D1`.

The extracted arXiv source package compiles to 28 pages with 0 missing glyphs,
0 fatal errors, 0 overfull hboxes, 4 underfull hboxes, 3 ignored infinite-glue
diagnostics, and 1 stable label warning.

## Release helpers

- Review package: `dist/seam-conformance-kit-20261026-review.zip`; regenerated
  from the final manifest. It extracts, verifies the tracked files, passes the
  repository QA suite, and rebuilds the 28-page arXiv candidate. The checksum is
  in the adjacent `.sha256` sidecar.
- arXiv package:
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip`, 160,075 bytes,
  SHA-256 `45774B48313002A5B80F560A14EF01BB3F4644440EF7F419005584863643581C`;
  contains `main.tex` and the two vector figures.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files and remains the stale 21 October tree, not a public-release
  candidate.

## Notes

- The 23 October canonical PDF and standalone export remain archived; the
  26 October build does not overwrite them.
- The correction pass changed no claims, experiments, references, or H4/H7
  status. H4 and H7 remain `UNTESTED`.
- The repository is private; arXiv endorsement, license, public email,
  repository URL, archival DOI, and release sanitization remain owner
  decisions.
