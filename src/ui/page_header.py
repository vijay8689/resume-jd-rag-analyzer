from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


@st.cache_data(show_spinner=False)
def _background_image_data_uri() -> str:
    image_path = Path(__file__).resolve().parents[2] / "files" / "RAG.png"
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_page_header(title: str, subtitle: str, eyebrow: str = "") -> None:
    """Render a compact 3D visual header shared by the application pages."""
    background_image = _background_image_data_uri()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(3, 12, 27, .74), rgba(5, 18, 39, .82)),
                url('{background_image}') center top / cover fixed no-repeat;
        }}
        [data-testid="stSidebar"] {{
            background: rgba(5, 18, 39, .91);
        }}
        [data-testid="stMainBlockContainer"] {{
            background: rgba(5, 18, 39, .78);
            border-radius: 18px;
            padding: 1.25rem 1.5rem 2rem;
            box-shadow: 0 18px 50px rgba(0, 0, 0, .18);
        }}
        [data-testid="stMainBlockContainer"] h1,
        [data-testid="stMainBlockContainer"] h3,
        [data-testid="stMainBlockContainer"] p,
        [data-testid="stMainBlockContainer"] label,
        [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] {{
            color: #f7fbff;
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {{
            color: #c5d6e8;
        }}
        [data-testid="stMainBlockContainer"] [data-baseweb="select"] > div,
        [data-testid="stMainBlockContainer"] textarea,
        [data-testid="stMainBlockContainer"] input {{
            color: #10243d;
            background: rgba(255, 255, 255, .96);
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stDataFrame"] {{
            border: 1px solid rgba(164, 211, 255, .28);
            border-radius: 10px;
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stAlert"] {{
            border: 1px solid rgba(91, 190, 255, .32);
            border-radius: 12px;
            color: #f7fbff;
            background: rgba(20, 55, 105, .76);
        }}
        [data-testid="stFileUploader"] > section,
        [data-testid="stTextArea"] > div {{
            border: 1px solid rgba(91, 190, 255, .48);
            border-radius: 12px;
            background: rgba(8, 31, 65, .78);
            box-shadow: 0 8px 24px rgba(0, 0, 0, .2);
        }}
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploader"] section > div,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {{
            background: rgba(8, 31, 65, .78);
            color: #f7fbff;
        }}
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] label {{
            color: #d7e8f7;
        }}
        [data-testid="stTextArea"] textarea {{
            min-height: 220px;
            border: 0;
            color: #10243d;
            background: rgba(245, 250, 255, .96);
        }}
        [data-testid="stTextArea"] textarea::placeholder {{
            color: #5c7186;
            opacity: 1;
        }}
        [data-testid="stMainBlockContainer"] button,
        [data-testid="stSidebar"] button {{
            border: 1px solid rgba(91, 190, 255, .42);
            border-radius: 9px;
            color: #f7fbff;
            background: linear-gradient(135deg, #1769a8, #2454ba);
        }}
        [data-testid="stMainBlockContainer"] button:hover,
        [data-testid="stSidebar"] button:hover {{
            border-color: #8deaff;
            background: linear-gradient(135deg, #2389c7, #356de0);
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stMetric"] {{
            padding: .8rem;
            border: 1px solid rgba(91, 190, 255, .26);
            border-radius: 12px;
            background: rgba(14, 44, 87, .62);
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: #f7fbff;
        }}
        .rai-3d-header {{
            position: relative;
            isolation: isolate;
            overflow: hidden;
            min-height: 145px;
            margin: 0 0 1.25rem;
            padding: 1.5rem 1.75rem;
            border: 1px solid rgba(20, 36, 61, 0.18);
            border-radius: 14px;
            color: #f7fbff;
            background: linear-gradient(135deg, rgba(16, 36, 61, .95) 0%, rgba(28, 77, 104, .92) 48%, rgba(44, 139, 134, .88) 100%);
            box-shadow: 0 16px 34px rgba(17, 39, 59, 0.22), inset 0 1px 0 rgba(255,255,255,.2);
            transform: perspective(900px) rotateX(1deg);
        }}
        .rai-3d-header::before,
        .rai-3d-header::after {{
            content: "";
            position: absolute;
            z-index: -1;
            border: 1px solid rgba(255,255,255,.18);
            transform: rotate(-18deg) skewX(-18deg);
            pointer-events: none;
        }}
        .rai-3d-header::before {{
            width: 260px;
            height: 190px;
            right: 7%;
            top: -74px;
            background: linear-gradient(135deg, rgba(132, 235, 211, .28), rgba(25, 63, 88, .05));
            box-shadow: 18px 22px 0 rgba(255,255,255,.06), 36px 44px 0 rgba(255,255,255,.04);
        }}
        .rai-3d-header::after {{
            width: 130px;
            height: 130px;
            right: 30%;
            bottom: -92px;
            background: rgba(246, 190, 72, .2);
        }}
        .rai-3d-header__content {{
            position: relative;
            z-index: 1;
            max-width: 72%;
        }}
        .rai-3d-header__eyebrow {{
            margin: 0 0 .45rem;
            color: #a9f0dc;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .14em;
        }}
        .rai-3d-header h1 {{
            margin: 0;
            color: #f8fcff !important;
            font-size: clamp(1.65rem, 3vw, 2.45rem);
            line-height: 1.05;
            letter-spacing: 0;
            text-shadow: 0 2px 0 rgba(4, 20, 35, .42), 0 8px 18px rgba(4, 20, 35, .36);
        }}
        .rai-3d-header p {{
            margin: .65rem 0 0;
            color: #dcecff !important;
            font-size: .95rem;
        }}
        @media (max-width: 640px) {{
            .rai-3d-header {{ padding: 1.2rem; min-height: 130px; }}
            .rai-3d-header__content {{ max-width: 100%; }}
            .rai-3d-header h1 {{ font-size: 1.65rem; }}
        }}
        </style>
        <section class="rai-3d-header">
            <div class="rai-3d-header__content">
                <div class="rai-3d-header__eyebrow">{eyebrow}</div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the application attribution footer."""
    st.markdown(
        """
        <style>
        .rai-footer {
            margin-top: 3rem;
            padding: 1rem 0 .5rem;
            border-top: 1px solid rgba(20, 36, 61, .14);
            color: #64748b;
            font-size: .8rem;
            text-align: center;
        }
        </style>
        <footer class="rai-footer">© Kothapalli Vijay Kumar</footer>
        """,
        unsafe_allow_html=True,
    )
