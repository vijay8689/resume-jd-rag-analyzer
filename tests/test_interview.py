import json

import pytest

from src.services import interview_service


def test_generate_interview_questions_returns_ten_validated_items(monkeypatch):
    response = json.dumps(
        [
            {"question": f"Question {index}?", "answer": f"Answer {index}.", "skill": "Python"}
            for index in range(10)
        ]
    )

    class FakeLLM:
        def generate(self, prompt):
            assert "Python" in prompt
            assert "Matched" in prompt
            return response

    monkeypatch.setattr(interview_service, "get_llm", lambda: FakeLLM())

    questions = interview_service.generate_interview_questions(
        selected_skills=["Python"],
        skill_statuses={"Python": "Matched"},
        job_title="Backend Engineer",
    )

    assert len(questions) == 10
    assert questions[0] == {"question": "Question 0?", "answer": "Answer 0.", "skill": "Python"}


def test_generate_interview_questions_rejects_incomplete_model_output(monkeypatch):
    class FakeLLM:
        def generate(self, prompt):
            return json.dumps([{"question": "Only one?", "answer": "Not enough.", "skill": "Python"}])

    monkeypatch.setattr(interview_service, "get_llm", lambda: FakeLLM())

    with pytest.raises(ValueError, match="exactly 10"):
        interview_service.generate_interview_questions(["Python"], {"Python": "Matched"}, "Engineer")