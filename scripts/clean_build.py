#!/usr/bin/env python3
"""Remove generated paper-build output, preserving hand-written build files."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "paper" / "build"

KEEP = {
    "README.md",
    "build.ps1",
    "build.sh",
    "preprocess.py",
    "retable.py",
    "fix_texttt.py",
    "header.tex",
}
REMOVE_SUFFIXES = (".aux", ".log", ".out", ".pdf", ".tex", ".png")
REMOVE_PREFIXES = ("manuscript_build",)


def main() -> int:
    removed = 0
    for path in sorted(BUILD.iterdir()) if BUILD.exists() else []:
        if not path.is_file():
            continue
        if path.name in KEEP:
            continue
        if path.name.startswith(REMOVE_PREFIXES) or path.suffix.lower() in REMOVE_SUFFIXES:
            path.unlink()
            removed += 1
            print(f"removed {path.relative_to(ROOT)}")
    print(f"removed {removed} generated files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
