from src.ingestion.document_processor import clean_text, detect_sections


def test_clean_text_normalizes_whitespace():
    text = "Hello   world\n\n\nNext line"
    result = clean_text(text)
    assert "Hello world" in result


def test_detect_sections_handles_common_resume_headers():
    text = "Professional Summary\nExperienced engineer\n\nTechnical Skills\nPython, Java\n"
    sections = detect_sections(text)
    assert any(item["section"] == "Professional Summary" for item in sections)
    assert any(item["section"] == "Technical Skills" for item in sections)
