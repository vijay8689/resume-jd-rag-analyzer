from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SECTION_KEYWORDS = {
    "Professional Summary": ["professional summary", "summary", "profile"],
    "Technical Skills": ["technical skills", "skills", "core competencies", "tools", "technologies"],
    "Professional Experience": ["professional experience", "work experience", "experience"],
    "Projects": ["projects", "selected projects"],
    "Education": ["education", "academic background"],
    "Certifications": ["certifications", "licenses"],
    "Achievements": ["achievements", "awards"],
    "Responsibilities": ["responsibilities", "key responsibilities"],
}


def clean_text(raw_text: str) -> str:
    """Normalize text while preserving technical content and years."""
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("•", "- ").replace("·", "- ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n +", "\n", text)
    return text.strip()


def detect_sections(text: str) -> list[dict[str, Any]]:
    """Return likely section headers in the document."""
    matches: list[dict[str, Any]] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned:
            continue
        for section, keywords in SECTION_KEYWORDS.items():
            lower = cleaned.lower()
            if any(keyword in lower for keyword in keywords):
                matches.append({"section": section, "line": idx, "title": cleaned})
                break
    return matches


def extract_text_from_file(file_kind: str, file_path: str | Path) -> str:
    """Load text from a supported resume file type."""
    if file_kind == "pdf":
        from src.ingestion.pdf_loader import extract_pdf_text

        return extract_pdf_text(file_path)
    if file_kind == "docx":
        from src.ingestion.docx_loader import extract_docx_text

        return extract_docx_text(file_path)
    if file_kind == "txt":
        from src.ingestion.txt_loader import extract_txt_text

        return extract_txt_text(file_path)
    raise ValueError(f"Unsupported file type: {file_kind}")
