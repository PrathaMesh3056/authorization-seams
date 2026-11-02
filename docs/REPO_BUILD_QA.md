# Repository build and QA record - 31 October 2026

Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This is a local
validation record. The repository has a private `origin` remote; local `main`
is ahead of `origin/main` and has not been pushed. No public release has
occurred.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (working copy; `RPaper` archive untouched) |
| Local branch | `main` |
| Tracked files | 321 |
| Manifest coverage | 319 selected files; see `artifacts/manifest.json` |
| Remote | private `origin` |
| Canonical PDF | `paper/drafts/MANUSCRIPT_DRAFT_2026-10-31.pdf` |
| Canonical PDF SHA-256 | `F2A3AB17565AF888D23687C5D207DC86C7A6BFE4B58E249608AEF43B607EBE9D` |
| arXiv candidate | `paper/arxiv_export/main.pdf` |
| arXiv PDF SHA-256 | `33207E1E00DB205F3C123C763EDC8FC978C959C2417EB2B4AC4B68D304933CE1` |

## Integrity

| Check | Result |
|---|---|
| `python scripts/verify_artifacts.py` | 319 selected files match; no missing or unexpected files |
| `python -m pytest -q qa` | 15 passed |
| TraceGrant Task D tests (`cd tests/tracegrant_task_d_20261014 && python -m pytest -q tests`) | 52 passed |
| E1 lock check (`run_extension_e1.py --check`) | dataset/lock SHA match, OK |
| SentinelAgent check (`run_sa.py --check`) | 672 rows, upstream and lock hashes match, OK |
| Boundary check (`run_boundary.py --check`) | 1,152 rows, harness and case hashes match, OK |

## Paper build

`paper/build/build.ps1` completed:

- 29 pages;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 3 cosmetic underfull hboxes;
- 4 ignored infinite-glue-shrinkage diagnostics;
- 1 stable `Label(s) may have changed` warning.

Canonical PDF:
`paper/drafts/MANUSCRIPT_DRAFT_2026-10-31.pdf`, 337,843 bytes, SHA-256
`F2A3AB17565AF888D23687C5D207DC86C7A6BFE4B58E249608AEF43B607EBE9D`.

Standalone export:

- `paper/latex_export/main.tex` SHA-256
  `0EDEC38B19B0836B5E52B0626C60CECCD7533665CD69BFDB19D5C6CCA468A1BA`;
- `paper/latex_export/main.pdf` 29 pages, 337,847 bytes, SHA-256
  `31F45A48ADFD4B0E16EA87727FEB740A22D33A4362C57D6161DF1E46F379E45A`;
- independent XeLaTeX compile: 0 fatal errors, 0 overfull hboxes, 3 underfull
  hboxes, 4 ignored infinite-glue diagnostics, and 1 stable label warning.

## arXiv candidate

`python paper/build/build_arxiv.py` completed:

- 32 pages, US Letter, 10 pt, 1-inch margins;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 4 cosmetic underfull hboxes;
- 1 stable label warning;
- source SHA-256
  `52F399DBDC3B65B54B751A2D85ACCBD3ADB21E7F9EB77DDE33F239F0AF1818A5`;
- 340,381-byte PDF with SHA-256
  `33207E1E00DB205F3C123C763EDC8FC978C959C2417EB2B4AC4B68D304933CE1`.

The last generated source package (26 October; historical) compiled to 28 pages;
the current 31 October source has not been repackaged.

## Release helpers

- The last review package is `dist/seam-conformance-kit-20261027-review.zip`
  (27 October; historical). It predates the 31 October review-correction pass;
  no new package has been generated.
- The last arXiv package is
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip` (26 October; historical),
  160,358 bytes, SHA-256
  `615962B8590C830E92625EED88F40D42F3D6C1F4A8031B6975599A95192C030A`.
  It predates the 31 October rebuild and was not regenerated.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files and remains the stale 21 October tree, not a public-release
  candidate.

## 31 October review-correction pass

- The manuscript was re-centered on E1, the method, the field-level failure map,
  and the repair taxonomy after the five-seat review.
- H3, H6, and ★ are `REFINED`; H1's resource clause is `UNTESTED`; H4 and H7
  remain `UNTESTED`.
- Canonical, standalone, and arXiv builds regenerated: 29, 29, and 32 pages;
  0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- `python scripts/verify_artifacts.py`: 319 files, all hashes match.
- `python -m pytest -q qa`: 15 passed.
- `python -m pytest -q qa/test_arxiv_build.py`: 6 passed.
- TraceGrant Task D suite: 52 passed.

## 28 October path-format and disclosure revision (historical)

- Section 3.7 now limits AI-use disclosure to experiment implementation,
  artifact quality assurance, and the documented review passes; it no longer
  claims AI-assisted drafting throughout the work. No new claim, experiment, or
  reference was added.
- The build header now forces upright `\texttt` and `\path` rendering, so code
  and paths inside notes are upright monospace rather than italic monospace.
  All three PDFs were checked for `LMMono*-Italic` spans: zero remain.
- The artifact-root key is defined once in Section 3.5, and Table 12 and the
  Appendix cross-reference it. Long path parentheticals were shortened, and
  italic note lead-ins became bold run-in labels.
- The revision changed no claims, numbers, experiments, references, table data,
  or H4/H7 status. At that revision the abstract remained 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.

## Notes

- The 23 October canonical PDF and standalone export remain archived; the
  31 October build supersedes the 26 October and 28 October builds and does not
  overwrite the 23 October files.
- The revision pass changed no claims, experiments, references, or H4/H7
  status. H4 and H7 remain `UNTESTED`.
- The repository is private; arXiv endorsement, license, public email,
  repository URL, archival DOI, and release sanitization remain owner
  decisions.
