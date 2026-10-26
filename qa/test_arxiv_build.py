"""Checks for the 26 October 2026 arXiv-compliant candidate.

These tests protect the separate 1-inch-margin build. They do not alter the
frozen canonical PDF or the frozen LaTeX export.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARXIV_TEX = ROOT / "paper" / "arxiv_export" / "main.tex"
ARXIV_PDF = ROOT / "paper" / "arxiv_export" / "main.pdf"
ARXIV_METADATA = ROOT / "paper" / "arxiv_export" / "ARXIV_METADATA.md"

EXPECTED_PAGES = 27
EXPECTED_AUTHOR = "Prathamesh N Patil"
EXPECTED_TITLE = (
    "The Handoff Nobody Owns: Measuring What Cross-Mechanism "
    "Authorization Seams Cannot Carry"
)


def test_arxiv_source_is_1in_and_named_author():
    text = ARXIV_TEX.read_text(encoding="utf-8")
    assert r"\usepackage[margin=1in,letterpaper]{geometry}" in text
    assert "0.75in" not in text
    assert f"\\author{{{EXPECTED_AUTHOR}}}" in text
    assert f"pdfauthor={{{EXPECTED_AUTHOR}}}" in text
    assert r"width=\linewidth,height=\textheight,keepaspectratio" in text
    assert "width=7in" not in text


def test_arxiv_source_has_no_identity_or_secret_leak():
    text = ARXIV_TEX.read_text(encoding="utf-8")
    banned = re.compile(
        r"agentscan@gmail\.com|C:\\Users|OneDrive|gho_[A-Za-z0-9]{10,}|"
        r"ghp_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    )
    assert not banned.search(text)


def test_arxiv_pdf_page_count_and_metadata():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(str(ARXIV_PDF))
    assert len(reader.pages) == EXPECTED_PAGES
    assert reader.metadata is not None
    assert reader.metadata.author == EXPECTED_AUTHOR
    assert reader.metadata.title == EXPECTED_TITLE
    for page in reader.pages:
        assert float(page.mediabox.width) == pytest.approx(612.0)
        assert float(page.mediabox.height) == pytest.approx(792.0)


def test_arxiv_pdf_has_no_raster_images():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(str(ARXIV_PDF))
    for page in reader.pages:
        assert len(page.images) == 0


def test_arxiv_pdf_text_contains_title_author_and_untested_hypotheses():
    pypdf = pytest.importorskip("pypdf")
    reader = pypdf.PdfReader(str(ARXIV_PDF))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "The Handoff Nobody Owns" in text
    assert EXPECTED_AUTHOR in text
    assert "H4" in text and "UNTESTED" in text
    assert "H7" in text and "UNTESTED" in text
    assert "agentscan@" not in text


def test_arxiv_metadata_uses_frozen_abstract_hash():
    text = ARXIV_METADATA.read_text(encoding="utf-8")
    assert "CD2278607B491BD49FE7A03585979B259BFD187B0E9C0F9D7D1D4181573B9654" in text
    assert "Abstract word count: 222" in text
    assert "cs.CR" in text
    assert "cs.AI" in text
