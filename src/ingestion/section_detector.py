from __future__ import annotations

from src.ingestion.document_processor import detect_sections


def detect_resume_sections(text: str):
    """Public helper to detect sections in resume text."""
    return detect_sections(text)
