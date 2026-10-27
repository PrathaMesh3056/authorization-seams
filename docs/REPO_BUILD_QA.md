# Repository build and QA record - 28 October 2026

Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This is a local
validation record. The repository has a private `origin` remote and the current
state is pushed to `origin/main`; no public release has occurred.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (working copy; `RPaper` archive untouched) |
| Local branch | `main` |
| Tracked files | 312 |
| Tracked bytes | 17,427,579 |
| Remote | private `origin` |
| Canonical PDF | `paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf` |
| Canonical PDF SHA-256 | `BC6AB2C5A82654D7FC3831AE4B7CEA66EE4A4C38A5ABF5924BC8EC65F236C544` |
| arXiv candidate | `paper/arxiv_export/main.pdf` |
| arXiv PDF SHA-256 | `7B8E8E7B6E167C9E4523BBA2B1F6F752F04FBA5FFA64D254E54AC5CAB4986165` |

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
`paper/drafts/MANUSCRIPT_DRAFT_2026-10-26.pdf`, 321,990 bytes, SHA-256
`BC6AB2C5A82654D7FC3831AE4B7CEA66EE4A4C38A5ABF5924BC8EC65F236C544`.

Standalone export:

- `paper/latex_export/main.tex` SHA-256
  `ED7970DFA49DB36B3759B3ED59700679C81EED91BFA326723503C5670E9A8515`;
- `paper/latex_export/main.pdf` 25 pages, 321,988 bytes, SHA-256
  `9B569A258F2510DC0823BDB839FFE9511CE4DE34171E5670EF30D35A17E20B7D`;
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
  `FCA5B98B2C209BA72EC8FFEBDE792FFB450C48660D1E6C7A999B81E4D467C007`;
- 323,573-byte PDF with SHA-256
  `7B8E8E7B6E167C9E4523BBA2B1F6F752F04FBA5FFA64D254E54AC5CAB4986165`.

The extracted arXiv source package compiles to 28 pages with 0 missing glyphs,
0 fatal errors, 0 overfull hboxes, 4 underfull hboxes, 3 ignored infinite-glue
diagnostics, and 1 stable label warning.

## Release helpers

- Review package: `dist/seam-conformance-kit-20261027-review.zip`; regenerated
  from the final manifest. It extracts, verifies the tracked files, passes the
  repository QA suite, and rebuilds the 28-page arXiv candidate. The checksum is
  in the adjacent `.sha256` sidecar.
- arXiv package:
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip`, 160,352 bytes,
  SHA-256 `61DC9672548878E450638DC969B07EAEE0D1BD0D35B3FE1C1ADC3B4CF2BB33DA`;
  contains `main.tex` and the two vector figures.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files and remains the stale 21 October tree, not a public-release
  candidate.

## 28 October path-format correction

- The build header now forces upright `\texttt` and `\path` rendering, so code
  and paths inside notes are upright monospace rather than italic monospace.
  All three PDFs were checked for `LMMono*-Italic` spans: zero remain.
- The artifact-root key is defined once in Section 3.5, and Table 12 and the
  Appendix cross-reference it. Long path parentheticals were shortened, and
  italic note lead-ins became bold run-in labels.
- The correction changed no claims, numbers, experiments, references, table
  data, or H4/H7 status. The abstract remains 222 words with SHA-256
  `CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654`.

## Notes

- The 23 October canonical PDF and standalone export remain archived; the
  26 October build was refreshed in place on 28 October and does not overwrite
  the 23 October files.
- The correction pass changed no claims, experiments, references, or H4/H7
  status. H4 and H7 remain `UNTESTED`.
- The repository is private; arXiv endorsement, license, public email,
  repository URL, archival DOI, and release sanitization remain owner
  decisions.
