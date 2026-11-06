# Repository build and QA record - 5 November 2026

Windows (Python 3.12.7, Pandoc 3.12.1, MiKTeX 25.12 XeLaTeX). This is a local
validation record. The repository has a private `origin` remote; local `main`
is ahead of `origin/main` and has not been pushed. No public release has
occurred.

## Snapshot

| Item | Value |
|---|---|
| Local repository | `RPaper-repo` (working copy; `RPaper` archive untouched) |
| Local branch | `main` |
| Tracked files | 331 |
| Manifest coverage | 320 selected files; see `artifacts/manifest.json` |
| Remote | private `origin` |
| Canonical PDF | `paper/drafts/MANUSCRIPT_DRAFT_2026-11-05.pdf` |
| Canonical PDF SHA-256 | `7CF87221C4DA167074893FBCCA90EE236577C4BCAAD85DF3BCB50DFE7944815F` |
| arXiv candidate | `paper/arxiv_export/main.pdf` |
| arXiv PDF SHA-256 | `C67939B0F2F4F9E6F4E2A59953CB45FC838A101FF8AC2811A53E44B0DD09AF28` |

## Integrity

| Check | Result |
|---|---|
| `python scripts/verify_artifacts.py` | 320 selected files match; no missing or unexpected files |
| `python -m pytest -q qa` | 16 passed |
| TraceGrant Task D tests (`cd tests/tracegrant_task_d_20261014 && python -m pytest -q tests`) | 52 passed |
| E1 lock check (`run_extension_e1.py --check`) | dataset/lock SHA match, OK |
| SentinelAgent check (`run_sa.py --check`) | 672 rows, upstream and lock hashes match, OK |
| Boundary check (`run_boundary.py --check`) | 1,152 rows, harness and case hashes match, OK |

## Paper build

`paper/build/build.ps1` completed:

- 31 pages;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 3 cosmetic underfull hboxes;
- 7 ignored infinite-glue-shrinkage diagnostics;
- 1 stable `Label(s) may have changed` warning.

Canonical PDF:
`paper/drafts/MANUSCRIPT_DRAFT_2026-11-05.pdf`, 348,663 bytes, SHA-256
`7CF87221C4DA167074893FBCCA90EE236577C4BCAAD85DF3BCB50DFE7944815F`.

Standalone export:

- `paper/latex_export/main.tex` SHA-256
  `6E17B5407C9BEC96F69BF011ED535014024C7BF89A1CAD2688FD7628016AECD8`;
- `paper/latex_export/main.pdf` 31 pages, 348,668 bytes, SHA-256
  `11FB860DF6398176735174B91F05C7C834F90523D1E77981ED3347F228D455E3`;
- independent XeLaTeX compile: 0 fatal errors, 0 overfull hboxes, 3 underfull
  hboxes, and 1 stable label warning.

## arXiv candidate

`python paper/build/build_arxiv.py` completed:

- 34 pages, US Letter, 10 pt, 1-inch margins;
- 0 missing glyphs;
- 0 fatal LaTeX errors;
- 0 overfull hboxes;
- 4 cosmetic underfull hboxes;
- 1 stable label warning;
- source SHA-256
  `B803242D7A54C6260CE94A0D638384E053B3BF95D17B981198E1612AA42A9AA2`;
- 351,679-byte PDF with SHA-256
  `C67939B0F2F4F9E6F4E2A59953CB45FC838A101FF8AC2811A53E44B0DD09AF28`.

The last generated source package (26 October; historical) compiled to 28 pages;
the current 5 November source has not been repackaged.

## Release helpers

- The last review package is `dist/seam-conformance-kit-20261027-review.zip`
  (27 October; historical). It predates the 31 October review-correction pass
  and the 5 November declarations revision; no new package has been generated.
- The last arXiv package is
  `dist/arxiv/authorization-seams-arxiv-2026-10-26.zip` (26 October; historical),
  160,358 bytes, SHA-256
  `615962B8590C830E92625EED88F40D42F3D6C1F4A8031B6975599A95192C030A`.
  It predates the 31 October and 5 November rebuilds and was not regenerated.
- `dist/sanitized` was not regenerated or edited; it verifies independently at
  298 files and remains the stale 21 October tree, not a public-release
  candidate.

## 5 November declarations and positioning revision

- Abstract trimmed to 222 words; Declarations, falsification/stop conditions,
  H4/H7 gate, three adjacent pointers, Appendix Table A2, and E1 8/8
  `report-only` qualifiers applied.
- References: 11 entries. H4 and H7 remain `UNTESTED`.
- Canonical, standalone, and arXiv builds regenerated: 31, 31, and 34 pages;
  0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes.
- `python scripts/verify_artifacts.py`: 320 files, all hashes match.
- `python -m pytest -q qa`: 16 passed.
- `python -m pytest -q qa/test_arxiv_build.py`: 6 passed.
- TraceGrant Task D suite: 52 passed.

## 31 October review-correction pass (historical)

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

- The 23 October, 31 October, and 5 November canonical PDFs and standalone
  exports are archived; the 5 November build supersedes the earlier builds and
  does not overwrite them.
- The revision pass changed no claims, experiments, references, or H4/H7
  status beyond the additions listed above. H4 and H7 remain `UNTESTED`.
- The repository is private; arXiv endorsement, license, public email,
  repository URL, archival DOI, and release sanitization remain owner
  decisions.
