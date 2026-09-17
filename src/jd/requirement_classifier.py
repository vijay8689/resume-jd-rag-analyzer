from __future__ import annotations

import re

PRIORITY_PATTERNS = {
    "MANDATORY": ["must have", "required", "mandatory", "experience required", "5+ years", "3+ years"],
    "PREFERRED": ["preferred", "nice to have", "plus", "good to have"],
    "OPTIONAL": ["optional", "a plus"],
}


def classify_requirement(text: str) -> str:
    """Classify a JD requirement as mandatory, preferred or optional."""
    lowered = text.lower()
    for level, patterns in PRIORITY_PATTERNS.items():
        if any(pattern in lowered for pattern in patterns):
            return level
    return "MANDATORY"


def extract_experience_requirement(text: str) -> float | None:
    """Extract a numeric year requirement from a JD requirement string."""
    match = re.search(r"(\d+(?:\.\d+)?)\+?\s*years?", text, flags=re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None
