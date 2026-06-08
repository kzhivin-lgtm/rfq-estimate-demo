import time
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="RFQ-to-Estimate Demo",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


COMPANY_NAME = "8DOOR"
VAT_RATE = 0.18


# -----------------------------
# data
# -----------------------------

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
        ("Detected objects", "Kitchen, Kitchen island, Wall shelf"),
    ]


def default_objects():
    return {
        "kitchen": {
            "name": "Kitchen",
            "qty": 1,
            "materials": [
                "carpentry / stainless steel",
                "formica",
            ],
            "approved": False,
            "unit_cost": None,
            "suggested_price": None,
            "sale_price": None,
        },
        "kitchen_island": {
            "name": "Kitchen island",
            "qty": 1,
            "materials": [
                "carpentry / stainless steel",
                "formica / stone",
            ],
            "approved": False,
            "unit_cost": None,
            "suggested_price": None,
            "sale_price": None,
        },
        "wall_shelf": {
            "name": "Wall shelf",
            "qty": 1,
            "materials": [
                "oak veneer / corten partitions",
                "metal elements",
            ],
            "approved": False,
            "unit_cost": None,
            "suggested_price": None,
            "sale_price": None,
        },
    }


def object_demo_costs():
    return {
        "kitchen": {
            "unit_cost": 249_348,
            "suggested_price": round(249_348 * 1.30),
        },
        "kitchen_island": {
            "unit_cost": 196_414,
            "suggested_price": round(196_414 * 1.30),
        },
        "wall_shelf": {
            "unit_cost": 97_521,
            "suggested_price": round(97_521 * 1.30),
        },
    }    


def object_materials(object_key: str):
    data = {
        "kitchen": [
            ["carpentry", "Formica Birman 2650 interior", "allowance", "₪8,600", "detected"],
            ["metal", "Stainless steel exterior panels", "allowance", "₪14,800", "supplier missing"],
            ["hardware", "Handles / hinges / slides", "allowance", "₪4,800", "quantity review"],
            ["consumables", "glue / screws / sanding / protection", "lot", "₪2,200", "auto-added"],
        ],
        "kitchen_island": [
            ["carpentry", "Formica Birman 2650 interior", "allowance", "₪6,900", "detected"],
            ["metal", "Stainless steel exterior panels", "allowance", "₪11,200", "supplier missing"],
            ["stone", "Laba Rosa countertop", "allowance", "₪16,800", "supplier missing"],
            ["hardware", "Handles / hinges / slides", "allowance", "₪3,400", "quantity review"],
            ["consumables", "glue / screws / sanding / protection", "lot", "₪1,800", "auto-added"],
        ],
        "wall_shelf": [
            ["carpentry", "Oak veneer NextDoor", "allowance", "₪7,200", "detected"],
            ["metal", "Corten partitions / metal elements", "allowance", "₪5,600", "supplier missing"],
            ["hardware", "Mounting hardware", "allowance", "₪1,300", "review"],
            ["consumables", "glue / screws / sanding / protection", "lot", "₪900", "auto-added"],
        ],
    }

    return pd.DataFrame(
        data[object_key],
        columns=["group", "material", "qty / basis", "cost", "status"],
    )


def object_labor(object_key: str):
    data = {
        "kitchen": [
            ["drawing review", "estimator / PM", 3, "₪180", "₪540"],
            ["cutting", "carpenter", 7, "₪160", "₪1,120"],
            ["drilling / machining", "carpenter / CNC", 8, "₪170", "₪1,360"],
            ["assembly", "carpenter", 18, "₪160", "₪2,880"],
            ["test assembly", "carpenter", 6, "₪160", "₪960"],
            ["disassembly", "carpenter", 3, "₪160", "₪480"],
            ["packing", "worker", 4, "₪120", "₪480"],
        ],
        "kitchen_island": [
            ["drawing review", "estimator / PM", 2, "₪180", "₪360"],
            ["cutting", "carpenter", 5, "₪160", "₪800"],
            ["drilling / machining", "carpenter / CNC", 6, "₪170", "₪1,020"],
            ["assembly", "carpenter", 13, "₪160", "₪2,080"],
            ["test assembly", "carpenter", 4, "₪160", "₪640"],
            ["packing", "worker", 3, "₪120", "₪360"],
        ],
        "wall_shelf": [
            ["drawing review", "estimator / PM", 2, "₪180", "₪360"],
            ["cutting", "carpenter", 4, "₪160", "₪640"],
            ["veneer work", "carpenter", 7, "₪160", "₪1,120"],
            ["metal / corten coordination", "metal worker", 4, "₪180", "₪720"],
            ["assembly", "carpenter", 8, "₪160", "₪1,280"],
            ["packing", "worker", 2, "₪120", "₪240"],
        ],
    }

    return pd.DataFrame(
        data[object_key],
        columns=["process", "role", "hours", "rate", "cost"],
    )


def object_cost_breakdown(object_key: str):
    data = {
        "kitchen": [
            ["materials", 48900],
            ["consumables", 2200],
            ["labor", 7820],
            ["machine consumables", 1600],
            ["equipment depreciation", 1900],
            ["subcontractors", 6400],
            ["internal transport", 980],
            ["overhead allocation", 2500],
        ],
        "kitchen_island": [
            ["materials", 40100],
            ["consumables", 1800],
            ["labor", 5260],
            ["machine consumables", 1200],
            ["equipment depreciation", 1500],
            ["subcontractors", 5700],
            ["internal transport", 720],
            ["overhead allocation", 1820],
        ],
        "wall_shelf": [
            ["materials", 15000],
            ["consumables", 900],
            ["labor", 4360],
            ["machine consumables", 600],
            ["equipment depreciation", 850],
            ["subcontractors", 1700],
            ["internal transport", 390],
            ["overhead allocation", 800],
        ],
    }

    return pd.DataFrame(data[object_key], columns=["cost block", "amount"])


def ensure_objects_state():
    if "objects" not in st.session_state:
        st.session_state.objects = default_objects()

def ensure_detection_state():
    ensure_objects_state()

    if "detected_object_names" not in st.session_state:
        st.session_state.detected_object_names = {
            key: obj["name"] for key, obj in st.session_state.objects.items()
        }

    if "objects_confirmed" not in st.session_state:
        st.session_state.objects_confirmed = False

    if "confirm_detection_error" not in st.session_state:
        st.session_state.confirm_detection_error = False


# -----------------------------
# css
# -----------------------------

def apply_css():
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #ffffff;
            --text-main: #20222a;
            --text-muted: #737373;
            --line-soft: #eeeeee;
            --upload-bg: #efefef;
            --upload-hover: #e7e7e7;
            --orange: #f47c48;
            --green-bg: #eaf7ee;
            --green-border: #cfead7;
            --green-text: #255c35;
            --card-bg: #ffffff;
            --card-border: #e8e8e8;
            --soft-bg: #f7f7f7;
            --blue-focus: #2f80ed;
            --error: #d94c4c;
            --ok: #2f9e44;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #0e1117;
                --text-main: #f2f2f2;
                --text-muted: #b8b8b8;
                --line-soft: #343842;
                --upload-bg: #1c202a;
                --upload-hover: #252a36;
                --orange: #f47c48;
                --green-bg: #10291a;
                --green-border: #245738;
                --green-text: #b8f3c9;
                --card-bg: #121722;
                --card-border: #303746;
                --soft-bg: #161a23;
            }
        }

        html, body, [class*="css"], .stApp {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
        }

        .stApp {
            background: var(--app-bg);
            color: var(--text-main);
        }

        .block-container {
            padding-top: 0.35rem;
            max-width: 1180px;
        }

        header[data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        /* hide Streamlit chrome / toolbar where reachable from app DOM */

        #MainMenu,
        footer,
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stDeployButton"],
        #GithubIcon,
        .viewerBadge_container__1QSob,
        .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK,
        .styles_viewerBadge__1yB5_ {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
        }

        /* hide image fullscreen buttons */
        button[title="View fullscreen"],
        button[title="Fullscreen"],
        button[aria-label="View fullscreen"],
        button[aria-label="Fullscreen"],
        div[data-testid="stImage"] button {
            display: none !important;
            visibility: hidden !important;
        }

        /* -----------------------------
           upload screen
        ----------------------------- */

        .hero-wrap {
            height: 100vh;
            max-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding-top: 0;
            transform: translateY(-24px);
        }

        .hero-title {
            text-align: center;
            font-size: 64px;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -2px;
            margin-bottom: 72px;
            color: var(--orange);
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
            background: var(--upload-bg);
            padding: 0;
            position: relative;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none;
        }

        div[data-testid="stFileUploader"] section:hover {
            background: var(--upload-hover);
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
            color: var(--text-main);
            pointer-events: none;
        }

        div[data-testid="stFileUploader"] section > div {
            padding: 0;
            width: 100%;
            height: 100%;
        }

        div[data-testid="stFileUploaderDropzoneInstructions"],
        div[data-testid="stFileUploader"] button,
        div[data-testid="stFileUploader"] small {
            display: none !important;
        }

        /* -----------------------------
           shared layout
        ----------------------------- */

        .screen-wrap {
            padding-top: 58px;
            max-width: 960px;
        }

        .screen-title {
            font-size: 42px;
            line-height: 1.1;
            font-weight: 700;
            letter-spacing: -1.2px;
            margin-bottom: 26px;
            color: var(--text-main);
        }

        .screen-subtitle {
            font-size: 16px;
            color: var(--text-muted);
            margin-top: -12px;
            margin-bottom: 28px;
            max-width: 760px;
        }

        .status-card {
            border-radius: 14px;
            padding: 13px 18px;
            background: var(--green-bg);
            border: 1px solid var(--green-border);
            color: var(--green-text);
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
            color: var(--text-main);
        }

        .meta-mobile-row {
            display: grid;
            grid-template-columns: 240px 1fr;
            column-gap: 18px;
            align-items: start;
        }

        .meta-divider {
            border-bottom: 1px solid var(--line-soft);
            margin: 5px 0 7px 0;
        }

        .meta-key-text {
            color: var(--text-muted);
            font-size: 16px;
            white-space: nowrap;
        }

        .meta-value-text {
            color: var(--text-main);
            font-size: 16px;
            font-weight: 500;
            text-align: left;
        }

        .soft-line {
            height: 1px;
            background: var(--line-soft);
            width: 100%;
            margin: 0 0 10px 0;
        }

        .center {
            text-align: center;
        }

        /* -----------------------------
           buttons
        ----------------------------- */

        div[data-testid="stButton"] {
            margin-top: 8px !important;
        }

        div[data-testid="stButton"] button {
            height: 68px !important;
            border-radius: 16px !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            border: 1px solid #f2f2f2 !important;
            background: #f2f2f2 !important;
            color: #111111 !important;
        }

        div[data-testid="stButton"] button p {
            font-size: 22px !important;
            font-weight: 900 !important;
            color: #111111 !important;
            white-space: nowrap !important;
        }

        div[data-testid="stButton"] button:hover {
            border-color: var(--orange) !important;
            background: #ffffff !important;
            color: var(--orange) !important;
        }

        div[data-testid="stButton"] button:hover p {
            color: var(--orange) !important;
        }

        div[data-testid="stButton"] button:disabled,
        div[data-testid="stButton"] button[disabled] {
            opacity: 0.45 !important;
            background: #d8d8d8 !important;
            color: #111111 !important;
            border-color: #d8d8d8 !important;
        }

        div[data-testid="stButton"] button:disabled p,
        div[data-testid="stButton"] button[disabled] p {
            color: #111111 !important;
        }

        /* small text actions: rename / ignore / save / cancel */
        button[kind="tertiary"] {
            height: 24px !important;
            min-height: 24px !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            background: transparent !important;
            border-radius: 0 !important;
            color: var(--text-muted) !important;
            box-shadow: none !important;
        }

        button[kind="tertiary"] p {
            font-size: 11px !important;
            font-weight: 700 !important;
            color: var(--text-muted) !important;
            white-space: nowrap !important;
        }

        button[kind="tertiary"]:hover {
            background: transparent !important;
            color: var(--orange) !important;
            border: none !important;
        }

        button[kind="tertiary"]:hover p {
            color: var(--orange) !important;
        }

        /* -----------------------------
           inputs
        ----------------------------- */

        div[data-testid="stTextInput"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stTextInput"] > div {
            margin-top: 30px !important;
            margin-bottom: 0 !important;
        }

        div[data-baseweb="base-input"] {
            width: 100% !important;
        }

        div[data-testid="stTextInput"] input {
            height: 46px !important;
            min-height: 46px !important;
            line-height: 46px !important;
            border-radius: 8px !important;
            border: 0 !important;
            background: rgba(128, 128, 128, 0.10) !important;
            text-align: center !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            color: #111111 !important;
            box-shadow: none !important;
            padding: 0 10px 2px 10px !important;
            overflow: visible !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border: 1px solid var(--blue-focus) !important;
            box-shadow: 0 0 0 1px var(--blue-focus) !important;
            outline: none !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: var(--blue-focus) !important;
            box-shadow: 0 0 0 1px var(--blue-focus) !important;
        }

        input {
            color: #111111 !important;
        }

        div[data-testid="InputInstructions"],
        div[data-testid="stTextInput"] [aria-live="polite"] {
            display: none !important;
        }

        input[aria-label="object name"],
        input[aria-label="missing object name"] {
            text-align: left !important;
            padding-left: 14px !important;
        }

/* -----------------------------
   screen 2: file review
----------------------------- */

.processing-title-block {
    margin-bottom: 46px;
}

.processing-section-title {
    font-size: 19px;
    line-height: 1.05;
    font-weight: 500;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    color: var(--text-main);
    margin: 0 0 22px 0;
}

.pdf-preview-card {
    width: 100%;
    max-width: 500px;
    min-height: 430px;
    border-radius: 14px;
    background: #f2f2f2;
    border: 1px solid var(--line-soft);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.pdf-preview-card img {
    display: block;
    width: 100%;
    height: auto;
}

.pdf-preview-missing {
    flex-direction: column;
    gap: 18px;
    padding: 24px;
}

.pdf-page-mock {
    width: 210px;
    height: 290px;
    background: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 4px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.pdf-line {
    height: 7px;
    width: 70%;
    background: #d8d8d8;
    margin-bottom: 13px;
    border-radius: 10px;
}

.pdf-line.wide {
    width: 90%;
}

.pdf-line.small {
    width: 45%;
}

.pdf-box {
    height: 110px;
    border: 1px solid #d8d8d8;
    margin: 18px 0;
    border-radius: 4px;
}

.pdf-missing-note {
    font-size: 11px;
    line-height: 1.45;
    color: var(--text-muted);
    text-align: center;
}

.preview-filename {
    max-width: 500px;
    margin-top: 10px;
    font-size: 12px;
    color: var(--text-muted);
    text-align: center;
}

/* detected objects */

.detected-objects-list {
    width: 100%;
    max-width: none;
    margin-top: 0;
    margin-bottom: 24px;
}

.detected-object-row {
    display: grid;
    grid-template-columns: 1fr 42px 116px;
    align-items: center;
    min-height: 38px;
    column-gap: 12px;
    border-bottom: 1px solid var(--line-soft);
}

.detected-object-name {
    font-size: 17px;
    line-height: 1.1;
    font-weight: 500;
    text-transform: uppercase;
    color: var(--text-main);
    text-align: left;
}

.detected-qty {
    font-size: 14px;
    line-height: 1.1;
    font-weight: 500;
    color: var(--text-main);
    text-align: center;
}

.detected-actions {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 6px;
    font-size: 11px;
    line-height: 1.1;
    font-weight: 500;
    color: var(--text-muted);
    white-space: nowrap;
}

.detected-actions span {
    display: inline-block;
}

.detected-actions .action-dot {
    color: #c9c9c9;
}

.add-missing-row {
    opacity: 0.48;
}

.add-missing-row .detected-object-name {
    font-size: 14px;
    font-weight: 500;
    text-transform: none;
    color: var(--text-muted);
}

/* project info */

.project-info-small-title {
    margin-top: 14px;
    margin-bottom: 16px;
    font-size: 19px;
    line-height: 1.05;
    font-weight: 500;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    color: var(--text-main);
}

.compact-meta-row {
    grid-template-columns: 132px 1fr;
}

.compact-meta-divider {
    margin: 2px 0 4px 0;
}

.project-info-small-row {
    min-height: 18px;
    max-width: none;
}

.project-info-small-key {
    font-size: 12px !important;
    color: var(--text-muted) !important;
}

.project-info-small-value {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: var(--text-main) !important;
}

.project-info-small-divider {
    max-width: none;
    opacity: 0.7;
}

.review-buttons-spacer {
    height: 18px;
}

        /* -----------------------------
           screen 3: project objects
        ----------------------------- */

        .objects-title-block {
            margin: 0;
            padding: 0;
        }

        .orange-title {
            color: var(--orange) !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
            font-size: 36px !important;
            line-height: 1.04 !important;
            font-weight: 900 !important;
            letter-spacing: -1.2px !important;
            margin: 0 0 28px 0 !important;
            padding: 0 !important;
            max-width: none !important;
        }

        .table-head {
            font-size: 12px;
            font-weight: 700;
            line-height: 1.25;
            color: var(--text-main);
            padding: 10px 0 12px 0;
        }

        .left-head {
            text-align: left;
        }

        .empty-head {
            color: transparent;
        }

        .row-line {
            margin: 8px 0 8px 0;
        }

        .summary-top-line {
            margin: 14px 0 20px 0;
        }

        .summary-bottom-line {
            margin: 22px 0 18px 0;
        }

        .object-cell {
            min-height: 52px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding-top: 24px;
        }

        .object-name {
            font-size: 19px;
            line-height: 1.02;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 7px;
        }

        .object-materials {
            font-size: 11px;
            line-height: 1.28;
            color: var(--text-muted);
        }

        .project-extra-row {
            min-height: 46px;
            padding-top: 36px;
        }

        .table-value {
            height: 42px;
            min-height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding-top: 52px;
            font-size: 14px;
            font-weight: 800;
            color: var(--text-main);
        }

        .suggested-note {
            font-size: 9px;
            font-style: italic;
            line-height: 1.0;
            color: var(--text-muted);
            margin-top: -12px;
            text-align: center;
        }

        .review-button-offset {
            height: 8px;
        }

        .project-summary-cell {
            padding: 22px 0 22px 0;
            min-height: 96px;
        }

        .project-side-summary {
            padding-top: 24px;
        }

        .summary-title {
            font-size: 19px;
            line-height: 1.02;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 18px;
        }

        .summary-number {
            font-size: 17px;
            line-height: 1.0;
            font-weight: 500;
            color: var(--text-main);
        }

        .project-total-cell {
            text-align: left;
        }

        .project-total-number {
            font-size: 27px;
            line-height: 1.0;
            font-weight: 900;
            color: var(--orange);
        }

        /* -----------------------------
           dataframes / proposal leftovers
        ----------------------------- */

        div[data-testid="stDataFrame"] {
            color: var(--text-main);
        }

        .center-cell {
            text-align: center;
        }

        .money-note {
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 4px;
            font-style: italic;
            text-align: center;
        }

        .final-row {
            border-top: 1px solid var(--line-soft);
            border-bottom: 1px solid var(--line-soft);
            padding: 28px 0;
            margin-top: 24px;
            margin-bottom: 22px;
        }

        .final-label {
            color: var(--text-muted);
            font-size: 15px;
            margin-bottom: 8px;
        }

        .final-value {
            color: var(--text-main);
            font-size: 30px;
            font-weight: 900;
        }

        .final-total {
            color: var(--orange);
            font-size: 42px;
            font-weight: 950;
        }

        /* -----------------------------
           responsive
        ----------------------------- */

        @media (max-height: 850px) {
            .screen-wrap {
                padding-top: 34px;
            }

            .screen-title {
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
                height: 58px !important;
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

            .screen-wrap {
                padding-top: 26px;
                max-width: 100%;
            }

            .screen-title {
                font-size: 30px;
                line-height: 1.14;
                margin-bottom: 22px;
            }

            .screen-subtitle {
                font-size: 14px;
            }

            .section-title {
                font-size: 23px;
                margin-top: 18px;
                margin-bottom: 14px;
            }

            .meta-mobile-row {
                display: block;
            }

            .meta-key-text {
                display: block;
                margin-bottom: 4px;
                font-size: 14px;
                white-space: normal;
            }

            .meta-value-text {
                display: block;
                font-size: 14px;
            }

            div[data-testid="stButton"] button {
                height: 58px !important;
            }

            div[data-testid="stButton"] button p {
                font-size: 16px !important;
                font-weight: 900 !important;
            }
        }

        /* hide image fullscreen / toolbar button */
            button[title="View fullscreen"],
            button[title="Fullscreen"],
            button[aria-label="View fullscreen"],
            button[aria-label="Fullscreen"] {
                display: none !important;
            }

            div[data-testid="stImage"] button {
                display: none !important;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# helpers
# -----------------------------

def nav_buttons(back_screen: str | None, next_screen: str | None, next_label: str = "Continue"):
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    if back_screen:
        if col1.button("Back", key=f"nav_back_{back_screen}_{next_screen}", use_container_width=True):
            st.session_state.screen = back_screen
            st.rerun()
    else:
        col1.empty()

    if next_screen:
        if col2.button(next_label, key=f"nav_next_{back_screen}_{next_screen}", use_container_width=True):
            st.session_state.screen = next_screen
            st.rerun()
    else:
        col2.empty()


def render_screen_header(title: str, subtitle: str | None = None):
    st.markdown('<div class="screen-wrap">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="screen-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            f"""
            <div class="screen-subtitle">
                {subtitle}
            </div>
            """,
            unsafe_allow_html=True,
        )


def format_money(value):
    if value is None:
        return "—"

    formatted = f"{int(value):,}".replace(",", "\u00A0")
    return f"₪{formatted}"


def parse_money_input(value, fallback=0):
    if value is None:
        return fallback

    digits = "".join(ch for ch in str(value) if ch.isdigit())

    if not digits:
        return fallback

    return int(digits)

def normalize_money_state(key, fallback=0):
    value = parse_money_input(st.session_state.get(key), fallback=fallback)
    st.session_state[key] = format_money(value)


# -----------------------------
# screens
# -----------------------------

def render_upload_screen():
    st.markdown(
        """
        <style>
        html, body {
            height: 100% !important;
            overflow: hidden !important;
        }

        .stApp,
        div[data-testid="stAppViewContainer"],
        section.main {
            height: 100vh !important;
            max-height: 100vh !important;
            overflow: hidden !important;
        }

        .block-container {
            height: 100vh !important;
            max-height: 100vh !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            overflow: hidden !important;
        }

        .landing-title {
            text-align: center;
            font-size: 64px;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -2px;
            margin: 150px 0 72px 0;
            color: var(--orange);
        }

        div[data-testid="stFileUploader"] {
            flex: 0 0 auto !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="landing-title">
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

    if uploaded_file is not None:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.uploaded_file_size = uploaded_file.size
        st.session_state.uploaded_file_type = detect_file_type(uploaded_file.name)
        st.session_state.screen = "processing"
        st.rerun()

def render_estimate_processing_screen():
    render_screen_header("Preparing object estimates")

    progress = st.progress(0)
    status_placeholder = st.empty()

    steps = [
        "Decomposing detected objects...",
        "Mapping materials and consumables...",
        "Estimating carpentry and metal work...",
        "Estimating labor processes...",
        "Allocating equipment and machine costs...",
        "Allocating workshop overhead...",
        "Preparing object-level sale price inputs...",
        "Estimate workspace ready.",
    ]

    for i, step in enumerate(steps, start=1):
        status_placeholder.markdown(
            f"<div class='status-card'>{step}</div>",
            unsafe_allow_html=True,
        )
        progress.progress(i / len(steps))
        time.sleep(0.5)

    st.session_state.screen = "objects"
    st.rerun()


def render_processing_screen():
    ensure_detection_state()

    if "metadata_extracted" not in st.session_state:
        st.session_state.metadata_extracted = False

    if not st.session_state.metadata_extracted:
        render_screen_header("Reading your RFQ package")

        progress = st.progress(0)
        status_placeholder = st.empty()

        steps = [
            "Detecting file type...",
            "Reading title block...",
            "Extracting project metadata...",
            "Detecting drawing pages...",
            "Identifying project objects...",
            "Project metadata extracted.",
        ]

        for i, step in enumerate(steps, start=1):
            status_placeholder.markdown(
                f"<div class='status-card'>{step}</div>",
                unsafe_allow_html=True,
            )
            progress.progress(i / len(steps))
            time.sleep(0.45)

        st.session_state.metadata_extracted = True
        st.rerun()

    st.markdown(
        "<div class='screen-block processing-title-block'>"
        "<h1 class='screen-title'>File review</h1>"
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            "<div class='processing-section-title'>Preview</div>",
            unsafe_allow_html=True,
        )

        preview_path = Path("assets/pdf_preview.png")

        if preview_path.exists():
            st.image(str(preview_path), width=500)
        else:
            st.markdown(
                "<div class='pdf-preview-card pdf-preview-missing'>"
                "<div class='pdf-page-mock'>"
                "<div class='pdf-line wide'></div>"
                "<div class='pdf-line'></div>"
                "<div class='pdf-box'></div>"
                "<div class='pdf-line small'></div>"
                "<div class='pdf-line'></div>"
                "</div>"
                "<div class='pdf-missing-note'>add preview image:<br>assets/pdf_preview.png</div>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='preview-filename'>RA-N01_20260216.pdf</div>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            "<div class='processing-section-title'>Detected objects</div>",
            unsafe_allow_html=True,
        )

        rows_html = ""

        for object_key, obj in list(st.session_state.objects.items()):
            current_name = st.session_state.detected_object_names.get(object_key, obj["name"])
            qty = obj.get("qty", 1)

            rows_html += (
                "<div class='detected-object-row'>"
                f"<div class='detected-object-name'>{current_name}</div>"
                f"<div class='detected-qty'>{qty}</div>"
                "<div class='detected-actions'>"
                "<span>rename</span>"
                "<span class='action-dot'>·</span>"
                "<span>ignore</span>"
                "</div>"
                "</div>"
            )

        rows_html += (
            "<div class='detected-object-row add-missing-row'>"
            "<div class='detected-object-name'>+ Add missing object</div>"
            "<div class='detected-qty'></div>"
            "<div class='detected-actions'></div>"
            "</div>"
        )

        st.markdown(
            "<div class='detected-objects-list'>" + rows_html + "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='project-info-small-title'>Project info</div>",
            unsafe_allow_html=True,
        )

        for key, value in project_metadata():
            if key == "Detected objects":
                continue

            st.markdown(
                "<div class='meta-mobile-row compact-meta-row project-info-small-row'>"
                f"<span class='meta-key-text project-info-small-key'>{key}:</span>"
                f"<span class='meta-value-text project-info-small-value'>{value}</span>"
                "</div>"
                "<div class='meta-divider compact-meta-divider project-info-small-divider'></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='review-buttons-spacer'></div>", unsafe_allow_html=True)

    b0, b1 = st.columns([1, 1])

    with b0:
        if st.button("Back", key="processing_back", use_container_width=True):
            st.session_state.metadata_extracted = False
            st.session_state.screen = "upload"
            st.rerun()

    with b1:
        if st.button(
            "Confirm object detection → Estimate",
            key="confirm_objects_continue",
            use_container_width=True,
        ):
            for object_key, name in st.session_state.detected_object_names.items():
                if object_key in st.session_state.objects:
                    st.session_state.objects[object_key]["name"] = name

            st.session_state.screen = "estimate_processing"
            st.rerun()


def render_objects_screen():
    ensure_objects_state()

    demo_costs = object_demo_costs()

    st.markdown(
        """
        <div class="screen-block objects-title-block">
            <div class="orange-title">
                <div>Review each object →</div>
                <div>Set sale price per unit →</div>
                <div>Generate proposal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    object_col_weights = [1.58, 0.46, 1.06, 1.32, 1.15, 0.06, 0.98]

    h0, h1, h2, h3, h4, h_spacer, h5 = st.columns(object_col_weights)

    with h0:
        st.markdown("<div class='table-head left-head'>project objects</div>", unsafe_allow_html=True)
    with h1:
        st.markdown("<div class='table-head center'>quantity</div>", unsafe_allow_html=True)
    with h2:
        st.markdown("<div class='table-head center'>self cost<br>per unit</div>", unsafe_allow_html=True)
    with h3:
        st.markdown("<div class='table-head center'>sale price<br>per unit</div>", unsafe_allow_html=True)
    with h4:
        st.markdown("<div class='table-head center'>sale price<br>total</div>", unsafe_allow_html=True)
    with h_spacer:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with h5:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("<div class='soft-line'></div>", unsafe_allow_html=True)

    objects_subtotal = 0

    for object_key, obj in st.session_state.objects.items():
        cost = demo_costs.get(object_key, {})
        unit_cost = cost.get("unit_cost", obj.get("unit_cost") or 0)
        suggested_price = cost.get("suggested_price", obj.get("suggested_price") or 0)

        obj["unit_cost"] = unit_cost
        obj["suggested_price"] = suggested_price

        input_key = f"sale_price_input_{object_key}"

        if input_key not in st.session_state:
            current_sale_price = obj.get("sale_price") or suggested_price
            st.session_state[input_key] = format_money(current_sale_price)

        c0, c1, c2, c3, c4, c_spacer, c5 = st.columns(object_col_weights)

        with c0:
            st.markdown(
                f"""
                <div class="object-cell">
                    <div class="object-name">{obj["name"]}</div>
                    <div class="object-materials">{obj["materials"][0]}</div>
                    <div class="object-materials">{obj["materials"][1]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c1:
            st.markdown(
                f"<div class='table-value center'>{obj['qty']}</div>",
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"<div class='table-value center'>{format_money(unit_cost)}</div>",
                unsafe_allow_html=True,
            )

        with c3:
            sale_price_raw = st.text_input(
                "sale price per unit",
                key=input_key,
                label_visibility="collapsed",
                on_change=normalize_money_state,
                args=(input_key, suggested_price),
            )
            sale_price = parse_money_input(sale_price_raw, suggested_price)
            obj["sale_price"] = sale_price

            st.markdown(
                "<div class='suggested-note center'>suggested: SC + 30%</div>",
                unsafe_allow_html=True,
            )

        sale_price_total = sale_price * obj["qty"]
        objects_subtotal += sale_price_total

        with c4:
            st.markdown(
                f"<div class='table-value center'>{format_money(sale_price_total)}</div>",
                unsafe_allow_html=True,
            )

        with c_spacer:
            st.markdown("&nbsp;", unsafe_allow_html=True)

        with c5:
            st.markdown("<div class='review-button-offset'></div>", unsafe_allow_html=True)

            if st.button("Review", key=f"review_{object_key}", use_container_width=True):
                st.session_state.current_object = object_key
                st.session_state.screen = "object_detail"
                st.rerun()

        st.markdown("<div class='soft-line row-line'></div>", unsafe_allow_html=True)

    delivery_suggested = round(objects_subtotal * 0.03)
    installation_suggested = round(objects_subtotal * 0.10)

    if "delivery_price_input" not in st.session_state:
        st.session_state.delivery_price_input = format_money(delivery_suggested)

    if "installation_price_input" not in st.session_state:
        st.session_state.installation_price_input = format_money(installation_suggested)

    extra_row_weights = [1.58, 1.52, 0.90, 0.82, 1.68, 0.98]

    d0, d1, d2, d3, d4, d5 = st.columns(extra_row_weights)

    with d0:
        st.markdown(
            """
            <div class="object-cell project-extra-row">
                <div class="object-name">Delivery</div>
                <div class="object-materials">project-level cost</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with d1:
        delivery_raw = st.text_input(
            "delivery",
            key="delivery_price_input",
            label_visibility="collapsed",
            on_change=normalize_money_state,
            args=("delivery_price_input", delivery_suggested),
        )
        delivery_price = parse_money_input(delivery_raw, delivery_suggested)

        st.markdown(
            "<div class='suggested-note center'>suggested: 3% of objects subtotal</div>",
            unsafe_allow_html=True,
        )

    with d2:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with d3:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with d4:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with d5:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("<div class='soft-line row-line'></div>", unsafe_allow_html=True)

    i0, i1, i2, i3, i4, i5 = st.columns(extra_row_weights)

    with i0:
        st.markdown(
            """
            <div class="object-cell project-extra-row">
                <div class="object-name">Installation</div>
                <div class="object-materials">project-level cost</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with i1:
        installation_raw = st.text_input(
            "installation",
            key="installation_price_input",
            label_visibility="collapsed",
            on_change=normalize_money_state,
            args=("installation_price_input", installation_suggested),
        )
        installation_price = parse_money_input(installation_raw, installation_suggested)

        st.markdown(
            "<div class='suggested-note center'>suggested: 10% of objects subtotal</div>",
            unsafe_allow_html=True,
        )

    with i2:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with i3:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with i4:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with i5:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("<div class='soft-line summary-top-line'></div>", unsafe_allow_html=True)

    project_price = objects_subtotal + delivery_price + installation_price
    vat = round(project_price * VAT_RATE)
    total = project_price + vat

    st.session_state.project_price = project_price
    st.session_state.vat = vat
    st.session_state.total_price = total
    st.session_state.delivery_price = delivery_price
    st.session_state.installation_price = installation_price

    s0, s1, s_spacer, s2 = st.columns([1.28, 1.05, 1.38, 0.98])

    with s0:
        st.markdown(
            f"""
            <div class="project-summary-cell project-side-summary">
                <div class="summary-title">Project Price</div>
                <div class="summary-number">{format_money(project_price)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s1:
        st.markdown(
            f"""
            <div class="project-summary-cell project-side-summary">
                <div class="summary-title">VAT 18%</div>
                <div class="summary-number">{format_money(vat)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s_spacer:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with s2:
        st.markdown(
            f"""
            <div class="project-summary-cell project-total-cell">
                <div class="summary-title">Project Total</div>
                <div class="summary-number project-total-number">{format_money(total)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='soft-line summary-bottom-line'></div>", unsafe_allow_html=True)

    b0, b1 = st.columns([1, 1])

    with b0:
        if st.button("Back", key="objects_back", use_container_width=True):
            st.session_state.screen = "processing"
            st.rerun()

    with b1:
        if st.button("Generate proposal", key="generate_proposal", use_container_width=True):
            st.session_state.screen = "proposal"
            st.rerun()


def render_object_detail_screen():
    ensure_objects_state()

    object_key = st.session_state.get("current_object", "kitchen")
    obj = st.session_state.objects.get(object_key, st.session_state.objects["kitchen"])

    render_screen_header(
        f"Object estimate: {obj['name']}",
        "Review materials, labor and cost blocks. Approve object cost to return to project summary.",
    )

    st.markdown("### Preview")
    st.markdown(
        f"""
        <div class="summary-box">
            Preview placeholder for <b>{obj["name"]}</b> from drawing package.
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_key = object_key if object_key in object_demo_costs() else "kitchen"

    st.markdown("### Materials and consumables")
    st.dataframe(object_materials(base_key), use_container_width=True, hide_index=True)

    st.markdown("### Labor processes")
    st.dataframe(object_labor(base_key), use_container_width=True, hide_index=True)

    st.markdown("### Cost breakdown")
    breakdown = object_cost_breakdown(base_key)
    st.dataframe(breakdown, use_container_width=True, hide_index=True)

    demo_costs = object_demo_costs()[base_key]
    unit_cost = demo_costs["unit_cost"]
    suggested_price = demo_costs["suggested_price"]
    sale_price = suggested_price

    c1, c2, c3 = st.columns(3)
    c1.metric("Unit cost", format_money(unit_cost))
    c2.metric("Suggested price", format_money(suggested_price))
    c3.metric("Default sale price", format_money(sale_price))

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    if col1.button("Back to objects", key=f"back_to_objects_{object_key}", use_container_width=True):
        st.session_state.screen = "objects"
        st.rerun()

    if col2.button(f"Approve {obj['name']}", key=f"approve_object_{object_key}", use_container_width=True):
        st.session_state.objects[object_key]["approved"] = True
        st.session_state.objects[object_key]["unit_cost"] = unit_cost
        st.session_state.objects[object_key]["suggested_price"] = suggested_price
        st.session_state.objects[object_key]["sale_price"] = sale_price
        st.session_state.screen = "objects"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_proposal_screen():
    ensure_objects_state()

    render_screen_header(
        "Proposal preview",
        "Client-facing draft generated from approved objects and project-level pricing.",
    )

    objects = st.session_state.objects
    final_price = st.session_state.get(
        "final_price",
        sum(obj["sale_price"] or 0 for obj in objects.values()) + 3500 + 12000,
    )

    proposal = f"""
# Commercial proposal

**Project:** RA-N01  
**Company:** {COMPANY_NAME}  
**Prepared from:** RA-N01_20260216.pdf  

## Scope included

- Kitchen
- Kitchen island
- Wall shelf
- delivery and installation

## Object pricing

| object | qty | sale price |
|---|---:|---:|
| Kitchen | 1 | {format_money(objects["kitchen"]["sale_price"])} |
| Kitchen island | 1 | {format_money(objects["kitchen_island"]["sale_price"])} |
| Wall shelf | 1 | {format_money(objects["wall_shelf"]["sale_price"])} |

## Project-level pricing

| line | price |
|---|---:|
| Delivery | {format_money(st.session_state.get("delivery", 0))} |
| Installation | {format_money(st.session_state.get("installation", 0))} |
| VAT 18% | {format_money(st.session_state.get("vat_amount", 0))} |

## Final proposal price

**{format_money(final_price)}**

## Assumptions

- final site measurement is required before production release
- stainless steel supplier / sample must be confirmed
- stone supplier, slab thickness and cutouts must be confirmed
- handle quantity must be verified
- appliance, sink and ventilation cutouts must be confirmed
- installation assumes standard access, elevator availability and regular working hours

## Not included

- electrical work
- plumbing
- stone supplier price changes after quotation
- special lifting / crane / non-standard access
- after-hours installation
- changes after production approval
"""

    st.markdown(proposal)

    st.markdown("### Purchasing list")
    purchasing = pd.DataFrame(
        [
            ["panel", "MDF / formica-related boards", "allowance", "kitchen, island", "buy / verify"],
            ["metal", "stainless steel sheets / panels", "allowance", "kitchen, island", "quote supplier"],
            ["stone", "stone marble laba rosa", "allowance", "kitchen island", "quote supplier"],
            ["finish", "oak veneer nextdoor", "allowance", "wall shelf", "verify sample"],
            ["metal", "corten / tin corten", "allowance", "wall shelf", "quote supplier"],
            ["hardware", "handles / hinges / slides", "lot", "kitchen, island", "verify quantity"],
            ["consumables", "glue / screws / sanding / protection", "lot", "all objects", "check stock"],
            ["packing", "foam / cardboard / stretch film", "lot", "all objects", "check stock"],
        ],
        columns=["category", "item", "qty / basis", "used in", "status"],
    )
    st.dataframe(purchasing, use_container_width=True, hide_index=True)

    st.markdown("### Production summary")
    production = pd.DataFrame(
        [
            ["estimator / PM", 7],
            ["carpenter", 74],
            ["CNC / machining", 14],
            ["metal coordination", 8],
            ["packing", 9],
            ["installation", 24],
        ],
        columns=["role / department", "hours"],
    )
    st.dataframe(production, use_container_width=True, hide_index=True)

    nav_buttons("objects", None)

    if st.button("Start over", key="proposal_start_over", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# router
# -----------------------------

apply_css()

if "screen" not in st.session_state:
    st.session_state.screen = "upload"

if st.session_state.screen == "upload":
    render_upload_screen()
elif st.session_state.screen == "processing":
    render_processing_screen()
elif st.session_state.screen == "estimate_processing":
    render_estimate_processing_screen()
elif st.session_state.screen == "objects":
    render_objects_screen()
elif st.session_state.screen == "object_detail":
    render_object_detail_screen()
elif st.session_state.screen == "proposal":
    render_proposal_screen()
else:
    st.session_state.screen = "upload"
    st.rerun()