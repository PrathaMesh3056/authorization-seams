#!/usr/bin/env python3
"""Rewrite pipe-table separator lines with explicit relative widths.

Formatting-only experiment on the build copy: no cell text changes.
Widths are fractions of \\linewidth; Pandoc normalizes dash counts.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
src = HERE / "manuscript_build.md"
out = HERE / "manuscript_build_wide.md"

WIDTHS = {
    6:  [0.24] + [0.1086] * 7,                                  # Table 5
    9:  [0.20] + [0.06] * 10 + [0.10, 0.10],                   # Table 8 (13 cols)
    10: [0.16, 0.10, 0.185, 0.185, 0.185, 0.185],               # Table 9
    11: [0.30, 0.14, 0.14, 0.14, 0.14, 0.14],                   # Table 10
    12: [0.08, 0.10, 0.70, 0.12],                               # Table 11
    13: [0.20, 0.08, 0.24, 0.24, 0.24],                         # Table 12
    14: [0.09, 0.13, 0.27, 0.12, 0.14, 0.13, 0.12],             # Table 13
    15: [0.21, 0.12, 0.17, 0.50],                               # Table 14
    16: [0.16, 0.34, 0.50],                                     # Table 15
    19: [0.18, 0.34, 0.18, 0.30],                               # Table A1 (appendix)
}

text = src.read_text(encoding="utf-8")
lines = text.split("\n")

# locate table blocks: header line + separator line
block = -1
i = 0
changed = []
while i < len(lines) - 1:
    if (lines[i].lstrip().startswith("|") and i + 1 < len(lines)
            and lines[i + 1].strip() and set(lines[i + 1].strip()) <= set("|-: ")):
        block += 1
        if block in WIDTHS:
            cells = [c for c in lines[i].strip().strip("|").split("|")]
            widths = WIDTHS[block]
            if len(cells) != len(widths):
                sys.exit(f"block {block}: {len(cells)} columns but {len(widths)} widths")
            sep = []
            for cell, w in zip(cells, widths):
                n = max(3, round(w * 100))
                align = ":" if cell.strip().startswith(":") and cell.strip().endswith(":") else (
                    ":" if cell.strip().endswith(":") else "")
                sep.append("-" * n + align if False else "-" * n)
            new = "|" + "|".join(sep) + "|"
            changed.append((block, len(cells), lines[i + 1][:60], new[:80]))
            lines[i + 1] = new
    i += 1

out.write_text("\n".join(lines), encoding="utf-8")
print(f"rewrote {len(changed)} separator lines -> {out}")
for b, n, old, new in changed:
    print(f"  block {b} ({n} cols): {new[:70]}...")


