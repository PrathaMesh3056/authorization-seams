#!/usr/bin/env bash
# Build the single-column arXiv-style draft with Pandoc + XeLaTeX.
# Run from anywhere; paths are resolved relative to this script.
# Requires: Pandoc 3.12+, python3, and xelatex on PATH.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
paper="$(dirname "$here")"
cd "$paper"

command -v pandoc >/dev/null 2>&1 || { echo "pandoc not found on PATH" >&2; exit 1; }
command -v xelatex >/dev/null 2>&1 || { echo "xelatex not found on PATH" >&2; exit 1; }

python3 "$here/preprocess.py"
python3 "$here/retable.py"

pandoc "$here/manuscript_build_wide.md" -f markdown -t latex -s \
  --shift-heading-level-by=-1 \
  "--include-in-header=$here/header.tex" \
  -V geometry:margin=0.75in -V geometry:letterpaper -V fontsize=10pt \
  -o "$here/manuscript_build_wide.tex"

python3 "$here/fix_texttt.py"

rm -f "$here/manuscript_build_wide.aux" "$here/manuscript_build_wide.out"
for pass in 1 2 3; do
  xelatex -interaction=nonstopmode -halt-on-error \
    "-output-directory=$here" "$here/manuscript_build_wide.tex" \
    > "$here/xelatex_console.log" 2>&1 || {
      echo "xelatex pass $pass failed; see $here/xelatex_console.log" >&2
      exit 1
    }
done

pdf="$here/manuscript_build_wide.pdf"
log="$here/manuscript_build_wide.log"
[ -f "$pdf" ] || { echo "PDF not produced: $pdf" >&2; exit 1; }

echo "PDF: $pdf"
echo "Missing glyphs: $(grep -c 'Missing character' "$log" || true)"
echo "Overfull hboxes: $(grep -c 'Overfull \\hbox' "$log" || true)"
echo "Underfull hboxes: $(grep -c 'Underfull \\hbox' "$log" || true)"
echo "LaTeX errors: $(grep -Ec '^!|LaTeX Error|Fatal error' "$log" || true)"
echo "Label-changed warnings: $(grep -c 'Label(s) may have changed' "$log" || true)"
