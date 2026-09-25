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
                linear-gradient(115deg, rgba(3, 12, 27, .74), rgba(5, 18, 39, .82)),
                repeating-linear-gradient(135deg, rgba(126, 249, 211, .025) 0 1px, transparent 1px 18px),
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
            border: 2px solid rgba(164, 211, 255, .38);
            border-radius: 10px;
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stAlert"] {{
            border: 2px solid rgba(91, 190, 255, .52);
            border-radius: 12px;
            color: #f7fbff;
            background: rgba(20, 55, 105, .76);
        }}
        [data-testid="stFileUploader"] > section,
        [data-testid="stTextArea"] > div {{
            border: 2px solid rgba(91, 190, 255, .72);
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
            border-color: #9af4d8;
            background: linear-gradient(135deg, #168f91, #2774c8);
            transform: translateY(-1px);
            box-shadow: 0 7px 18px rgba(21, 173, 166, .24);
        }}
        [data-testid="stMainBlockContainer"] button,
        [data-testid="stSidebar"] button {{
            transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: .35rem;
            border-bottom: 1px solid rgba(126, 249, 211, .24);
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 2.8rem;
            color: #c5d6e8;
            border-radius: 8px 8px 0 0;
            transition: color .18s ease, background .18s ease;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: #a9f0dc;
            background: rgba(30, 126, 145, .22);
        }}
        .stTabs [aria-selected="true"] {{
            color: #a9f0dc !important;
            background: rgba(30, 126, 145, .2);
        }}
        [data-testid="stProgressBar"] > div > div > div > div {{
            background: linear-gradient(90deg, #25b7a5, #5bcaff);
        }}
        [data-testid="stExpander"] {{
            border: 1px solid rgba(91, 190, 255, .3);
            border-radius: 10px;
            background: rgba(8, 31, 65, .46);
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stAlert"] a {{
            color: #9af4d8;
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                transition-duration: .01ms !important;
                scroll-behavior: auto !important;
            }}
        }}
        [data-testid="stMainBlockContainer"] [data-testid="stMetric"] {{
            padding: .8rem;
            border: 2px solid rgba(91, 190, 255, .42);
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
            overflow: visible;
            min-height: 145px;
            margin: 0 0 1.25rem;
            padding: 1.5rem 1.75rem;
            border: 2px solid rgba(120, 190, 255, 0.7);
            border-radius: 14px;
            color: #f7fbff;
            background: transparent;
            box-shadow: none;
            transform: perspective(900px) rotateX(1deg);
        }}
        .rai-3d-header::before,
        .rai-3d-header::after {{
            content: "";
            position: absolute;
            z-index: -1;
            border: 1px solid rgba(255,255,255,.12);
            transform: rotate(-18deg) skewX(-18deg);
            pointer-events: none;
            opacity: .15;
        }}
        .rai-3d-header::before {{
            width: 240px;
            height: 180px;
            right: 8%;
            top: -72px;
            background: linear-gradient(135deg, rgba(126, 249, 211, .14), rgba(64, 191, 255, .04), transparent 75%);
            box-shadow: 18px 22px 0 rgba(255,255,255,.02), 36px 44px 0 rgba(255,255,255,.01);
        }}
        .rai-3d-header::after {{
            width: 110px;
            height: 110px;
            right: 28%;
            bottom: -78px;
            background: rgba(255, 216, 107, .08);
            box-shadow: 0 0 16px rgba(255, 216, 107, .08);
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
            margin: .75rem 0 0;
            color: #dcecff !important;
            font-size: .98rem;
            max-width: 70%;
            text-shadow: 0 2px 10px rgba(5, 18, 39, .4);
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
            border-top: 1px solid rgba(126, 249, 211, .24);
            color: #c5d6e8;
            font-size: .8rem;
            text-align: center;
        }
        </style>
        <footer class="rai-footer">© Kothapalli Vijay Kumar</footer>
        """,
        unsafe_allow_html=True,
    )
