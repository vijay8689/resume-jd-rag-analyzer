from __future__ import annotations

from pathlib import Path


def extract_txt_text(file_path: str | Path) -> str:
    """Read plain text from a TXT file."""
    return Path(file_path).read_text(encoding="utf-8", errors="replace")
