from __future__ import annotations

import re

from src.jd.keyword_extractor import extract_keywords
from src.jd.requirement_classifier import classify_requirement, extract_experience_requirement
from src.jd.skill_extractor import extract_skills


def parse_jd(text: str) -> dict:
    """Parse a JD into requirements, metadata, and keyword signals."""
    skills = extract_skills(text)
    keywords = extract_keywords(text)
    requirement_names = list(skills)
    for keyword in keywords:
        if keyword.lower() not in {skill.lower() for skill in requirement_names}:
            requirement_names.append(keyword)
    requirements = []
    for skill in requirement_names:
        requirements.append(
            {
                "skill": skill,
                "category": "General",
                "priority": classify_requirement(skill),
                "required_experience": extract_experience_requirement(skill),
                "source_text": skill,
            }
        )

    metadata = {
        "job_title": "Not detected",
        "company": "Not specified",
        "location": "Not detected",
        "experience_requirement": "Not detected",
    }

    title_match = re.search(r"(?:job title|title)[:\-]?\s*([A-Za-z0-9 /&\-]+)", text, flags=re.IGNORECASE)
    if title_match:
        metadata["job_title"] = title_match.group(1).strip()

    company_match = re.search(r"company[:\-]?\s*([A-Za-z0-9 .&\-]+)", text, flags=re.IGNORECASE)
    if company_match:
        metadata["company"] = company_match.group(1).strip()

    return {"requirements": requirements, "keywords": keywords, "metadata": metadata}
