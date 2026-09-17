from src.jd.skill_extractor import extract_skills


def test_extract_skills_from_text():
    text = "Python, Selenium, Playwright, Kubernetes"
    skills = extract_skills(text)
    assert "Python" in skills
    assert "Selenium" in skills
    assert "Playwright" in skills
