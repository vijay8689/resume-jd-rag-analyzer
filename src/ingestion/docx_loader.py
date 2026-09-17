from __future__ import annotations

from pathlib import Path

from docx import Document


def extract_docx_text(file_path: str | Path) -> str:
    """Extract paragraph text from a DOCX document."""
    document = Document(str(file_path))
    paragraphs: list[str] = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)
