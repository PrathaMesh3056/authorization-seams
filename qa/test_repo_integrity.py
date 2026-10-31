"""Repository-level integrity tests.

These tests protect the frozen evidence and the canonical draft. They do not
run the experiments and do not require network access.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

MANUSCRIPT = ROOT / "paper" / "MANUSCRIPT_REVISED.md"
CANONICAL_PDF = ROOT / "paper" / "drafts" / "MANUSCRIPT_DRAFT_2026-10-31.pdf"
LATEX_TEX = ROOT / "paper" / "latex_export" / "main.tex"
LATEX_PDF = ROOT / "paper" / "latex_export" / "main.pdf"

EXPECTED_MANUSCRIPT_SHA = "79CB8E608CD516B18077943E10433A8F22C834B05AD5D19156330B53B258A876"
EXPECTED_PDF_SHA = "F2A3AB17565AF888D23687C5D207DC86C7A6BFE4B58E249608AEF43B607EBE9D"
EXPECTED_TEX_SHA = "0EDEC38B19B0836B5E52B0626C60CECCD7533665CD69BFDB19D5C6CCA468A1BA"
EXPECTED_LATEX_PDF_SHA = "31F45A48ADFD4B0E16EA87727FEB740A22D33A4362C57D6161DF1E46F379E45A"
EXPECTED_ABSTRACT_SHA = "060C2D9F7A78D8E346DC4B8A3BA8278BFD5A34883E6B33CED33CAC90A0D57CD7"
EXPECTED_ABSTRACT_WORDS = 278
EXPECTED_PAGES = 29
EXPECTED_REFERENCE_ENTRIES = 8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def abstract_text() -> str:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    match = re.search(
        r"## Abstract\s*\n\s*\n(.*?)\n\s*\n\*\*Keywords",
        manuscript,
        re.S,
    )
    assert match, "Abstract block not found"
    return match.group(1).strip()


def test_manuscript_hash_is_frozen():
    assert sha256(MANUSCRIPT) == EXPECTED_MANUSCRIPT_SHA


def test_canonical_pdf_hash_is_frozen():
    assert sha256(CANONICAL_PDF) == EXPECTED_PDF_SHA


def test_latex_export_hashes_are_frozen():
    assert sha256(LATEX_TEX) == EXPECTED_TEX_SHA
    assert sha256(LATEX_PDF) == EXPECTED_LATEX_PDF_SHA


def test_abstract_words_and_hash():
    text = abstract_text()
    assert len(text.split()) == EXPECTED_ABSTRACT_WORDS
    assert hashlib.sha256(text.encode("utf-8")).hexdigest().upper() == EXPECTED_ABSTRACT_SHA


def test_canonical_pdf_page_count():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(str(CANONICAL_PDF))
    assert len(reader.pages) == EXPECTED_PAGES


def test_reference_entry_count():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    match = re.search(r"##\s*References\s*\n(.*)$", manuscript, re.S)
    assert match, "References section not found"
    entries = [
        line
        for line in match.group(1).splitlines()
        if line.startswith("**") and not line.startswith("**Reference status")
    ]
    assert len(entries) == EXPECTED_REFERENCE_ENTRIES


def test_h4_and_h7_remain_untested():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert re.search(r"\*\*H4 [-\u2014] `UNTESTED`\.\*\*", manuscript)
    assert re.search(r"\*\*H7 [-\u2014] `UNTESTED`\.\*\*", manuscript)


def test_no_placeholder_email_or_token_material():
    banned = re.compile(
        r"agentscan@gmail\.com|gho_[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|"
        r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    )
    text_suffixes = {
        ".md", ".txt", ".json", ".jsonl", ".py", ".ps1", ".sh", ".cff",
        ".toml", ".yml", ".yaml", ".tex", ".cfg", ".ini", ".csv", ".svg",
    }
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "dist" in path.parts:
            continue
        if path.suffix.lower() not in text_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if banned.search(text):
            hits.append(path.relative_to(ROOT).as_posix())
    assert not hits, f"banned placeholder/token patterns in: {hits}"


def test_verify_artifacts_script_passes():
    result = subprocess.run(
        [sys.executable, "scripts/verify_artifacts.py"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "all hashes match" in result.stdout
