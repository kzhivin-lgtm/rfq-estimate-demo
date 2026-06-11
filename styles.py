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
            --blue-focus: #2f80ed;
            --error: #d94c4c;

            --button-bg: #f2f2f2;
            --button-border: #f2f2f2;
            --button-text: #111111;

            --success-soft-bg: #eaf7ee;
            --success-soft-hover: #dff2e5;
            --success-soft-border: #cfead7;
            --success-soft-hover-border: #bfe2ca;
            --success-soft-text: #255c35;

            --success-strong-bg: #2f9e44;
            --success-strong-hover: #26883a;
            --success-strong-text: #ffffff;

            --card-bg: #ffffff;
            --card-border: #e8e8e8;
            --soft-bg: #f7f7f7;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #0e1117;
                --text-main: #f2f2f2;
                --text-muted: #b8b8b8;
                --line-soft: #343842;

                --upload-bg: #1c202a;
                --upload-hover: #252a36;

                --button-bg: #f2f2f2;
                --button-border: #f2f2f2;
                --button-text: #111111;

                --success-soft-bg: #10291a;
                --success-soft-hover: #163520;
                --success-soft-border: #245738;
                --success-soft-hover-border: #2d6a45;
                --success-soft-text: #b8f3c9;

                --success-strong-bg: #2f9e44;
                --success-strong-hover: #26883a;
                --success-strong-text: #ffffff;

                --card-bg: #121722;
                --card-border: #303746;
                --soft-bg: #161a23;
            }
        }

        html,
        body,
        [class*="css"],
        .stApp {
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
            background: var(--success-soft-bg);
            border: 1px solid var(--success-soft-border);
            color: var(--success-soft-text);
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

        .soft-line {
            height: 1px;
            background: var(--line-soft);
            width: 100%;
            margin: 0 0 10px 0;
        }

        .center {
            text-align: center;
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

        /* -----------------------------
           progress
        ----------------------------- */

        div[data-testid="stProgress"] div[role="progressbar"] {
            background-color: var(--blue-focus) !important;
        }

        div[data-testid="stProgress"] div[role="progressbar"] > div {
            background-color: var(--orange) !important;
        }

        .stProgress > div > div > div {
            background-color: var(--blue-focus) !important;
        }

        .stProgress > div > div > div > div {
            background-color: var(--orange) !important;
        }

        div[data-testid="stProgress"] * {
            border-color: var(--orange) !important;
        }

        div[data-testid="stProgress"] div[style*="background-color"] {
            background-color: var(--orange) !important;
        }

        /* -----------------------------
           buttons
        ----------------------------- */

        div[data-testid="stButton"],
        div[data-testid="stDownloadButton"] {
            width: 100% !important;
            margin-top: 8px !important;
        }

        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {
            width: 100% !important;
            height: 68px !important;
            min-height: 68px !important;
            max-height: 68px !important;
            padding: 0 !important;
            border-radius: 16px !important;
            border: 1px solid var(--button-border) !important;
            background: var(--button-bg) !important;
            color: var(--button-text) !important;
            box-sizing: border-box !important;
            box-shadow: none !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            line-height: 68px !important;
        }

        div[data-testid="stButton"] button p,
        div[data-testid="stDownloadButton"] button p {
            margin: 0 !important;
            padding: 0 !important;
            color: var(--button-text) !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            line-height: 68px !important;
            white-space: nowrap !important;
        }

        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            border-color: var(--orange) !important;
            background: #ffffff !important;
            color: var(--orange) !important;
        }

        div[data-testid="stButton"] button:hover p,
        div[data-testid="stDownloadButton"] button:hover p {
            color: var(--orange) !important;
        }

        div[data-testid="stButton"] button:disabled,
        div[data-testid="stButton"] button[disabled],
        div[data-testid="stDownloadButton"] button:disabled,
        div[data-testid="stDownloadButton"] button[disabled] {
            opacity: 0.45 !important;
            background: #d8d8d8 !important;
            color: #111111 !important;
            border-color: #d8d8d8 !important;
        }

        div[data-testid="stButton"] button:disabled p,
        div[data-testid="stButton"] button[disabled] p,
        div[data-testid="stDownloadButton"] button:disabled p,
        div[data-testid="stDownloadButton"] button[disabled] p {
            color: #111111 !important;
        }

        /* Regular primary buttons: object Done state. */
        div[data-testid="stButton"] button[kind="primary"] {
            background: var(--success-soft-bg) !important;
            border-color: var(--success-soft-border) !important;
            color: var(--success-soft-text) !important;
        }

        div[data-testid="stButton"] button[kind="primary"] p {
            color: var(--success-soft-text) !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            background: var(--success-soft-hover) !important;
            border-color: var(--success-soft-hover-border) !important;
            color: var(--success-soft-text) !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover p {
            color: var(--success-soft-text) !important;
        }

        /* Download primary button: final proposal generated state. */
        div[data-testid="stDownloadButton"] button[kind="primary"] {
            background: var(--success-strong-bg) !important;
            border-color: var(--success-strong-bg) !important;
            color: var(--success-strong-text) !important;
        }

        div[data-testid="stDownloadButton"] button[kind="primary"] p {
            color: var(--success-strong-text) !important;
        }

        div[data-testid="stDownloadButton"] button[kind="primary"]:hover {
            background: var(--success-strong-hover) !important;
            border-color: var(--success-strong-hover) !important;
            color: var(--success-strong-text) !important;
        }

        div[data-testid="stDownloadButton"] button[kind="primary"]:hover p {
            color: var(--success-strong-text) !important;
        }

        button[kind="tertiary"] {
            width: auto !important;
            height: 24px !important;
            min-height: 24px !important;
            max-height: 24px !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            background: transparent !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            color: var(--text-muted) !important;
        }

        button[kind="tertiary"] p {
            margin: 0 !important;
            padding: 0 !important;
            color: var(--text-muted) !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            line-height: 24px !important;
            white-space: nowrap !important;
        }

        button[kind="tertiary"]:hover {
            background: transparent !important;
            border: none !important;
            color: var(--orange) !important;
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

        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {
            width: 100% !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }

        div[data-baseweb="input"]:hover,
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="base-input"]:hover,
        div[data-baseweb="base-input"]:focus-within {
            background: #ffffff !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextInput"] input:hover,
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextInput"] input:active {
            height: 46px !important;
            min-height: 46px !important;
            line-height: 46px !important;
            border-radius: 8px !important;
            border: 1px solid transparent !important;
            background: #ffffff !important;
            text-align: center !important;
            font-size: 18px !important;
            font-weight: 900 !important;
            color: #111111 !important;
            box-shadow: none !important;
            padding: 0 10px 2px 10px !important;
            overflow: visible !important;
            outline: none !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: var(--blue-focus) !important;
            box-shadow: 0 0 0 1px var(--blue-focus) !important;
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
            margin-bottom: 28px;
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
            margin: 8px 0 18px 0;
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
            text-align: right;
        }

        .project-total-number {
            font-size: 27px;
            line-height: 1.0;
            font-weight: 900;
            color: var(--orange);
        }

        .project-summary-download-row {
            min-height: 27px !important;
            display: flex !important;
            align-items: center !important;
        }

        .project-summary-download-link {
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
            text-decoration: none !important;
            font-size: 17px !important;
            line-height: 1 !important;
            font-weight: 800 !important;
            color: var(--orange) !important;
        }

        .project-summary-download-link:hover {
            color: var(--orange) !important;
            text-decoration: underline !important;
        }

        .project-summary-download-link.locked {
            color: var(--text-muted) !important;
            opacity: 0.62 !important;
            text-decoration: none !important;
        }

        .project-summary-download-link.locked:hover {
            color: var(--text-muted) !important;
            opacity: 0.82 !important;
            text-decoration: underline !important;
        }

        .project-summary-pdf-icon {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 28px !important;
            height: 19px !important;
            border-radius: 4px !important;
            background: var(--orange) !important;
            color: #ffffff !important;
            font-size: 9px !important;
            font-weight: 900 !important;
            letter-spacing: 0.2px !important;
        }

        .project-summary-download-link.locked .project-summary-pdf-icon {
            background: #b8b8b8 !important;
        }

        .project-summary-download-missing {
            font-size: 15px !important;
            font-weight: 800 !important;
            color: var(--text-muted) !important;
        }

        .review-required-error {
            margin: 10px 0 0 0 !important;
            padding: 10px 12px !important;
            border: 1.5px solid #f1b3a5 !important;
            border-radius: 10px !important;
            background: #fff3ef !important;
            color: #c34828 !important;
            font-size: 13px !important;
            font-weight: 800 !important;
            line-height: 1.15 !important;
            text-align: left !important;
        }

        .review-required-error-wide {
            display: none !important;
            width: 100% !important;
            margin: 10px 0 0 0 !important;
            padding: 14px 18px !important;
            border: 2px solid #ef8f78 !important;
            border-radius: 12px !important;
            background: #fff0eb !important;
            color: #c33a1d !important;
            font-size: 16px !important;
            font-weight: 900 !important;
            line-height: 1.2 !important;
            text-align: left !important;
        }

        .review-required-error-wide.visible,
        #review-required-message:target {
            display: block !important;
        }

        /* -----------------------------
           dataframes / proposal leftovers
        ----------------------------- */

        div[data-testid="stDataFrame"] {
            color: var(--text-main);
            margin-bottom: 4px !important;
        }

        div[data-testid="stDataFrame"] div[role="gridcell"],
        div[data-testid="stDataFrame"] div[role="columnheader"] {
            font-size: 12px !important;
        }

        div[data-testid="stDataFrame"] div[role="columnheader"] {
            font-weight: 800 !important;
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
           object detail card
        ----------------------------- */

        .object-detail-title-block {
            margin-bottom: 36px;
        }

        .object-card-section-title {
            font-size: 24px;
            line-height: 1.05;
            font-weight: 800;
            color: var(--text-main);
            margin: 0 0 18px 0;
        }

        .object-card-section-spaced {
            margin-top: 44px;
        }

        .object-meta-line {
            display: flex;
            gap: 34px;
            align-items: center;
            font-size: 22px;
            line-height: 1.05;
            font-weight: 800;
            color: var(--text-main);
            margin: 20px 0 24px 0;
        }

        .object-section-header {
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            align-items: end;
            column-gap: 24px;
            margin: 26px 0 8px 0;
        }

        .object-section-title {
            font-size: 20px;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: 0.2px;
            color: var(--text-main);
        }

        .object-section-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr 1.15fr;
            column-gap: 16px;
            align-items: end;
        }

        .object-section-metric-label {
            font-size: 11px;
            line-height: 1.05;
            color: var(--text-muted);
            margin-bottom: 5px;
        }

        .object-section-metric-value {
            font-size: 18px;
            line-height: 1;
            font-weight: 800;
            color: var(--text-main);
        }

        .object-section-metric-total .object-section-metric-value {
            color: var(--orange);
            font-size: 22px;
            font-weight: 900;
        }

        .object-cost-summary {
            margin-top: 26px;
            display: grid;
            grid-template-columns: 1fr 1fr 1.2fr;
            column-gap: 18px;
            align-items: stretch;
        }

        .object-cost-cell {
            border-top: 1px solid var(--line-soft);
            padding-top: 18px;
        }

        .object-cost-label {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 10px;
        }

        .object-cost-value {
            font-size: 24px;
            line-height: 1;
            font-weight: 900;
            color: var(--text-main);
        }

        .object-cost-total .object-cost-value {
            color: var(--orange);
            font-size: 32px;
        }

        .object-final-summary {
            margin-top: 30px;
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            column-gap: 24px;
            align-items: end;
        }

        .object-final-title {
            font-size: 24px;
            line-height: 1.05;
            font-weight: 900;
            color: var(--text-main);
        }

        .object-final-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr 1.2fr;
            column-gap: 16px;
            align-items: end;
        }

        .object-final-label {
            font-size: 11px;
            line-height: 1.05;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .object-final-value {
            font-size: 20px;
            line-height: 1;
            font-weight: 800;
            color: var(--text-main);
        }

        .object-final-total {
            font-size: 30px;
            font-weight: 950;
            color: var(--orange);
        }

        .object-detail-buttons-spacer {
            height: 26px;
        }

        div[data-testid="stExpander"] {
            border: 0 !important;
            box-shadow: none !important;
            margin: 2px 0 !important;
        }

        div[data-testid="stExpander"] details {
            border: 0 !important;
        }

        div[data-testid="stExpander"] summary {
            padding: 4px 0 !important;
            font-size: 12px !important;
            color: var(--text-muted) !important;
        }

        div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
            padding: 2px 0 8px 0 !important;
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

            div[data-testid="stButton"] button,
            div[data-testid="stDownloadButton"] button {
                height: 58px !important;
                min-height: 58px !important;
                max-height: 58px !important;
                line-height: 58px !important;
            }

            div[data-testid="stButton"] button p,
            div[data-testid="stDownloadButton"] button p {
                font-size: 19px !important;
                line-height: 58px !important;
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

            div[data-testid="stButton"] button,
            div[data-testid="stDownloadButton"] button {
                height: 58px !important;
                min-height: 58px !important;
                max-height: 58px !important;
                line-height: 58px !important;
            }

            div[data-testid="stButton"] button p,
            div[data-testid="stDownloadButton"] button p {
                font-size: 16px !important;
                font-weight: 900 !important;
                line-height: 58px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
