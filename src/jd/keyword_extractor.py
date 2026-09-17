from __future__ import annotations

KEYWORDS = [
    "CI/CD",
    "Kubernetes",
    "Terraform",
    "Performance Testing",
    "Test Observability",
    "Quality Assurance",
    "Automation",
    "API Testing",
    "Cloud",
    "Docker",
    "Jenkins",
    "Azure",
]


def extract_keywords(text: str) -> list[str]:
    """Extract important keywords from freeform text."""
    found: list[str] = []
    lowered = text.lower()
    for keyword in KEYWORDS:
        if keyword.lower() in lowered:
            found.append(keyword)
    return found
