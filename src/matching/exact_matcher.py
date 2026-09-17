from __future__ import annotations


def exact_match(skill: str, resume_text: str) -> bool:
    """Return True when a skill is explicitly present in the resume text."""
    return skill.lower() in resume_text.lower()


def exact_match_skills(skills: list[str], resume_text: str) -> list[str]:
    """Return the subset of skills that match exactly."""
    return [skill for skill in skills if exact_match(skill, resume_text)]
