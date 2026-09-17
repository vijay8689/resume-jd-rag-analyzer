import os
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.config.settings import settings
from src.services.resume_service import ResumeService
from src.services.analysis_service import AnalysisService
from src.ui.page_header import render_footer, render_page_header


st.set_page_config(page_title="Resume AI Match Analyzer", page_icon="📄", layout="wide")
st.logo(str(Path(__file__).parent / "files" / "RAG_LOGO.png"), size="medium")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .main { padding-top: 1rem; }
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
    ])

    with tabs[0]:
        st.write(f"Resume: {st.session_state.get('resume_filename', 'Unknown')}")
        st.write(f"Overall Match: {analysis_result.get('overall_match_percentage', 0):.1f}%")
        st.write("Top Matching Skills")
        for skill in analysis_result.get("top_matching_skills", [])[:5]:
            st.write(f"- {skill}")
        st.write("Key Skill Gaps")
        for skill in analysis_result.get("key_gaps", [])[:5]:
            st.write(f"- {skill}")

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
        for item in analysis_result.get("learning_resources", []):
            st.write(item)

    with tabs[7]:
        for item in analysis_result.get("resume_suggestions", []):
            st.write(f"- {item}")

    with tabs[8]:
        for evidence in analysis_result.get("evidence", []):
            st.write(evidence)

else:
    st.info("Upload your resume to get started. Your resume will be processed, chunked, embedded and indexed into ChromaDB.")

render_footer()
