from __future__ import annotations

import json
from typing import Any

from src.llm.llm_client import get_llm, safe_json_loads


def generate_interview_questions(
    selected_skills: list[str],
    skill_statuses: dict[str, str],
    job_title: str,
) -> list[dict[str, str]]:
    """Generate ten tailored interview questions and answers for selected skills."""
    if not selected_skills:
        raise ValueError("Select at least one skill to generate interview questions.")

    selected_stack = [
        {"skill": skill, "resume_match": skill_statuses.get(skill, "UNKNOWN")}
        for skill in selected_skills
    ]
    prompt = f"""
Create exactly 10 interview questions and concise, accurate sample answers for a candidate
preparing for the role {job_title or "described by the selected skill stack"}.
Base every question on this selected skill stack and resume match context:
{json.dumps(selected_stack, ensure_ascii=True)}

For matched skills, test practical depth. For partial skills, test applied understanding.
For missing skills, use fair foundational or transferable-skill questions; do not imply
the candidate has experience they do not claim. Mix technical, scenario, and troubleshooting
questions where appropriate. Avoid duplicate questions.

Return only a valid JSON array containing exactly 10 objects. Each object must have
"question", "answer", and "skill" string fields. Keep answers helpful and interview-ready.
""".strip()

    response = get_llm().generate(prompt)
    parsed: Any = safe_json_loads(response)
    if isinstance(parsed, dict):
        parsed = parsed.get("questions")
    if not isinstance(parsed, list) or len(parsed) != 10:
        raise ValueError("The model did not return exactly 10 interview questions.")

    questions: list[dict[str, str]] = []
    for item in parsed:
        if not isinstance(item, dict):
            raise ValueError("The model returned an invalid interview question.")
        question = item.get("question")
        answer = item.get("answer")
        skill = item.get("skill")
        if not all(isinstance(value, str) and value.strip() for value in (question, answer, skill)):
            raise ValueError("The model returned an incomplete interview question or answer.")
        questions.append({"question": question.strip(), "answer": answer.strip(), "skill": skill.strip()})

    return questions