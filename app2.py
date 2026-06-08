import time
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="RFQ-to-Estimate Copilot",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


COMPANY_NAME = "8DOOR"


def detect_file_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    mapping = {
        ".pdf": "PDF drawing package",
        ".xlsx": "Excel / BOQ file",
        ".xls": "Excel / BOQ file",
        ".csv": "CSV / BOQ file",
        ".png": "Image / drawing export",
        ".jpg": "Image / drawing export",
        ".jpeg": "Image / drawing export",
        ".dwg": "CAD drawing",
        ".dxf": "CAD drawing",
    }
    return mapping.get(suffix, "Unknown file type")


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def project_metadata():
    return [
        ("File type", "PDF drawing package"),
        ("Company", COMPANY_NAME),
        ("Project name", "RA-N01"),
        ("Document date", "16/02/2026"),
        ("Author", "Abdallah"),
        ("Pages detected", "12"),
        ("Detected objects", "Kitchen, island, wall shelf, stainless steel elements, stone surfaces"),
    ]


def apply_css():
    st.markdown(
        """
        <style>
        html, body, [class*="css"], .stApp {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
        }

        .block-container {
            padding-top: 0.35rem;
            max-width: 1180px;
        }

        header[data-testid="stHeader"] {
            background: rgba(255,255,255,0);
            height: 0rem;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .hero-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 250px;
        }

        .hero-title {
            text-align: center;
            font-size: 64px;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -2px;
            margin-bottom: 72px;
            color: #f47c48;
        }

        div[data-testid="stFileUploader"] {
            width: 600px;
            max-width: 100%;
            margin-left: auto;
            margin-right: auto;
        }

        div[data-testid="stFileUploader"] label {
            display: none;
        }

        div[data-testid="stFileUploader"] section {
            width: 600px;
            height: 200px;
            min-height: 200px;
            border: none;
            border-radius: 24px;
            background: #efefef;
            padding: 0;
            position: relative;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none;
        }

        div[data-testid="stFileUploader"] section:hover {
            background: #e7e7e7;
        }

        div[data-testid="stFileUploader"] section::before {
            content: "📎 Drop or upload";
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            font-weight: 400;
            color: #444;
            pointer-events: none;
        }

        div[data-testid="stFileUploader"] section > div {
            padding: 0;
            width: 100%;
            height: 100%;
        }

        div[data-testid="stFileUploaderDropzoneInstructions"] {
            display: none !important;
        }

        div[data-testid="stFileUploader"] button {
            display: none !important;
        }

        div[data-testid="stFileUploader"] small {
            display: none !important;
        }

        .processing-wrap {
            padding-top: 62px;
            max-width: 860px;
        }

        .processing-title {
            font-size: 42px;
            line-height: 1.1;
            font-weight: 700;
            letter-spacing: -1.2px;
            margin-bottom: 26px;
        }

        .status-card {
            border-radius: 14px;
            padding: 13px 18px;
            background: #eaf7ee;
            border: 1px solid #cfead7;
            color: #255c35;
            font-size: 15px;
            margin-top: 16px;
            margin-bottom: 28px;
        }

        .section-title {
            font-size: 28px;
            line-height: 1.15;
            font-weight: 700;
            letter-spacing: -0.8px;
            margin-top: 26px;
            margin-bottom: 18px;
        }

        .meta-divider {
            border-bottom: 1px solid #eeeeee;
            margin: 5px 0 7px 0;
        }

        .meta-key-text {
            color: #777;
            font-size: 16px;
            white-space: nowrap;
        }

        .meta-value-text {
            color: #222;
            font-size: 16px;
            font-weight: 500;
            text-align: left;
        }

        div[data-testid="stButton"] button {
            height: 68px;
            border-radius: 16px;
            font-size: 22px !important;
            font-weight: 900 !important;
            border: 1px solid #111;
        }

        div[data-testid="stButton"] button p {
            font-size: 22px !important;
            font-weight: 900 !important;
        }

        div[data-testid="stButton"] button:hover {
            border-color: #f47c48;
            color: #f47c48;
        }

        @media (max-height: 850px) {
            .processing-wrap {
                padding-top: 34px;
            }

            .processing-title {
                font-size: 38px;
                margin-bottom: 22px;
            }

            .status-card {
                margin-bottom: 22px;
            }

            .section-title {
                margin-top: 18px;
                margin-bottom: 14px;
            }

            div[data-testid="stButton"] button {
                height: 58px;
            }

            div[data-testid="stButton"] button p {
                font-size: 19px !important;
            }
        }

        @media (max-width: 760px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }

        .hero-wrap {
            padding-top: 140px;
        }

        .hero-title {
            font-size: 40px;
            line-height: 1.12;
            margin-bottom: 44px;
            letter-spacing: -1.3px;
        }

        div[data-testid="stFileUploader"] {
            width: 100%;
        }

        div[data-testid="stFileUploader"] section {
            width: 100%;
            height: 170px;
            min-height: 170px;
            border-radius: 20px;
        }

        div[data-testid="stFileUploader"] section::before {
            font-size: 23px;
        }

        .processing-wrap {
            padding-top: 26px;
            max-width: 100%;
        }

        .processing-title {
            font-size: 30px;
            line-height: 1.14;
            margin-bottom: 22px;
        }

        .status-card {
            font-size: 14px;
            padding: 12px 14px;
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 23px;
            margin-top: 18px;
            margin-bottom: 14px;
        }

        .meta-key-text,
        .meta-value-text {
            font-size: 14px;
        }

        div[data-testid="stButton"] button {
            height: 58px;
        }

        div[data-testid="stButton"] button p {
            font-size: 16px !important;
            font-weight: 900 !important;
        }
        
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_upload_screen():
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-title">
            RFQ to Estimate to Proposal
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Drop or upload",
        type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "dwg", "dxf"],
        label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.uploaded_file_size = uploaded_file.size
        st.session_state.uploaded_file_type = detect_file_type(uploaded_file.name)
        st.session_state.screen = "processing"
        st.rerun()

def render_processing_screen():
    st.markdown('<div class="processing-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="processing-title">
            Reading your RFQ package
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress = st.progress(0)
    status_placeholder = st.empty()

    steps = [
        "Detecting file type...",
        "Reading title block...",
        "Extracting project metadata...",
        "Detecting drawing pages...",
        "Identifying scope categories...",
        "Project metadata extracted.",
    ]

    for i, step in enumerate(steps, start=1):
        status_placeholder.markdown(
            f"""
            <div class="status-card">
                {step}
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress.progress(i / len(steps))
        time.sleep(0.75)

    st.markdown(
        """
        <div class="section-title">
            Detected project info
        </div>
        """,
        unsafe_allow_html=True,
    )

    for key, value in project_metadata():
        col1, col2 = st.columns([0.30, 0.70])
        with col1:
            st.markdown(
                f'<div class="meta-key-text">{key}:</div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="meta-value-text">{value}</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="meta-divider"></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    if col1.button("Back", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if col2.button("Continue to estimation", use_container_width=True):
        st.session_state.screen = "next_placeholder"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def render_next_placeholder():
    st.markdown("## Next screen placeholder")
    st.write("Here we will add extracted scope, materials, missing info, estimate draft and proposal preview.")

    if st.button("Start over"):
        st.session_state.clear()
        st.rerun()


apply_css()

if "screen" not in st.session_state:
    st.session_state.screen = "upload"

if st.session_state.screen == "upload":
    render_upload_screen()
elif st.session_state.screen == "processing":
    render_processing_screen()
else:
    render_next_placeholder()