from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeChunk(BaseModel):
    chunk_id: str
    document_id: str
    session_id: str
    text: str
    section: str | None = None
    page: int | None = None


class JobRequirement(BaseModel):
    skill: str
    category: str
    priority: str
    required_experience: float | None = None
    source_text: str


class SkillMatch(BaseModel):
    skill: str
    category: str
    priority: str
    status: str
    confidence: str
    similarity_score: float | None = None
    jd_evidence: str
    resume_evidence: str
    required_experience: float | None = None
    resume_experience: float | None = None
    experience_status: str = "NOT_SPECIFIED"


class AnalysisResult(BaseModel):
    overall_match_percentage: float
    matched_percentage: float
    partial_percentage: float
    missing_percentage: float
    keyword_match_percentage: float
    mandatory_skill_percentage: float
    experience_match_percentage: float
    matched_skills: list[SkillMatch] = Field(default_factory=list)
    partial_skills: list[SkillMatch] = Field(default_factory=list)
    missing_skills: list[SkillMatch] = Field(default_factory=list)
    present_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    related_keywords: list[str] = Field(default_factory=list)
    learning_resources: dict = Field(default_factory=dict)
    resume_suggestions: list[str] = Field(default_factory=list)
