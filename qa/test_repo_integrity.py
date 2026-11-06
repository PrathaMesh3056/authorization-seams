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
CANONICAL_PDF = ROOT / "paper" / "drafts" / "MANUSCRIPT_DRAFT_2026-11-06.pdf"
LATEX_TEX = ROOT / "paper" / "latex_export" / "main.tex"
LATEX_PDF = ROOT / "paper" / "latex_export" / "main.pdf"

EXPECTED_MANUSCRIPT_SHA = "76E9E8F6F7233121277B97C0363DF38AC05284F71CD52D26E33D6A8E098B1A98"
EXPECTED_PDF_SHA = "08752FEED7AA766DA8D4ABDF7FCBDD7907F35A6C53D2E235D57C0A8B6B51C256"
EXPECTED_TEX_SHA = "C4BBBD28A189E8ED461CD0E246FA2E7B3054D3ED7B1765DC270C47EF800B5139"
EXPECTED_LATEX_PDF_SHA = "F13D7EA29D4136101CFA44D07F31A1F4C56B09F05AC48CE0E7122AC06FCDB7BC"
EXPECTED_ABSTRACT_SHA = "35C17A00CBB3A15B5C67298F45E37FE7D663275A65A1CB38DA78BB84FDF89F45"
EXPECTED_ABSTRACT_WORDS = 222
EXPECTED_PAGES = 32
EXPECTED_REFERENCE_ENTRIES = 21


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
    assert "**H4/H7 gate.**" in manuscript


def test_required_declarations_present():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "## Declarations" in manuscript
    for heading in (
        "**Data availability.**",
        "**Ethics.**",
        "**Author contributions (CRediT).**",
        "**Competing interests.**",
        "**Funding.**",
        "**Limitations.**",
    ):
        assert heading in manuscript


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
