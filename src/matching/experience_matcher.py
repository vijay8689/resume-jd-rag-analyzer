from __future__ import annotations

import re


def extract_resume_experience(text: str, skill: str) -> float | None:
    """Find an explicit skill-duration pair in the resume text."""
    pattern = rf"({re.escape(skill)}.*?(\d+(?:\.\d+)?)\s*years?)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return float(match.group(2))
    return None


def compare_experience(required_years: float | None, resume_years: float | None) -> str:
    """Compare skill experience requirements and resume experience."""
    if required_years is None:
        return "NOT_REQUIRED"
    if resume_years is None:
        return "NOT_SPECIFIED"
    if resume_years >= required_years:
        return "MEETS_REQUIREMENT"
    return "BELOW_REQUIREMENT"
