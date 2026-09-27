import streamlit as st

from src.config.settings import settings
from src.llm.llm_client import MissingAPIKeyError
from src.services.interview_service import generate_interview_questions
from src.ui.page_header import render_footer, render_page_header

st.set_page_config(page_title="Interview Preparation", page_icon=":material/forum:", layout="wide")
render_page_header(
    "Interview Preparation",
    "Build confidence with tailored questions and sample answers for your target role.",
    tone="violet",
)

analysis_result = st.session_state.get("analysis_result")
if not analysis_result:
    st.info("Analyze your resume against a job description first to prepare a tailored interview practice set.")
    st.page_link("Application.py", label="Go to resume analysis", icon=":material/description:")
    render_footer()
    st.stop()

st.caption(f"Target role: {analysis_result.get('job_title') or 'Your selected role'}")

skill_statuses = {}
for result_key, status in (
    ("matched_skills", "Matched"),
    ("partial_skills", "Partial"),
    ("missing_skills", "Unmatched"),
):
    for item in analysis_result.get(result_key, []):
        skill = item.get("skill")
        if skill:
            skill_statuses.setdefault(skill, status)

skills = list(skill_statuses)
selected_skills = st.multiselect(
    "Select preferred skills",
    options=skills,
    format_func=lambda skill: f"{skill} · {skill_statuses[skill]}",
    default=[skill for skill in st.session_state.get("interview_selected_skills", []) if skill in skills],
    key="_interview_selected_skills",
    help="Choose matched, partially matched, or unmatched skills for your interview practice set.",
)
st.session_state.interview_selected_skills = list(selected_skills)

generate_clicked = st.button(
    "Generate 10 Questions",
    key="generate_interview_questions",
    type="primary",
    disabled=not selected_skills or not settings.llm_enabled,
)

if not settings.llm_enabled:
    st.info("Enable the language model in your app configuration to generate interview questions.")
elif not skills:
    st.info("No extracted skills are available for interview preparation.")
elif not selected_skills:
    st.info("Select one or more skills to build your interview practice set.")

if generate_clicked:
    with st.spinner("Preparing interview questions and sample answers..."):
        try:
            questions = generate_interview_questions(
                selected_skills=selected_skills,
                skill_statuses=skill_statuses,
                job_title=analysis_result.get("job_title", ""),
            )
            st.session_state.interview_questions = {
                "skills": list(selected_skills),
                "items": questions,
            }
        except MissingAPIKeyError as exc:
            st.session_state.interview_questions = None
            st.warning(str(exc))
            st.caption("Add your key locally, then select Generate 10 Questions again.")
            st.code("XKIRO_API_KEY=your-api-key", language="dotenv")
        except Exception as exc:
            st.session_state.interview_questions = None
            st.error(f"Unable to generate interview preparation: {exc}")

generated = st.session_state.get("interview_questions")
if generated and generated.get("skills") == list(selected_skills):
    st.caption("Generated for: " + ", ".join(generated["skills"]))
    for index, item in enumerate(generated["items"], start=1):
        with st.expander(f"{index}. {item['question']}", expanded=index == 1):
            st.caption(f"Skill focus: {item['skill']}")
            st.markdown(f"**Sample answer**\n\n{item['answer']}")
elif generated and selected_skills:
    st.info("Your selection changed. Generate again to update the questions and answers.")


render_footer()
