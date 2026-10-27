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
CANONICAL_PDF = ROOT / "paper" / "drafts" / "MANUSCRIPT_DRAFT_2026-10-26.pdf"
LATEX_TEX = ROOT / "paper" / "latex_export" / "main.tex"
LATEX_PDF = ROOT / "paper" / "latex_export" / "main.pdf"

EXPECTED_MANUSCRIPT_SHA = "1732872C36D4AC5EAE349450ACA946120F0EA21A2C48235F58985167A414CCC2"
EXPECTED_PDF_SHA = "B3D39ED0D5F26CB42C1B436D43B9D5FFCC3C6FE613461C860561A0DBEBB788D3"
EXPECTED_TEX_SHA = "4C27CB582582473B961C9DD7E7574D67BD2ECB9C00CA55E6AFDDA493044D8602"
EXPECTED_LATEX_PDF_SHA = "5901ED2B13AC24C9536E41F313BD2A4BBF161F4BDF46E8A9D7D6FC11500492AE"
EXPECTED_ABSTRACT_SHA = "CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654"
EXPECTED_ABSTRACT_WORDS = 222
EXPECTED_PAGES = 25
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
