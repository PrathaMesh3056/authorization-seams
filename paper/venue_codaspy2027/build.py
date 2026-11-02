#!/usr/bin/env python3
"""Build and QA the CODASPY 2027 venue cut.

Usage:
    python build.py              # build with xelatex/bibtex, then run checks
    python build.py --skip-build # check the existing main.pdf only

The script fails (exit 1) on page-budget, layout, anonymity, or frozen-claim
regressions. It never touches the canonical preprint or the arXiv export.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN_TEX = ROOT / "main.tex"
MAIN_PDF = ROOT / "main.pdf"
MAIN_LOG = ROOT / "main.log"
MAIN_BLG = ROOT / "main.blg"
MAIN_BBL = ROOT / "main.bbl"

MAIN_PAGE_LIMIT = 12
APPENDIX_PAGE_LIMIT = 2
EXPECTED_REFERENCES = 16

# Frozen claim strings that must survive every venue edit. whitespace-normalised
# page text is matched, so line breaks inside the PDF do not matter.
CLAIM_PATTERNS = {
    "execution ledger": r"2,446\s*=\s*560\s*\+\s*40\s*\+\s*6\s*\+\s*16\s*\+\s*672\s*\+\s*1,152",
    "Pilot-1 leak cases": r"24/40",
    "Pilot-1 effect events": r"26 unauthorized-effect events",
    "Pilot-1 novelty zero": r"0/40 receiver-relative novelty",
    "SA leak cases": r"28/48",
    "SA effect events": r"30 unauthorized-effect events",
    "SA novelty zero": r"0/48 receiver-relative novelty",
    "E1 family-wide": r"0/4 under the frozen family-wide",
    "E1 arm-native": r"4/4 under the arm-native",
    "boundary split": r"32\s*=\s*28\s*\+\s*4",
    "boundary effect events": r"34 unauthorized-effect events",
    "fail-closed benign denials": r"20 benign false denials",
}

FORBIDDEN_TEXT = (
    "Prathamesh",
    "prathamesh",
    "Sardar Patel",
    "spit.ac.in",
    "OneDrive",
    "C:\\Users",
    "github.com/",
    "RPaper",
)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


class Checks:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if condition:
            print(f"PASS  {message}")
        else:
            print(f"FAIL  {message}")
            self.failures.append(message)

    def note(self, message: str) -> None:
        print(f"INFO  {message}")
        self.notes.append(message)


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-40:])
        print(tail)
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(command)}")


def build() -> None:
    for generated in ("main.aux", "main.bbl", "main.blg", "main.out"):
        path = ROOT / generated
        if path.exists():
            path.unlink()
    xelatex = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    run(xelatex)
    run(["bibtex", "main"])
    run(xelatex)
    run(xelatex)


def normalise(text: str) -> str:
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text).strip()


def read_pages() -> tuple[list[str], list[str], object]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit("pypdf is required for QA checks: python -m pip install pypdf") from exc

    reader = PdfReader(str(MAIN_PDF))
    raw = [(page.extract_text() or "") for page in reader.pages]
    return raw, [normalise(page) for page in raw], reader


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def check() -> int:
    checks = Checks()

    if not MAIN_PDF.exists():
        raise SystemExit(f"missing {MAIN_PDF}; run without --skip-build first")

    raw_pages, pages, reader = read_pages()
    total_pages = len(pages)
    joined = normalise(" ".join(pages))

    # ---- Page budget -----------------------------------------------------
    appendix_index = next(
        (i for i, page in enumerate(pages) if "hypothesis lineage and detailed tables" in page.lower()),
        None,
    )
    checks.require(appendix_index is not None, "appendix opening page found")
    if appendix_index is None:
        return 1

    appendix_start = appendix_index + 1  # 1-based
    main_pages = appendix_start - 1
    appendix_pages = total_pages - main_pages
    checks.note(f"total pages: {total_pages}")
    checks.note(f"main body + references: pages 1-{main_pages}")
    checks.note(f"appendix: pages {appendix_start}-{total_pages}")
    checks.require(
        main_pages <= MAIN_PAGE_LIMIT,
        f"main body + references within {MAIN_PAGE_LIMIT} pages (got {main_pages})",
    )
    checks.require(
        appendix_pages <= APPENDIX_PAGE_LIMIT,
        f"appendix within {APPENDIX_PAGE_LIMIT} pages (got {appendix_pages})",
    )
    checks.require(
        any("references" in page.lower() for page in pages[:main_pages]),
        "references section is inside the main page budget",
    )

    # ---- Layout ----------------------------------------------------------
    log = MAIN_LOG.read_text(encoding="utf-8", errors="replace") if MAIN_LOG.exists() else ""
    overfull_h = count(r"Overfull \\hbox", log)
    overfull_v = count(r"Overfull \\vbox", log)
    underfull_h = count(r"Underfull \\hbox", log)
    underfull_v = count(r"Underfull \\vbox", log)
    undefined_refs = count(r"LaTeX Warning: Reference .* undefined", log)
    undefined_cites = count(r"LaTeX Warning: Citation .* undefined", log)
    missing_chars = count(r"Missing character", log)
    font_warnings = count(r"LaTeX Font Warning", log)
    latex_warnings = count(r"(?<!Package )LaTeX Warning", log)
    acmart_warnings = count(r"Class acmart Warning", log)

    checks.require(overfull_h == 0, f"no overfull hboxes (got {overfull_h})")
    checks.require(overfull_v == 0, f"no overfull vboxes (got {overfull_v})")
    checks.require(undefined_refs == 0, f"no undefined references (got {undefined_refs})")
    checks.require(undefined_cites == 0, f"no undefined citations (got {undefined_cites})")
    checks.require(missing_chars == 0, f"no missing characters (got {missing_chars})")
    checks.require(font_warnings == 0, f"no font warnings (got {font_warnings})")
    checks.require(latex_warnings == 0, f"no LaTeX warnings (got {latex_warnings})")
    checks.require(acmart_warnings == 0, f"no acmart warnings (got {acmart_warnings})")
    checks.note(f"underfull hboxes: {underfull_h} (cosmetic justification, tolerated)")
    checks.note(f"underfull vboxes: {underfull_v} (cosmetic page fill, tolerated)")

    if MAIN_BLG.exists():
        blg = MAIN_BLG.read_text(encoding="utf-8", errors="replace")
        bibtex_warnings = count(r"(?m)^Warning--", blg)
        checks.note(f"BibTeX warnings: {bibtex_warnings} (metadata completeness, reviewed)")

    # ---- Bibliography ----------------------------------------------------
    if MAIN_BBL.exists():
        bbl = MAIN_BBL.read_text(encoding="utf-8", errors="replace")
        references = len(re.findall(r"\\bibitem", bbl))
    else:
        references = 0
    checks.require(
        references == EXPECTED_REFERENCES,
        f"bibliography has {EXPECTED_REFERENCES} entries (got {references})",
    )

    # ---- Anonymity -------------------------------------------------------
    checks.require("Anonymous Author(s)" in joined, "anonymous author block present")
    leaks = [token for token in FORBIDDEN_TEXT if token.lower() in joined.lower()]
    checks.require(not leaks, f"no author/affiliation/path tokens in body (found: {leaks})")
    emails = sorted(set(EMAIL_RE.findall(joined)))
    unexpected = [e for e in emails if not e.lower().endswith(("@example.test", "@example.com"))]
    checks.require(not unexpected, f"no unexpected email addresses (found: {unexpected})")
    if emails:
        checks.note(f"allowed synthetic emails: {', '.join(emails)}")

    metadata_author = ""
    if reader.metadata is not None:
        metadata_author = (reader.metadata.author or "").strip()
    checks.require(not metadata_author, f"PDF metadata author is blank (got: {metadata_author!r})")

    # ---- Frozen claims ---------------------------------------------------
    for name, pattern in CLAIM_PATTERNS.items():
        found = count(pattern, joined)
        checks.require(found > 0, f"frozen claim present: {name}")

    checks.require(
        count(r"H4[^.]{0,120}UNTESTED", joined) > 0,
        "H4 remains UNTESTED",
    )
    checks.require(
        count(r"H7[^.]{0,120}UNTESTED", joined) > 0,
        "H7 remains UNTESTED",
    )
    placeholders = count(r"TODO|XXX|PLACEHOLDER|TBD", joined)
    checks.require(placeholders == 0, f"no placeholders (got {placeholders})")

    # ---- Summary ---------------------------------------------------------
    print()
    if checks.failures:
        print(f"FAILED: {len(checks.failures)} check(s)")
        for failure in checks.failures:
            print(f"  - {failure}")
        return 1
    print(f"PASS: all venue checks satisfied ({total_pages} pages; {main_pages} main + {appendix_pages} appendix)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-build", action="store_true", help="check the existing main.pdf")
    args = parser.parse_args()

    if not args.skip_build:
        build()
    return check()


if __name__ == "__main__":
    sys.exit(main())
