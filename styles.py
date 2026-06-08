import streamlit as st

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
    margin-top: 4px;
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