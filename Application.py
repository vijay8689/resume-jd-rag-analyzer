import os
from datetime import datetime
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

from src.config.settings import settings
from src.services.resume_service import ResumeService
from src.services.analysis_service import AnalysisService
from src.services.interview_service import generate_interview_questions
from src.ui.page_header import render_footer, render_page_header


st.set_page_config(page_title="Resume AI Match Analyzer", page_icon="📄", layout="wide")
st.logo(str(Path(__file__).parent / "files" / "RAG_LOGO.png"), size="medium")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .main { padding-top: 0; }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
            box-shadow: none;
            border-bottom: none;
        }
        [data-testid="stHeader"] .stAppHeader {
            background: rgba(0, 0, 0, 0);
        }
        .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
        .stTabs [data-baseweb="tab"] { height: 2.5rem; }
        .metric-container { background: #f0f2f6; border-radius: 0.75rem; padding: 0.8rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


render_page_header("Resume AI Match Analyzer", "RAG-powered resume and job description skill gap analysis.")

if "session_id" not in st.session_state:
    st.session_state.session_id = "session_" + os.urandom(4).hex()
if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "interview_selected_skills" not in st.session_state:
    st.session_state.interview_selected_skills = []

resume_service = ResumeService()
analysis_service = AnalysisService()

with st.sidebar:
    st.subheader("Resume")
    uploaded = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        help="PDF, DOCX, or TXT. Maximum file size: 500 KB.",
    )
    if uploaded is not None:
        if st.button("Process Resume"):
            status = st.status("Processing resume...", expanded=True)
            try:
                status.write("Extracting resume text and preparing searchable chunks...")
                result = resume_service.process_uploaded_resume(uploaded, st.session_state.session_id)
                st.session_state.resume_processed = True
                st.session_state.resume_filename = uploaded.name
                st.session_state.document_id = result["document_id"]
                status.update(
                    label=f"Resume indexed successfully ({result['chunk_count']} chunks)",
                    state="complete",
                    expanded=False,
                )
            except Exception as exc:
                status.update(label="Resume processing failed", state="error", expanded=True)
                st.error(f"Unable to process resume: {exc}")

    st.write(f"Resume Status: {'Ready' if st.session_state.get('resume_processed') else 'Not uploaded'}")
    if st.session_state.get("resume_filename"):
        st.write(f"File: {st.session_state.resume_filename}")

    st.subheader("Analysis")
    st.write(f"Model Status: {'Enabled' if settings.llm_enabled else 'Disabled'}")
    st.write("Vector DB Status: Active")

    st.subheader("Actions")
    if st.button("Clear Resume"):
        resume_service.clear_session_data(st.session_state.session_id)
        st.session_state.resume_processed = False
        st.session_state.analysis_result = None
        st.session_state.pop("resume_filename", None)
        st.session_state.pop("document_id", None)
        st.success("Session reset.")

    st.subheader("Settings")
    st.write(f"Similarity Threshold: {settings.match_threshold}")
    st.write(f"Top K: {settings.top_k}")

st.subheader("Job Description")
jd_text = st.text_area("Paste the complete job description below.", height=220, placeholder="Paste job description here...")

if st.button("Analyze Resume", disabled=not bool(jd_text.strip())):
    if not st.session_state.get("resume_processed"):
        st.warning("Please upload a resume before starting analysis.")
    elif not jd_text.strip():
        st.warning("The Job Description does not contain enough information for analysis.")
    else:
        with st.spinner("Analyzing resume against JD..."):
            try:
                result = analysis_service.analyze_resume_against_jd(
                    session_id=st.session_state.session_id,
                    document_id=st.session_state.document_id,
                    jd_text=jd_text,
                )
                st.session_state.analysis_result = result
                st.session_state.interview_questions = None
                st.session_state.interview_selected_skills = []
                st.session_state.analysis_history.append(
                    {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "resume": st.session_state.get("resume_filename", "Unknown"),
                        "job_title": result.get("job_title", "Not detected"),
                        "overall_match_percentage": result.get("overall_match_percentage", 0.0),
                        "matched_count": result.get("matched_count", 0),
                        "partial_count": result.get("partial_count", 0),
                        "missing_count": result.get("missing_count", 0),
                        "result": result,
                    }
                )
                st.success("Analysis complete.")
            except Exception as exc:
                st.error(f"AI reasoning is temporarily unavailable: {exc}")

analysis_result = st.session_state.get("analysis_result")

if analysis_result:
    st.subheader("Analysis")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Match", f"{analysis_result.get('overall_match_percentage', 0):.1f}%")
    c2.metric("Matched Skills", analysis_result.get("matched_count", 0))
    c3.metric("Partial Skills", analysis_result.get("partial_count", 0))
    c4.metric("Missing Skills", analysis_result.get("missing_count", 0))

    tabs = st.tabs([
        "Overview",
        "Skills Match",
        "Partial Match",
        "Missing Skills",
        "Keywords",
        "Experience",
        "Learning Roadmap",
        "Resume Suggestions",
        "Evidence",
        "Interview Preparation",
    ])

    with tabs[0]:
        overview_columns = st.columns([1, 1.5])
        match_percentage = float(analysis_result.get("overall_match_percentage", 0))
        status_counts = [
            int(analysis_result.get("matched_count", 0)),
            int(analysis_result.get("partial_count", 0)),
            int(analysis_result.get("missing_count", 0)),
        ]
        with overview_columns[0]:
            st.caption(f"Resume: {st.session_state.get('resume_filename', 'Unknown')}")
            if sum(status_counts):
                chart = go.Figure(
                    go.Pie(
                        labels=["Matched", "Partial", "Missing"],
                        values=status_counts,
                        hole=0.7,
                        sort=False,
                        marker={"colors": ["#43d6b5", "#ffc857", "#ff7b72"]},
                        textinfo="label+value",
                        textfont={"color": "#f7fbff", "size": 12},
                        hovertemplate="%{label}: %{value} skills<extra></extra>",
                    )
                )
                chart.update_layout(
                    height=280,
                    margin={"t": 12, "b": 12, "l": 12, "r": 12},
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    annotations=[
                        {
                            "text": f"{match_percentage:.0f}%<br><span style='font-size:12px'>MATCH</span>",
                            "x": 0.5,
                            "y": 0.5,
                            "showarrow": False,
                            "font": {"color": "#f7fbff", "size": 25},
                        }
                    ],
                )
                st.plotly_chart(chart, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("No skill matches were found to visualize.")
        with overview_columns[1]:
            st.subheader("Top Matching Skills")
            matching_skills = analysis_result.get("top_matching_skills", [])[:5]
            st.write(" · ".join(matching_skills) if matching_skills else "No matching skills found.")
            st.subheader("Key Skill Gaps")
            key_gaps = analysis_result.get("key_gaps", [])[:5]
            st.write(" · ".join(key_gaps) if key_gaps else "No skill gaps found.")

    with tabs[1]:
        for skill in analysis_result.get("matched_skills", []):
            st.write(f"- {skill['skill']} ({skill.get('status', 'MATCHED')})")

    with tabs[2]:
        for skill in analysis_result.get("partial_skills", []):
            st.write(f"- {skill['skill']} ({skill.get('status', 'PARTIAL')})")

    with tabs[3]:
        for skill in analysis_result.get("missing_skills", []):
            st.write(f"- {skill['skill']} ({skill.get('priority', 'MEDIUM')})")

    with tabs[4]:
        st.write("Present Keywords")
        st.write(", ".join(analysis_result.get("present_keywords", [])) or "None")
        st.write("Missing Keywords")
        st.write(", ".join(analysis_result.get("missing_keywords", [])) or "None")

    with tabs[5]:
        for entry in analysis_result.get("experience_analysis", []):
            st.write(entry)

    with tabs[6]:
        roadmap = analysis_result.get("learning_resources", {})
        if isinstance(roadmap, dict):
            for skill, resources in roadmap.items():
                st.subheader(skill)
                if not resources:
                    st.info("No tutorial links found for this skill.")
                    continue
                for resource in resources if isinstance(resources, list) else [resources]:
                    if isinstance(resource, dict) and resource.get("url"):
                        title = resource.get("title") or resource.get("name") or resource["url"]
                        st.markdown(f"- [{title}]({resource['url']})")
                    else:
                        st.write(resource)
        elif roadmap:
            st.write(roadmap)
        else:
            st.info("No learning resources are needed.")

    with tabs[7]:
        for item in analysis_result.get("resume_suggestions", []):
            st.write(f"- {item}")

    with tabs[8]:
        for evidence in analysis_result.get("evidence", []):
            st.write(evidence)

    with tabs[9]:
        st.subheader("Interview Preparation")
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
            key="interview_selected_skills",
            help="Choose matched, partially matched, or unmatched skills for your interview practice set.",
        )
        generate_clicked = st.button(
            "Generate 10 Questions",
            key="generate_interview_questions",
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

else:
    st.info("Upload your resume to get started. Your resume will be processed, chunked, embedded and indexed into ChromaDB.")

render_footer()
