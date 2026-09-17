from __future__ import annotations

from pydantic import BaseModel, Field


class MatchEvidence(BaseModel):
    skill: str
    status: str
    confidence: str
    jd_evidence: str
    resume_evidence: str
    source_section: str | None = None
    source_page: int | None = None
    similarity_score: float | None = None


class AnalysisSummary(BaseModel):
    overall_match_percentage: float
    matched_count: int
    partial_count: int
    missing_count: int
    keyword_coverage: float
    experience_coverage: float
    mandatory_coverage: float
    evidence: list[MatchEvidence] = Field(default_factory=list)
