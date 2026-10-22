#!/usr/bin/env python3
"""Build-only wrapper for the live revised manuscript.

The live manuscript already contains the two figure image includes. This
script only:
  - checks the source hash;
  - replaces the H1 title with YAML title/author/date metadata;
  - wraps the Abstract section in a LaTeX abstract environment.

It never writes outside paper/build/.
"""
from pathlib import Path
import hashlib
import sys

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "MANUSCRIPT_REVISED.md"
OUT = HERE / "manuscript_build.md"
EXPECTED_SHA = "6EC07C5A2FBCD423E8BEEA235187366ED74644977E8AE8A4A277FCE577DACC9B"

text = SRC.read_text(encoding="utf-8")
sha = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()
if sha != EXPECTED_SHA:
    sys.exit(f"source hash mismatch: {sha}")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        sys.exit(f"{label}: expected 1 occurrence, found {count}")
    text = text.replace(old, new, 1)


TITLE = (
    "# The Handoff Nobody Owns: Measuring What Cross-Mechanism "
    "Authorization Seams Cannot Carry"
)
replace_once(
    TITLE,
    "---\n"
    'title: "The Handoff Nobody Owns: Measuring What Cross-Mechanism Authorization Seams Cannot Carry"\n'
    'author: "Prathamesh Patil"\n'
    'pdfauthor: "Prathamesh Patil"\n'
    'keywords: "cross-mechanism authorization; agent authorization; authorization seams; scope narrowing; evidence carriage; conformance testing; locked-artifact methodology"\n'
    'date: "23 October 2026"\n'
    "---",
    "title",
)

replace_once(
    "## Abstract",
    "```{=latex}\n\\begin{abstract}\n```",
    "abstract-begin",
)
replace_once(
    "## 1. Introduction",
    "```{=latex}\n\\end{abstract}\n```\n\n## 1. Introduction",
    "abstract-end",
)

OUT.write_text(text, encoding="utf-8")
print(f"wrote {OUT} ({len(text)} chars)")
print("source sha256:", sha)
