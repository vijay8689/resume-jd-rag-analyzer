from __future__ import annotations

from src.matching.exact_matcher import exact_match
from src.matching.semantic_matcher import related_similarity, semantic_similarity


def hybrid_status(skill: str, resume_text: str, similarity_score: float | None) -> str:
    """Determine the status by exact evidence, then semantic evidence."""
    if exact_match(skill, resume_text):
        return "MATCHED"
    if similarity_score is not None and semantic_similarity(similarity_score):
        return "MATCHED"
    if similarity_score is not None and related_similarity(similarity_score):
        return "PARTIAL"
    return "MISSING"
