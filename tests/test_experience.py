from src.matching.experience_matcher import compare_experience, extract_resume_experience


def test_extract_resume_experience_handles_explicit_years():
    text = "Selenium automation experience for 10 years"
    assert extract_resume_experience(text, "Selenium") == 10.0


def test_compare_experience_meets_requirement():
    assert compare_experience(5.0, 7.0) == "MEETS_REQUIREMENT"
