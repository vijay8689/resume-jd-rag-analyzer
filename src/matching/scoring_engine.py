from __future__ import annotations

PRIORITY_WEIGHTS = {"MANDATORY": 3, "PREFERRED": 2, "OPTIONAL": 1}
MATCH_WEIGHTS = {"MATCHED": 1.0, "PARTIAL": 0.5, "MISSING": 0.0}


def calculate_weighted_score(results: list[dict]) -> float:
    """Compute the weighted match percentage from a set of skill results."""
    weighted = 0.0
    total = 0.0
    for item in results:
        weight = PRIORITY_WEIGHTS.get(item.get("priority", "OPTIONAL"), 1)
        value = MATCH_WEIGHTS.get(item.get("status", "MISSING"), 0.0)
        weighted += weight * value
        total += weight
    if total == 0:
        return 0.0
    return round((weighted / total) * 100, 1)


def compute_keyword_coverage(present: list[str], missing: list[str], total: list[str] | None = None) -> float:
    """Compute keyword coverage using present and missing sets."""
    total_keywords = total if total is not None else list(set(present + missing))
    if not total_keywords:
        return 0.0
    return round((len(present) / len(total_keywords)) * 100, 1)


def compute_group_coverage(matches: list[dict], total: list[dict]) -> float:
    """Calculate coverage relative to a total group."""
    if not total:
        return 0.0
    return round((len(matches) / len(total)) * 100, 1)
