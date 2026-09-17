from __future__ import annotations

from src.config.settings import settings


def semantic_similarity(score: float) -> bool:
    """Return True when a similarity score meets the match threshold."""
    return score >= settings.match_threshold


def related_similarity(score: float) -> bool:
    """Return True when the score is in the partial evidence band."""
    return settings.partial_threshold <= score < settings.match_threshold
