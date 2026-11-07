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
CANONICAL_PDF = ROOT / "paper" / "drafts" / "MANUSCRIPT_DRAFT_2026-11-07.pdf"
LATEX_TEX = ROOT / "paper" / "latex_export" / "main.tex"
LATEX_PDF = ROOT / "paper" / "latex_export" / "main.pdf"

EXPECTED_MANUSCRIPT_SHA = "117A229932806A7E4D6205581A7E90FC276C838867BEEBFF7F972E561ABF7722"
EXPECTED_PDF_SHA = "D8F80E8B9384BB352C440E48EDB0BD3534CBD38CEEE55D942CF8C8F07D7A348F"
EXPECTED_TEX_SHA = "FC2618112D3CE711FEE9B327665527E66664DFE9FF1D8A21AE96BAD327008F32"
EXPECTED_LATEX_PDF_SHA = "A56FF2B9CEC2EABFC92D0C7ECEBB26FBD7401473BF91FA97074A76989FEF9413"
EXPECTED_ABSTRACT_SHA = "B93412AC45C73A9692F33E6B765959C581231BF93DE65F0D6C2BC8CBC460AF38"
EXPECTED_ABSTRACT_WORDS = 222
EXPECTED_PAGES = 33
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
