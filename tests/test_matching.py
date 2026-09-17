from src.matching.exact_matcher import exact_match
from src.matching.hybrid_matcher import hybrid_status


def test_exact_match_detects_skill():
    assert exact_match("Playwright", "Playwright automation using Python") is True


def test_hybrid_status_for_related_technology():
    assert hybrid_status("Cypress", "Playwright is used in testing", 0.65) == "PARTIAL"
