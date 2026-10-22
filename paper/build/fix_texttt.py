#!/usr/bin/env python3
"""Allow line breaks only inside long \\texttt code spans.

Global seqsplit was breaking short status tokens (SUPPORTED -> SUPPOR/TED).
This pass walks balanced braces, wraps only code spans longer than 20
characters, and leaves short tokens unbreakable. It edits the generated .tex,
never the manuscript.
"""
from pathlib import Path
import sys

TEX = Path(__file__).resolve().parent / "manuscript_build_wide.tex"
if not TEX.exists():
    sys.exit(f"missing {TEX}")

text = TEX.read_text(encoding="utf-8")
needle = r"\texttt{"
out = []
pos = 0
wrapped = 0
scanned = 0


def find_close(s: str, open_pos: int) -> int:
    """Return index of the closing brace for the group starting at open_pos."""
    depth = 1
    i = open_pos
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


while True:
    start = text.find(needle, pos)
    if start == -1:
        out.append(text[pos:])
        break
    out.append(text[pos:start])
    open_pos = start + len(needle)
    close_pos = find_close(text, open_pos)
    if close_pos == -1:
        out.append(text[start:])
        break
    content = text[open_pos:close_pos]
    scanned += 1
    looks_like_path = (
        r"\textbackslash{}" in content or "/" in content
    )
    has_space_or_bracket = (
        " " in content
        or r"\ " in content
        or "{[}" in content
        or "{]}" in content
        or "[" in content
        or "]" in content
    )
    if len(content) > 20 and looks_like_path and not has_space_or_bracket:
        # True paths only: use \path, which typesets in typewriter and
        # inserts breakpoints at path separators. Do not route identifiers
        # or code snippets with spaces/brackets here: \path prints Pandoc's
        # {[}/{]} escapes literally and ignores spaces.
        path = content
        path = path.replace(r"\textbackslash{}", "\\")
        path = path.replace(r"\_", "_")
        path = path.replace(r"\ ", " ")
        path = path.replace(r"\%", "%")
        path = path.replace(r"\&", "&")
        path = path.replace(r"\#", "#")
        path = path.replace(r"\$", "$")
        out.append(r"\path{" + path + "}")
        wrapped += 1
    elif len(content) > 20:
        out.append(r"\texttt{" + content + "}")
        wrapped += 1
    else:
        out.append(text[start:close_pos + 1])
    pos = close_pos + 1

text = "".join(out)
# Pandoc's default template adds a table-caption setup even though all table
# captions in this manuscript are ordinary body paragraphs. Remove the unused
# setup so the build log is clean.
text = text.replace("\\captionsetup[table]{skip=6pt}\n", "")
TEX.write_text(text, encoding="utf-8")
print(f"wrapped {wrapped} long code spans out of {scanned} in {TEX}")
