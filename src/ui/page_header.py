from __future__ import annotations

import streamlit as st


def render_page_header(title: str, subtitle: str, eyebrow: str = "RESUME INTELLIGENCE") -> None:
    """Render a compact 3D visual header shared by the application pages."""
    st.markdown(
        f"""
        <style>
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
            background:
                linear-gradient(135deg, #10243d 0%, #1c4d68 48%, #2c8b86 100%);
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
            color: #ffffff;
            font-size: clamp(1.65rem, 3vw, 2.45rem);
            line-height: 1.05;
            letter-spacing: 0;
            text-shadow: 0 3px 0 rgba(4, 20, 35, .22), 0 10px 22px rgba(4, 20, 35, .2);
        }}
        .rai-3d-header p {{
            margin: .65rem 0 0;
            color: rgba(247, 251, 255, .8);
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
