from __future__ import annotations

from pydantic import BaseModel, Field


class JDMetadata(BaseModel):
    job_title: str | None = None
    company: str | None = None
    location: str | None = None
    experience_requirement: str | None = None


class JDAnalysis(BaseModel):
    requirements: list = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    metadata: JDMetadata = JDMetadata()
