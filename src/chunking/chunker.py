from __future__ import annotations

from src.config.settings import settings


def chunk_text(text: str, section_name: str = "General") -> list[str]:
    """Segment text into section-aware chunks while preserving sentence flow."""
    segments = [segment.strip() for segment in text.split("\n\n") if segment.strip()]
    chunks: list[str] = []
    for segment in segments:
        if len(segment) <= settings.chunk_size:
            chunks.append(f"[{section_name}]\n{segment}")
            continue

        start = 0
        step = max(settings.chunk_size - settings.chunk_overlap, 1)
        while start < len(segment):
            end = min(start + settings.chunk_size, len(segment))
            chunks.append(f"[{section_name}]\n{segment[start:end]}")
            if end == len(segment):
                break
            start += step
    return chunks
