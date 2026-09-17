from __future__ import annotations

from pathlib import Path
from typing import Any

import fitz


def extract_pdf_text(file_path: str | Path) -> str:
    """Extract text from a PDF file and keep page boundaries."""
    doc = fitz.open(file_path)
    sections: list[str] = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text()
        if text.strip():
            sections.append(f"## PAGE {page_index + 1}\n{text}")
    doc.close()
    return "\n\n".join(sections)


def get_pdf_metadata(file_path: str | Path) -> dict[str, Any]:
    """Return simple PDF metadata for the UI."""
    doc = fitz.open(file_path)
    result = {"pages": len(doc), "file_type": "PDF"}
    doc.close()
    return result
