import os
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go

from src.config.settings import settings
from src.services.resume_service import ResumeService
from src.services.analysis_service import AnalysisService
from src.ui.page_header import render_footer, render_page_header, render_workflow


st.set_page_config(page_title="Resume AI Match Analyzer", page_icon="📄", layout="wide")




render_page_header("Resume AI Match Analyzer", "Understand your fit. Identify skill gaps. Plan your next career move.")

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
        if st.button("Process Resume", type="primary", use_container_width=True):
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

render_workflow(st.session_state.get("resume_processed", False), bool(st.session_state.get("analysis_result")))

with st.container(border=True, key="job_description_panel"):
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the complete job description below.", height=220, placeholder="Paste job description here...")

if st.button("Analyze Resume", type="primary", disabled=not bool(jd_text.strip())):
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
                        marker={"colors": ["#28776a", "#c99738", "#bb6861"]},
                        textinfo="label+value",
                        textposition="outside", automargin=True,
                        textfont={"color": "#20333f", "size": 12},
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
                            "font": {"color": "#20333f", "size": 25},
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


else:
    st.info("Start with your resume in the sidebar, then add a job description. Your analysis will highlight matching skills, opportunities to improve, and practical next steps.")

render_footer()
