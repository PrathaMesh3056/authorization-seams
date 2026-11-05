# Paper build

Pandoc converts `../MANUSCRIPT_REVISED.md` into LaTeX; XeLaTeX compiles it
three times to converge labels. All output stays in this directory and is
generated, not tracked.

## Files

| File | Purpose |
|---|---|
| `build.ps1` | Windows build (Pandoc + XeLaTeX from PATH) |
| `build.sh` | POSIX build |
| `build_arxiv.py` | Builds the 34-page arXiv candidate with 1-inch margins from the frozen LaTeX export |
| `preprocess.py` | Hash-checks the manuscript and adds YAML metadata + abstract env |
| `retable.py` | Rewrites pipe-table separator widths; formatting only |
| `header.tex` | Build preamble; not part of the manuscript |
| `fix_texttt.py` | Wraps long code spans after Pandoc; never edits the manuscript |

## Expected result

- `manuscript_build_wide.pdf`: 31 pages.
- Build log: zero missing glyphs, zero fatal LaTeX errors, zero overfull
  hboxes, and four ignored infinite-glue-shrinkage diagnostics.
- Three underfull hboxes and one `Label(s) may have changed` warning are
  expected and cosmetic.
- `build_arxiv.py` writes `paper/arxiv_export/main.pdf`: 34 pages, 1-inch
  margins, zero missing glyphs, zero fatal LaTeX errors, zero overfull hboxes,
  four cosmetic underfull hboxes, and one stable label warning.

## Version notes

The reference build used Pandoc 3.12.1 and MiKTeX 25.12 (XeLaTeX). Older
Pandoc releases may render tables differently. `docs/TOOLCHAIN.md` records the
verified toolchain.

## Rule

Never edit `../MANUSCRIPT_REVISED.md` to make a build pass. If a source hash
mismatches, stop and open a revision record.
