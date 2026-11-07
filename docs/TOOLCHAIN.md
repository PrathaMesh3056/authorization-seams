# Toolchain - verified 26 Oct 2026; builds refreshed 7 Nov 2026

Local build tools used for the manuscript, figure, and PDF pass. These are
development dependencies only; none is bundled into the paper or artifact
release.

| Tool | Version | Path / notes |
|---|---|---|
| Inkscape | 1.4.4 (dcaf3e7, 2026-05-05) | `C:\Program Files\Inkscape\bin\inkscape.exe` |
| MiKTeX | 25.12 | `C:\Users\prath\AppData\Local\Programs\MiKTeX\miktex\bin\x64` |
| XeLaTeX | 4.16 | `xelatex.exe` in the MiKTeX bin directory |
| PdfLaTeX | 4.23 | `pdflatex.exe` in the MiKTeX bin directory |
| BibTeX | 4.2 | `bibtex.exe` in the MiKTeX bin directory |
| Pandoc | 3.12.1 | `C:\Users\prath\AppData\Local\Pandoc\pandoc.exe` |
| Poppler | 25.07.0 | Local QA only; not part of the paper or release package |
| Python | 3.x | PyMuPDF 1.28.0, pypdf 6.14.2, Pillow 12.1.0 |

## Commands

### Manuscript build

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File paper\build\build.ps1
```

The script runs `preprocess.py` (source hash check and YAML metadata),
`retable.py` (pipe-table normalization), Pandoc, `fix_texttt.py` (selective
long-path wrapping), and XeLaTeX three times. It writes
`paper\build\manuscript_build_wide.pdf`.

### Standalone export

```powershell
cd paper\latex_export
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The export directory contains `main.tex`, `figures/`, `main.pdf`, and
`README.md`.

### arXiv candidate

```powershell
python paper\build\build_arxiv.py
```

The script verifies the pinned LaTeX export hash and the unified author name,
applies the 1-inch margin and Figure 2 width changes, and compiles three times.
It writes `paper\arxiv_export\main.tex` and `paper\arxiv_export\main.pdf`
(37 pages, 0 missing glyphs, 0 fatal LaTeX errors, 0 overfull hboxes; 4 cosmetic
underfull hboxes and 1 stable label warning). See `docs\ARXIV_BUILD_QA.md`.

### Figure conversion

```powershell
powershell -ExecutionPolicy Bypass -File paper\convert_figures.ps1
```

The script calls Inkscape with `--export-area-page`, then checks `pdffonts`,
`pdfimages -list`, and `pdftotext`.

### Figure PDF QA

```powershell
python paper\qa_pdf.py
```

Renders 300-dpi previews under `paper\figures\pdf_preview\` and prints
font/image/text checks. Poppler is used locally for QA only.

## TeX notes

- `latexmk` is not usable out of the box because MiKTeX cannot find Perl. Use
  `xelatex` directly or install Perl if a later build requires `latexmk`.
- `xelatex` with `fontspec` + `unicode-math` works. The body `★` is mapped to
  the Latin Modern Math `\star` glyph; do not reintroduce a Segoe UI Symbol
  fallback.
- Figure labels use Arial; the subset glyph is explicitly set in Cambria Math.
  No Lucida Sans Unicode or Segoe UI Symbol fallback remains.
- The current canonical build produces 33 pages, 360,634 bytes, 0 missing
  glyphs, 0 fatal LaTeX errors, 0 overfull hboxes, 6 cosmetic underfull hboxes,
  and 6 ignored infinite-glue-shrinkage diagnostics. References are a static
  bracketed list embedded by Pandoc; no citeproc or BibTeX run is used.
- One stable `Label(s) may have changed` warning remains after the three-pass
  build. It is not an unresolved-reference warning and is documented as a
  build-tooling artifact.

## Licensing note

Inkscape, MiKTeX, Pandoc, and Poppler are separate open-source tools. They are
not redistributed with the paper or artifact kit. The paper's license and the
kit's license remain separate decisions.
