from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st


def render_page_header(title: str, subtitle: str, eyebrow: str = "RESUME INTELLIGENCE", tone: str = "indigo") -> None:
    """Apply the shared visual system and render an accessible page heading."""
    css = Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
    tone = tone if tone in {"indigo", "teal", "violet", "blue"} else "indigo"
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <section class="rai-header rai-header--{tone}">
            <div class="rai-header__content">
                <div class="rai-eyebrow">{escape(eyebrow)}</div>
                <h1>{escape(title)}</h1>
                <p>{escape(subtitle)}</p>
            </div>
            <div class="rai-graphic" aria-hidden="true">
                <div class="rai-graphic__document"><span></span><span></span><span></span><span></span></div>
                <div class="rai-graphic__connection"></div>
                <div class="rai-graphic__target"><div></div></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_workflow(resume_ready: bool, analysis_ready: bool) -> None:
    """Show actual session progress without implying an analysis score."""
    steps = [
        ("01", "Add your resume", "Ready for analysis" if resume_ready else "Upload and process in the sidebar", resume_ready),
        ("02", "Define the role", "Paste the job description below", resume_ready),
        ("03", "Explore the match", "Results available below" if analysis_ready else "Review skills, gaps, and next steps", analysis_ready),
    ]
    cards = "".join(
        f'<div class="rai-step {"is-ready" if ready else ""}">'
        f'<span class="rai-step__number">{number}</span>'
        f'<div><strong>{title}</strong><p>{description}</p></div></div>'
        for number, title, description, ready in steps
    )
    st.markdown(f'<section class="rai-workflow" aria-label="Analysis workflow">{cards}</section>', unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown(
        '<footer class="rai-footer"><span>Resume AI Match Analyzer</span><span>&copy; Kothapalli Vijay Kumar</span></footer>',
        unsafe_allow_html=True,
    )
