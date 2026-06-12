# RFQ-to-Estimate Demo — app.py
#
# Formatting-only cleanup of the old Streamlit app code.
# Business logic, formulas, session_state keys, routing, widget keys,
# and hardcoded demo values are intentionally preserved.

import base64
import re
import time
from pathlib import Path
from textwrap import dedent

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    from st_aggrid import (
        AgGrid,
        DataReturnMode,
        GridOptionsBuilder,
        GridUpdateMode,
        JsCode,
    )
except ImportError:
    AgGrid = None
    DataReturnMode = None
    GridOptionsBuilder = None
    GridUpdateMode = None
    JsCode = None

from styles import apply_css
from pricing import format_money, parse_money_input, normalize_money_state

from estimate_config import (
    VAT_RATE,
    EMPLOYER_LOAD_RATE,
    SALE_PRICE_MARKUP_RATE,
    LABOR_CONTINGENCY_RATE,
    WARRANTY_RESERVE_RATE,
    MANAGEMENT_BUFFER_RATE,
    DESIGN_BUREAU_COMMISSION_RATE,
    PRODUCTION_WORKERS,
    WORKDAYS_PER_MONTH,
    HOURS_PER_DAY,
    ROLE_RATES,
    MONTHLY_OVERHEAD_ROWS,
    DELIVERY_RATE,
    INSTALLATION_RATE,
)
from objects.kitchen import (
    kitchen_materials_rows,
    kitchen_labor_rows,
    kitchen_overhead_rows,
)

from objects.kitchen_island import (
    kitchen_island_materials_rows,
    kitchen_island_labor_rows,
    kitchen_island_overhead_rows,
)

from objects.wall_shelf import (
    wall_shelf_materials_rows,
    wall_shelf_labor_rows,
    wall_shelf_overhead_rows,
)

st.set_page_config(
    page_title="RFQ-to-Estimate Demo",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


COMPANY_NAME = "8DOOR"

OBJECT_DETAIL_CONFIG = {
    "kitchen": {
        "state_prefix": "kitchen",
        "self_cost_title": "KITCHEN SELF COST",
        "approve_label": "Approve kitchen estimate",
        "preview_path": "assets/kitchen_preview.png",
        "confidence": 93,
        "materials_rows": kitchen_materials_rows,
        "labor_rows": kitchen_labor_rows,
        "overhead_rows": kitchen_overhead_rows,
    },
    "kitchen_island": {
        "state_prefix": "kitchen_island",
        "self_cost_title": "KITCHEN ISLAND SELF COST",
        "approve_label": "Approve kitchen island estimate",
        "preview_path": "assets/kitchen_island_preview.png",
        "confidence": 89,
        "materials_rows": kitchen_island_materials_rows,
        "labor_rows": kitchen_island_labor_rows,
        "overhead_rows": kitchen_island_overhead_rows,
    },

        "wall_shelf": {
        "state_prefix": "wall_shelf",
        "self_cost_title": "WALL SHELF SELF COST",
        "approve_label": "Approve wall shelf estimate",
        "preview_path": "assets/wall_shelf_preview.png",
        "confidence": 95,
        "materials_rows": wall_shelf_materials_rows,
        "labor_rows": wall_shelf_labor_rows,
        "overhead_rows": wall_shelf_overhead_rows,
    },
}

# -----------------------------------------------------------------------------
# Static demo data and object defaults
# -----------------------------------------------------------------------------

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


def suggested_sale_price(self_cost):
    return round(self_cost * (1 + SALE_PRICE_MARKUP_RATE))


def suggested_markup_label():
    return f"suggested: SC + {int(SALE_PRICE_MARKUP_RATE * 100)}%"

def project_level_self_costs():
    return {
        "delivery": 1400,
        "installation": 5800,
    }


def locked_demo_values():
    return {
        "objects": {
            "kitchen": {
                "unit_cost": 29925,
                "suggested_price": 38902,
            },
            "kitchen_island": {
                "unit_cost": 33363,
                "suggested_price": 43372,
            },
            "wall_shelf": {
                "unit_cost": 19904,
                "suggested_price": 25875,
            },
        },
        "project_level_prices": {
            "delivery": 3244,
            "installation": 10815,
        },
    }


def object_demo_costs():
    def estimate_initial_self_cost_excl_vat(object_key: str) -> int:
        config = OBJECT_DETAIL_CONFIG.get(object_key)

        if not config:
            return 0

        materials_cost = round(
            sum(
                row["unit_price"] * row["qty"]
                for row in config["materials_rows"]()
            )
        )

        direct_labor_cost = sum(
            row["hours"] * row["rate"]
            for row in config["labor_rows"]()
        )
        labor_base = round(direct_labor_cost * (1 + LABOR_CONTINGENCY_RATE))
        employer_load = round(labor_base * EMPLOYER_LOAD_RATE)
        labor_total = labor_base + employer_load

        overhead_cost = round(
            sum(
                row["object_cost"]
                for row in config["overhead_rows"]()
            )
        )

        return materials_cost + labor_total + overhead_cost

    return {
        object_key: {
            "unit_cost": estimate_initial_self_cost_excl_vat(object_key),
            "suggested_price": suggested_sale_price(
                estimate_initial_self_cost_excl_vat(object_key)
            ),
        }
        for object_key in OBJECT_DETAIL_CONFIG
    }


def ensure_objects_state():
    if "objects" not in st.session_state:
        st.session_state.objects = default_objects()


def ensure_detection_state():
    ensure_objects_state()

    if "detected_object_names" not in st.session_state:
        st.session_state.detected_object_names = {
            key: obj["name"] for key, obj in st.session_state.objects.items()
        }


# -----------------------------------------------------------------------------
# Shared UI and dataframe helpers
# -----------------------------------------------------------------------------

def nav_buttons(back_screen: str | None, next_screen: str | None, next_label: str = "Continue"):
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    if back_screen:
        if col1.button("Back", key=f"nav_back_{back_screen}_{next_screen}", width="stretch"):
            st.session_state.screen = back_screen
            st.rerun()
    else:
        col1.empty()

    if next_screen:
        if col2.button(next_label, key=f"nav_next_{back_screen}_{next_screen}", width="stretch"):
            st.session_state.screen = next_screen
            st.rerun()
    else:
        col2.empty()




def apply_bottom_action_button_css():
    st.markdown(
        """
        <style>
        /* Larger bottom action buttons only. Target Streamlit key classes so object REVIEW buttons stay unchanged. */
        div[class*="st-key-nav_back_"] button,
        div[class*="st-key-nav_next_"] button,
        div[class*="st-key-processing_back"] button,
        div[class*="st-key-confirm_objects_continue"] button,
        div[class*="st-key-objects_back"] button,
        div[class*="st-key-generate_proposal_download"] button,
        div[class*="st-key-generate_proposal_download_done"] button,
        div[class*="st-key-generate_proposal_missing"] button,
        div[class*="st-key-generate_proposal_locked"] button,
        div[class*="st-key-back_to_objects_"] button,
        div[class*="st-key-approve_"] button,
        div[class*="st-key-proposal_start_over"] button {
            min-height: 52px !important;
            height: 52px !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        div[class*="st-key-nav_back_"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-nav_next_"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-processing_back"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-confirm_objects_continue"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-objects_back"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-generate_proposal_download"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-generate_proposal_download_done"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-generate_proposal_missing"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-generate_proposal_locked"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-back_to_objects_"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-approve_"] button div[data-testid="stMarkdownContainer"],
        div[class*="st-key-proposal_start_over"] button div[data-testid="stMarkdownContainer"] {
            height: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        div[class*="st-key-nav_back_"] button p,
        div[class*="st-key-nav_next_"] button p,
        div[class*="st-key-processing_back"] button p,
        div[class*="st-key-confirm_objects_continue"] button p,
        div[class*="st-key-objects_back"] button p,
        div[class*="st-key-generate_proposal_download"] button p,
        div[class*="st-key-generate_proposal_download_done"] button p,
        div[class*="st-key-generate_proposal_missing"] button p,
        div[class*="st-key-generate_proposal_locked"] button p,
        div[class*="st-key-back_to_objects_"] button p,
        div[class*="st-key-approve_"] button p,
        div[class*="st-key-proposal_start_over"] button p {
            line-height: 1.2 !important;
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_screen_header(title: str, subtitle: str | None = None):
    st.markdown('<div class="screen-wrap">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <h1 class="app-h1">
            {title}
        </h1>
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

def go_to_screen(screen_name: str):
    st.session_state.screen = screen_name
    st.session_state.scroll_to_top = True
    st.rerun()

def mark_proposal_generated():
    st.session_state.proposal_generated = True


def request_scroll_to_top():
    st.session_state.scroll_to_top = True


def run_scroll_to_top_if_requested():
    if not st.session_state.get("scroll_to_top"):
        return

    st.session_state.scroll_to_top = False

    components.html(
        """
        <script>
        function scrollToTopNow() {
            const doc = window.parent.document;

            const targets = [
                doc.scrollingElement,
                doc.documentElement,
                doc.body,
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('section.main'),
                doc.querySelector('.stMain'),
                doc.querySelector('.main'),
                doc.querySelector('.block-container')?.parentElement
            ];

            targets.forEach((el) => {
                if (!el) return;

                if (typeof el.scrollTo === 'function') {
                    el.scrollTo({ top: 0, left: 0, behavior: 'auto' });
                }

                el.scrollTop = 0;
                el.scrollLeft = 0;
            });

            window.parent.scrollTo(0, 0);
        }

        [0, 50, 150, 300, 600].forEach((delay) => {
            window.setTimeout(scrollToTopNow, delay);
        });
        </script>
        """,
        height=0,
    )

def safe_float(value, fallback=0):
    if value is None:
        return fallback

    if isinstance(value, (int, float)):
        return float(value)

    cleaned = (
        str(value)
        .replace("₪", "")
        .replace(",", "")
        .replace("\u00A0", "")
        .replace("\u202F", "")
        .replace(" ", "")
        .strip()
    )

    try:
        return float(cleaned)
    except ValueError:
        return fallback


def df_changed(old_df: pd.DataFrame, new_df: pd.DataFrame) -> bool:
    old = old_df.reset_index(drop=True).copy()
    new = new_df.reset_index(drop=True).copy()

    if list(old.columns) != list(new.columns):
        return True

    if len(old) != len(new):
        return True

    numeric_cols = {
        "Unit Cost",
        "Qty",
        "Hours",
        "Rate",
        "Monthly Cost",
        "Cost",
    }

    for col in old.columns:
        if col in numeric_cols:
            old_values = [round(safe_float(v), 4) for v in old[col].tolist()]
            new_values = [round(safe_float(v), 4) for v in new[col].tolist()]
        else:
            old_values = [str(v).strip() for v in old[col].tolist()]
            new_values = [str(v).strip() for v in new[col].tolist()]

        if old_values != new_values:
            return True

    return False


def update_editor_state_and_rerun(state_key: str, edited_df: pd.DataFrame, drop_columns: list[str] | None = None):
    if drop_columns is None:
        drop_columns = []

    clean_df = edited_df.drop(columns=drop_columns, errors="ignore").reset_index(drop=True)
    old_df = st.session_state[state_key].reset_index(drop=True)

    if df_changed(old_df, clean_df):
        st.session_state[state_key] = clean_df
        st.rerun()

def section_header(title, left_label, left_value, mid_label, mid_value, right_label, right_value):
    st.markdown(
        f"""
        <div class="object-section-header object-section-header-3">
            <div class="object-section-title">{title}</div>
            <div class="object-section-metrics">
                <div class="object-section-metric object-section-metric-col-3">
                    <div class="object-section-metric-label">{left_label}</div>
                    <div class="object-section-metric-value">{format_money(left_value)}</div>
                </div>
                <div class="object-section-metric object-section-metric-col-4">
                    <div class="object-section-metric-label">{mid_label}</div>
                    <div class="object-section-metric-value">{format_money(mid_value)}</div>
                </div>
                <div class="object-section-metric object-section-metric-total object-section-metric-col-5">
                    <div class="object-section-metric-label">{right_label}</div>
                    <div class="object-section-metric-value">{format_money(right_value)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def format_hours(value) -> str:
    hours = safe_float(value)

    if float(hours).is_integer():
        return f"{int(hours)} h"

    return f"{hours:.1f} h"

def labor_section_header(title, hours_value, labor_cost, employer_load, total):
    st.markdown(
        f"""
        <div class="object-section-header object-section-header-labor">
            <div class="object-section-title">{title}</div>
            <div class="object-section-metrics">
                <div class="object-section-metric object-section-metric-col-2">
                    <div class="object-section-metric-label">Total hours</div>
                    <div class="object-section-metric-value">{format_hours(hours_value)}</div>
                </div>
                <div class="object-section-metric object-section-metric-col-3">
                    <div class="object-section-metric-label">Cost</div>
                    <div class="object-section-metric-value">{format_money(labor_cost)}</div>
                </div>
                <div class="object-section-metric object-section-metric-col-4">
                    <div class="object-section-metric-label">Employer 25%</div>
                    <div class="object-section-metric-value">{format_money(employer_load)}</div>
                </div>
                <div class="object-section-metric object-section-metric-total object-section-metric-col-5">
                    <div class="object-section-metric-label">Total</div>
                    <div class="object-section-metric-value">{format_money(total)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Kitchen editor state and cost-calculation helpers
# -----------------------------------------------------------------------------

def init_object_editor_state(object_key: str):
    config = OBJECT_DETAIL_CONFIG[object_key]
    state_prefix = config["state_prefix"]

    materials_key = f"{state_prefix}_materials_editor_df"
    labor_key = f"{state_prefix}_labor_editor_df"
    overhead_key = f"{state_prefix}_overhead_editor_df"

    materials_version_key = f"{state_prefix}_materials_editor_version"
    labor_version_key = f"{state_prefix}_labor_editor_version"
    overhead_version_key = f"{state_prefix}_overhead_editor_version"

    materials_version = f"{state_prefix}_materials_v3_normalized_material_names"
    labor_version = f"{state_prefix}_labor_v2_site_measurement"
    overhead_version = f"{state_prefix}_overhead_v2_site_measurement"

    if (
        materials_key not in st.session_state
        or st.session_state.get(materials_version_key) != materials_version
    ):
        rows = []

        for row in config["materials_rows"]():
            rows.append(
                {
                    "Category": row["category"],
                    "Item": row["item"],
                    "Unit": row["unit"],
                    "Unit Cost": row["unit_price"],
                    "Qty": row["qty"],
                }
            )

        st.session_state[materials_key] = pd.DataFrame(rows)
        st.session_state[materials_version_key] = materials_version

    if (
        labor_key not in st.session_state
        or st.session_state.get(labor_version_key) != labor_version
    ):
        rows = []

        for row in config["labor_rows"]():
            rows.append(
                {
                    "Group": row["group"],
                    "Work": row["work"],
                    "Role": row["role"],
                    "Hours": row["hours"],
                    "Rate": row["rate"],
                }
            )

        base_labor_df = pd.DataFrame(rows)
        direct_hours = base_labor_df["Hours"].apply(safe_float).sum()
        direct_cost = (
            base_labor_df["Hours"].apply(safe_float)
            * base_labor_df["Rate"].apply(safe_float)
        ).sum()

        contingency_hours = round(direct_hours * 0.10, 1)
        contingency_rate = round(direct_cost / direct_hours) if direct_hours else 0

        rows.append(
            {
                "Group": "contingency",
                "Work": "Production contingency 10%",
                "Role": "all roles",
                "Hours": contingency_hours,
                "Rate": contingency_rate,
            }
        )

        st.session_state[labor_key] = pd.DataFrame(rows)
        st.session_state[labor_version_key] = labor_version

    if (
        overhead_key not in st.session_state
        or st.session_state.get(overhead_version_key) != overhead_version
    ):
        rows = []

        for row in config["overhead_rows"]():
            rows.append(
                {
                    "Overhead Group": row.get("overhead_group", row["group"]),
                    "Group": row["group"],
                    "Monthly Cost": row["monthly_cost"],
                    "Allocation": row["allocation"],
                    "VAT": "yes" if row["vat_applicable"] else "no",
                    "Cost": row["object_cost"],
                }
            )

        st.session_state[overhead_key] = pd.DataFrame(rows)
        st.session_state[overhead_version_key] = overhead_version


def init_kitchen_editor_state():
    init_object_editor_state("kitchen")

def add_material_cost_column(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["Unit Cost"] = result["Unit Cost"].apply(safe_float)
    result["Qty"] = result["Qty"].apply(safe_float)
    result["Cost"] = (result["Unit Cost"] * result["Qty"]).round().astype(int)

    return result


def add_labor_cost_column(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["Hours"] = result["Hours"].apply(safe_float)
    result["Rate"] = result["Rate"].apply(safe_float)
    result["Cost"] = (result["Hours"] * result["Rate"]).round().astype(int)

    return result


def parse_allocation_hours(allocation: str) -> tuple[float, float] | None:
    match = re.search(r"([0-9.]+)h\s*/\s*([0-9.]+)h", str(allocation))

    if not match:
        return None

    object_hours = safe_float(match.group(1), 0)
    capacity_hours = safe_float(match.group(2), 0)

    if capacity_hours <= 0:
        return None

    return object_hours, capacity_hours


def parse_allocation_percent(allocation: str) -> float | None:
    match = re.search(r"([0-9.]+)\s*%", str(allocation))

    if not match:
        return None

    return safe_float(match.group(1), 0)


def normalize_overhead_df(df: pd.DataFrame, percentage_base_cost: float = 0) -> pd.DataFrame:
    result = df.copy()

    result["Monthly Cost"] = result["Monthly Cost"].apply(safe_float)
    result["Cost"] = result["Cost"].apply(safe_float)

    percent_mask = result["Allocation"].astype(str).str.contains("%", regex=False, na=False)

    for index, row in result.iterrows():
        percent_from_allocation = parse_allocation_percent(row.get("Allocation", ""))

        if percent_from_allocation is not None and safe_float(row.get("Monthly Cost"), 0) == 0:
            result.at[index, "Monthly Cost"] = percent_from_allocation

    base_cost = safe_float(percentage_base_cost, 0)

    for index, row in result[~percent_mask].iterrows():
        monthly_cost = safe_float(row.get("Monthly Cost"), 0)
        allocation_hours = parse_allocation_hours(row.get("Allocation", ""))

        if allocation_hours:
            object_hours, capacity_hours = allocation_hours
            cost = round(monthly_cost / capacity_hours * object_hours)
            result.at[index, "Cost"] = cost
        else:
            cost = round(safe_float(row.get("Cost"), 0))
            result.at[index, "Cost"] = cost

        base_cost += cost

    for index, row in result[percent_mask].iterrows():
        percent_value = safe_float(row.get("Monthly Cost"), 0)
        result.at[index, "Cost"] = round(base_cost * percent_value / 100)

    result["Monthly Cost"] = result["Monthly Cost"].round(2)
    result["Cost"] = result["Cost"].round().astype(int)

    return result


def vat_from_taxable_rows(df: pd.DataFrame, cost_col="Cost", vat_col="VAT") -> int:
    if df is None or cost_col not in df or vat_col not in df:
        return 0

    taxable = df[df[vat_col].astype(str).str.lower().eq("yes")]
    return round(taxable[cost_col].apply(safe_float).sum() * VAT_RATE)

# -----------------------------------------------------------------------------
# Kitchen AG Grid grouping helpers
# -----------------------------------------------------------------------------

MATERIAL_GROUP_ORDER = [
    "Sheet materials",
    "Hardware",
    "Consumables / fixings",
    "Packaging",
]

LABOR_GROUP_ORDER = [
    "Technical prep / production files",
    "CNC operations",
    "Carpentry",
    "Metalworks",
    "Assembly",
    "Packaging / dispatch",
    "Production contingency",
]

OVERHEAD_GROUP_ORDER = [
    "Back-office payroll",
    "Facility / rent / arnona",
    "Utilities / safety",
    "Machinery / equipment",
    "Software / shop supplies / waste",
    "Project reserves",
]


def require_aggrid():
    if AgGrid is None:
        st.error(
            "streamlit-aggrid is not installed. Install it with: pip install streamlit-aggrid"
        )
        st.stop()


def material_display_group(row) -> str:
    category = str(row.get("Category", "")).lower()
    item = str(row.get("Item", "")).lower()

    if "hardware" in category:
        return "Hardware"

    if "packaging" in category:
        return "Packaging"

    if (
        "consumable" in category
        or "edge banding" in item
        or "fixing" in item
        or "fixings" in item
        or "glue" in item
        or "sealant" in item
    ):
        return "Consumables / fixings"

    return "Sheet materials"


def labor_display_group(row) -> str:
    group = str(row.get("Group", "")).lower()
    work = str(row.get("Work", "")).lower()
    role = str(row.get("Role", "")).lower()

    if "contingency" in group or "contingency" in work:
        return "Production contingency"

    if "cnc" in work or "cnc" in role:
        return "CNC operations"

    if (
        "drawing" in work
        or "laser file" in work
        or "production file" in work
        or "measurement" in work
        or "site survey" in work
        or "field survey" in work
    ):
        return "Technical prep / production files"

    if (
        "laser cutting" in work
        or "bending" in work
        or "countertop" in work
        or "backsplash" in work
        or "toe kick" in work
        or "metal qa" in work
        or "metal cleaning" in work
    ):
        return "Metalworks"

    if (
        "carcass" in work
        or "drawer box" in work
        or "assembly" in work
        or "fitting" in work
        or "test fit" in work
        or "disassembly" in work
    ):
        return "Assembly"

    if (
        "packing" in group
        or "packing" in work
        or "labeling" in work
        or "loading" in work
        or "dispatch" in work
    ):
        return "Packaging / dispatch"

    return "Carpentry"


def overhead_display_group(row) -> str:
    overhead_group = str(row.get("Overhead Group", "")).strip()
    group = str(row.get("Group", "")).strip()

    if overhead_group in OVERHEAD_GROUP_ORDER:
        return overhead_group

    text = f"{overhead_group} {group}".lower()

    if (
        "back-office" in text
        or "back office" in text
        or "payroll" in text
        or "accountant" in text
        or "constructor" in text
        or "project manager" in text
    ):
        return "Back-office payroll"

    if (
        "facility" in text
        or "rent" in text
        or "arnona" in text
        or "maintenance fee" in text
    ):
        return "Rent / arnona / facility"

    if (
        "utilities" in text
        or "safety" in text
        or "electricity" in text
        or "water" in text
        or "compressed air" in text
        or "gas" in text
        or "insurance" in text
        or "fire" in text
    ):
        return "Utilities / safety"

    if (
        "machinery" in text
        or "equipment" in text
        or "machine" in text
        or "depreciation" in text
        or "wear" in text
    ):
        return "Machinery / equipment"

    if (
        "software" in text
        or "subscriptions" in text
        or "shop supplies" in text
        or "cleaning" in text
        or "waste" in text
    ):
        return "Software / shop supplies / waste"

    return "Project reserves"

def order_grouped_rows(df: pd.DataFrame, group_col: str, group_order: list[str]) -> pd.DataFrame:
    result = df.copy()
    order_map = {group_name: index for index, group_name in enumerate(group_order)}
    result["_group_order"] = result[group_col].map(order_map).fillna(len(group_order)).astype(int)
    result["_row_order"] = range(len(result))
    result = result.sort_values(["_group_order", "_row_order"]).reset_index(drop=True)
    return result.drop(columns=["_group_order", "_row_order"], errors="ignore")


def update_aggrid_state_and_rerun(
    state_key: str,
    response: dict,
    drop_columns: list[str] | None = None,
    ):
    if drop_columns is None:
        drop_columns = []

    if not response or "data" not in response:
        return

    edited_df = pd.DataFrame(response["data"])

    if edited_df.empty:
        return

    clean_df = edited_df.drop(columns=drop_columns, errors="ignore").reset_index(drop=True)
    old_df = st.session_state[state_key].reset_index(drop=True)

    if df_changed(old_df, clean_df):
        st.session_state[state_key] = clean_df
        st.rerun()

def render_aggrid_editor(
    df: pd.DataFrame,
    key: str,
    group_col: str,
    auto_group_leaf_field: str,
    editable_columns: list[str],
    numeric_sum_columns: list[str],
    hidden_columns: list[str] | None = None,
    visible_group_count: int | None = None,
    cost_formula: str | None = None,
    percentage_base_cost: float = 0,
):
    require_aggrid()

    if hidden_columns is None:
        hidden_columns = []

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        editable=False,
        filter=False,
        sortable=False,
        resizable=True,
        suppressMenu=True,
        suppressHeaderMenuButton=True,
        suppressHeaderFilterButton=True,
        floatingFilter=False,
        cellClass="ag-text-cell",
        headerClass="ag-left-header",
    )

    gb.configure_column(
        group_col,
        rowGroup=True,
        hide=True,
        filter=False,
        sortable=False,
        suppressMenu=True,
        suppressHeaderMenuButton=True,
        suppressHeaderFilterButton=True,
    )

    for col in hidden_columns:
        if col in df.columns:
            gb.configure_column(
                col,
                hide=True,
                filter=False,
                sortable=False,
                suppressMenu=True,
                suppressHeaderMenuButton=True,
                suppressHeaderFilterButton=True,
            )

    if auto_group_leaf_field in df.columns:
        gb.configure_column(
            auto_group_leaf_field,
            hide=True,
            filter=False,
            sortable=False,
            suppressMenu=True,
            suppressHeaderMenuButton=True,
            suppressHeaderFilterButton=True,
        )

    for col in editable_columns:
        if col in df.columns:
            gb.configure_column(
                col,
                editable=True,
                filter=False,
                sortable=False,
                suppressMenu=True,
                suppressHeaderMenuButton=True,
                suppressHeaderFilterButton=True,
            )

    number_parser = JsCode(
        """
        function(params) {
            const value = params.newValue;
            if (value === null || value === undefined || value === '') return 0;
            return Number(String(value).replace(/[₪,\u00A0\u202F\\s]/g, '').trim()) || 0;
        }
        """
    )

    hide_group_total_when_open = JsCode(
        """
        function(params) {
            if (params.node && params.node.group && params.node.expanded) {
                return "";
            }

            if (params.value === null || params.value === undefined || params.value === "") {
                return "";
            }

            if (
                params.valueFormatted !== null &&
                params.valueFormatted !== undefined &&
                params.valueFormatted !== ""
            ) {
                return params.valueFormatted;
            }

            return params.value;
        }
        """
    )

    for col in numeric_sum_columns:
        if col in df.columns:
            gb.configure_column(
                col,
                aggFunc="sum",
                valueParser=number_parser,
                cellRenderer=hide_group_total_when_open,
                cellClass="ag-number-cell",
                headerClass="ag-center-header",
                filter=False,
                sortable=False,
                suppressMenu=True,
                suppressHeaderMenuButton=True,
                suppressHeaderFilterButton=True,
            )

    if "Allocation" in df.columns:
        gb.configure_column(
            "Allocation",
            editable=False,
            cellClass="ag-number-cell",
            headerClass="ag-center-header",
            filter=False,
            sortable=False,
            suppressMenu=True,
            suppressHeaderMenuButton=True,
            suppressHeaderFilterButton=True,
        )

    if cost_formula == "materials":
        gb.configure_column(
            "Cost",
            aggFunc="sum",
            editable=False,
            valueGetter=JsCode(
                """
                function(params) {
                    if (params.node.group) {
                        return params.node.aggData && params.node.aggData.Cost;
                    }

                    const unitCost = Number(params.data["Unit Cost"]) || 0;
                    const qty = Number(params.data["Qty"]) || 0;

                    return Math.round(unitCost * qty);
                }
                """
            ),
            cellRenderer=hide_group_total_when_open,
            cellClass="ag-number-cell",
            headerClass="ag-center-header",
            filter=False,
            sortable=False,
            suppressMenu=True,
            suppressHeaderMenuButton=True,
            suppressHeaderFilterButton=True,
        )

    if cost_formula == "labor":
        gb.configure_column(
            "Cost",
            aggFunc="sum",
            editable=False,
            valueGetter=JsCode(
                """
                function(params) {
                    if (params.node.group) {
                        return params.node.aggData && params.node.aggData.Cost;
                    }

                    const hours = Number(params.data["Hours"]) || 0;
                    const rate = Number(params.data["Rate"]) || 0;

                    return Math.round(hours * rate);
                }
                """
            ),
            cellRenderer=hide_group_total_when_open,
            cellClass="ag-number-cell",
            headerClass="ag-center-header",
            filter=False,
            sortable=False,
            suppressMenu=True,
            suppressHeaderMenuButton=True,
            suppressHeaderFilterButton=True,
        )

    if cost_formula == "overhead":
        gb.configure_column(
            "Cost",
            aggFunc="sum",
            editable=False,
            valueGetter=JsCode(
                f"""
                function(params) {{
                    if (params.node.group) {{
                        return params.node.aggData && params.node.aggData.Cost;
                    }}

                    const parseNumber = (value) => {{
                        if (value === null || value === undefined || value === '') return 0;
                        return Number(String(value).replace(/[₪,\u00A0\u202F\\s]/g, '').trim()) || 0;
                    }};

                    const rowCost = (data) => {{
                        const monthlyCost = parseNumber(data["Monthly Cost"]);
                        const allocation = String(data["Allocation"] || "");
                        const hoursMatch = allocation.match(/([0-9.]+)h\\s*\\/\\s*([0-9.]+)h/);

                        if (monthlyCost && hoursMatch) {{
                            const objectHours = Number(hoursMatch[1]) || 0;
                            const capacityHours = Number(hoursMatch[2]) || 1;
                            return Math.round(monthlyCost / capacityHours * objectHours);
                        }}

                        return parseNumber(data["Cost"]);
                    }};

                    const allocation = String(params.data["Allocation"] || "");

                    if (allocation.includes("%")) {{
                        const percent = parseNumber(params.data["Monthly Cost"]);
                        let baseCost = {safe_float(percentage_base_cost, 0)};

                        params.api.forEachNode((node) => {{
                            if (!node.data) return;

                            const nodeAllocation = String(node.data["Allocation"] || "");
                            if (nodeAllocation.includes("%")) return;

                            baseCost += rowCost(node.data);
                        }});

                        return Math.round(baseCost * percent / 100);
                    }}

                    return rowCost(params.data);
                }}
                """
            ),
            cellRenderer=hide_group_total_when_open,
            cellClass="ag-number-cell",
            headerClass="ag-center-header",
            filter=False,
            sortable=False,
            suppressMenu=True,
            suppressHeaderMenuButton=True,
            suppressHeaderFilterButton=True,
        )

    refresh_js = JsCode(
        """
        function(params) {
            params.api.refreshCells({force: true});
            params.api.resetRowHeights();
        }
        """
    )

    gb.configure_grid_options(
        autoGroupColumnDef={
            "headerName": "",
            "field": auto_group_leaf_field,
            "minWidth": 320,
            "suppressMenu": True,
            "suppressHeaderMenuButton": True,
            "suppressHeaderFilterButton": True,
            "filter": False,
            "sortable": False,
            "cellRendererParams": {
                "suppressCount": True,
                "suppressPadding": True,
            },
            "cellClass": "ag-text-cell",
            "headerClass": "ag-left-header",
        },
        groupDefaultExpanded=0,
        groupSuppressBlankHeader=True,
        suppressAggFuncInHeader=True,
        suppressMenuHide=True,
        stopEditingWhenCellsLoseFocus=True,
        singleClickEdit=True,
        headerHeight=36,
        rowHeight=38,
        domLayout="autoHeight",
        onCellValueChanged=refresh_js,
        onRowGroupOpened=refresh_js,
    )

    grid_options = gb.build()

    money_formatter = JsCode(
        """
               function(params) {
            const raw = params.value;
            const field = params.colDef && params.colDef.field;
            const data = params.data || {};
            const overheadGroup = String(data["Overhead Group"] || data["_display_group"] || "");
            const allocation = String(data["Allocation"] || "");
            const groupKey = params.node && params.node.group ? String(params.node.key || "") : "";

            if (field === "Monthly Cost" && params.node && params.node.group && groupKey === "Project reserves") {
                return "—";
            }

            if (raw === null || raw === undefined || raw === "") {
                return "";
            }

            const value = Number(String(raw).replace(/[₪,\u00A0\u202F\\s]/g, "").trim());

            if (!isFinite(value)) {
                return raw;
            }

            const rounded = Math.round((value + Number.EPSILON) * 10) / 10;
            const isInteger = Math.abs(rounded % 1) < 0.0001;
            const text = isInteger
                ? String(Math.round(rounded))
                : rounded.toFixed(1).replace(/\\.0$/, "");

            if (field === "Monthly Cost" && allocation.includes("%")) {
                return text;
            }

            const parts = text.split(".");
            const intPart = parts[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, "\u202F");

            return "₪" + intPart + (parts.length > 1 ? "." + parts[1] : "");
        }
        """
    )

    number_formatter = JsCode(
        """
        function(params) {
            const raw = params.value;

            if (raw === null || raw === undefined || raw === "") {
                return "";
            }

            const value = Number(String(raw).replace(/[\u00A0\u202F\\s]/g, "").trim());

            if (!isFinite(value)) {
                return raw;
            }

            const rounded = Math.round((value + Number.EPSILON) * 100) / 100;
            const isInteger = Math.abs(rounded % 1) < 0.0001;
            const text = isInteger
                ? String(Math.round(rounded))
                : rounded.toFixed(2).replace(/0+$/, "").replace(/\\.$/, "");

            const parts = text.split(".");
            const intPart = parts[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, "\\u202F");

            return intPart + (parts.length > 1 ? "." + parts[1] : "");
        }
        """
    )

    money_columns = {"Unit Cost", "Rate", "Monthly Cost", "Cost"}
    plain_number_columns = {"Qty", "Hours"}

    def apply_number_formatters(column_defs):
        for col_def in column_defs:
            field = col_def.get("field")

            if field in money_columns:
                col_def["valueFormatter"] = money_formatter
                col_def["valueParser"] = number_parser
                col_def["cellClass"] = "ag-number-cell"
                col_def["headerClass"] = "ag-center-header"

            if field in plain_number_columns:
                col_def["valueFormatter"] = number_formatter
                col_def["valueParser"] = number_parser
                col_def["cellClass"] = "ag-number-cell"
                col_def["headerClass"] = "ag-center-header"

            if "children" in col_def:
                apply_number_formatters(col_def["children"])

    apply_number_formatters(grid_options.get("columnDefs", []))

    initial_visible_rows = visible_group_count or len(df)
    initial_grid_height = 36 + 38 * initial_visible_rows + 6

    custom_css = {
        ".ag-theme-balham": {
            "font-family": "var(--sans) !important",
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
        },
        ".ag-root-wrapper": {
            "border-radius": "var(--r-md) !important",
            "border": "1px solid rgba(23, 25, 28, 0.42) !important",
            "box-shadow": "none !important",
            "background": "var(--surface) !important",
        },
        ".ag-root-wrapper-body": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height .ag-center-cols-viewport": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height .ag-center-cols-container": {
            "min-height": "0 !important",
        },
        ".ag-header-cell-menu-button": {
            "display": "none !important",
        },
        ".ag-header-icon": {
            "display": "none !important",
        },
        ".ag-header-cell-label": {
            "justify-content": "flex-start !important",
        },
        ".ag-header-cell.ag-center-header .ag-header-cell-label": {
            "justify-content": "center !important",
        },
        ".ag-header": {
            "background": "var(--bg) !important",
            "border-color": "rgba(23, 25, 28, 0.28) !important",
        },
        ".ag-header-cell": {
            "background": "var(--bg) !important",
            "color": "var(--ink-500) !important",
            "border": "0 !important",
            "border-right": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-header-cell-text": {
            "font-family": "var(--mono) !important",
            "font-size": "11px !important",
            "font-weight": "500 !important",
            "text-transform": "uppercase !important",
            "letter-spacing": "0.06em !important",
            "color": "var(--ink-500) !important",
        },
        ".ag-row": {
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
            "border": "0 !important",
            "border-bottom": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-cell": {
            "display": "flex !important",
            "align-items": "center !important",
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
            "border": "0 !important",
            "border-right": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-text-cell": {
            "justify-content": "flex-start !important",
            "text-align": "left !important",
        },
        ".ag-number-cell": {
            "justify-content": "center !important",
            "text-align": "center !important",
        },
        ".ag-right-aligned-cell": {
            "justify-content": "center !important",
            "text-align": "center !important",
        },
        ".ag-header-cell.ag-right-aligned-header .ag-header-cell-label": {
            "justify-content": "center !important",
        },
    }

    return AgGrid(
        df,
        gridOptions=grid_options,
        key=key,
        theme="balham",
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=True,
        reload_data=False,
        custom_css=custom_css,
        height=initial_grid_height,
    )

    def apply_number_formatters(column_defs):
        for col_def in column_defs:
            field = col_def.get("field")

            if field in money_columns:
                col_def["valueFormatter"] = money_formatter
                col_def["valueParser"] = number_parser
                col_def["cellClass"] = "ag-number-cell"
                col_def["headerClass"] = "ag-center-header"

            if field in plain_number_columns:
                col_def["valueFormatter"] = number_formatter
                col_def["valueParser"] = number_parser
                col_def["cellClass"] = "ag-number-cell"
                col_def["headerClass"] = "ag-center-header"

            if "children" in col_def:
                apply_number_formatters(col_def["children"])

    apply_number_formatters(grid_options.get("columnDefs", []))

    initial_visible_rows = visible_group_count or len(df)
    initial_grid_height = 36 + 38 * initial_visible_rows + 2

    custom_css = {
        ".ag-theme-balham": {
            "font-family": "var(--sans) !important",
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
        },
        ".ag-root-wrapper": {
            "border-radius": "var(--r-md) !important",
            "border": "1px solid rgba(23, 25, 28, 0.42) !important",
            "box-shadow": "none !important",
            "background": "var(--surface) !important",
        },
        ".ag-root-wrapper-body": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height .ag-center-cols-viewport": {
            "min-height": "0 !important",
        },
        ".ag-layout-auto-height .ag-center-cols-container": {
            "min-height": "0 !important",
        },
        ".ag-header-cell-menu-button": {
            "display": "none !important",
        },
        ".ag-header-icon": {
            "display": "none !important",
        },
        ".ag-header-cell-label": {
            "justify-content": "flex-start !important",
        },
        ".ag-header-cell.ag-center-header .ag-header-cell-label": {
            "justify-content": "center !important",
        },
        ".ag-header": {
            "background": "var(--bg) !important",
            "border-color": "rgba(23, 25, 28, 0.28) !important",
        },
        ".ag-header-cell": {
            "background": "var(--bg) !important",
            "color": "var(--ink-500) !important",
            "border": "0 !important",
            "border-right": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-header-cell-text": {
            "font-family": "var(--mono) !important",
            "font-size": "11px !important",
            "font-weight": "500 !important",
            "text-transform": "uppercase !important",
            "letter-spacing": "0.06em !important",
            "color": "var(--ink-500) !important",
        },
        ".ag-row": {
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
            "border": "0 !important",
            "border-bottom": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-cell": {
            "display": "flex !important",
            "align-items": "center !important",
            "background": "var(--surface) !important",
            "color": "var(--ink-900) !important",
            "border": "0 !important",
            "border-right": "1px solid rgba(23, 25, 28, 0.32) !important",
        },
        ".ag-text-cell": {
            "justify-content": "flex-start !important",
            "text-align": "left !important",
        },
        ".ag-number-cell": {
            "justify-content": "center !important",
            "text-align": "center !important",
        },
        ".ag-right-aligned-cell": {
            "justify-content": "center !important",
            "text-align": "center !important",
        },
        ".ag-header-cell.ag-right-aligned-header .ag-header-cell-label": {
            "justify-content": "center !important",
        },
    }

    return AgGrid(
        df,
        gridOptions=grid_options,
        key=key,
        theme="balham",
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=True,
        reload_data=False,
        custom_css=custom_css,
        height=initial_grid_height,
    )

#-----------------------------------------------------------------------------
# Streamlit screens
# -----------------------------------------------------------------------------

# First screen: upload RFQ / drawing package.
def render_upload_screen():
    st.markdown(
        """
        <style>

        .stApp:has(.upload-screen-active) .block-container {
            height: 100vh !important;
            max-height: 100vh !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

       .stApp:has(.upload-screen-active) .block-container > div {
            height: 100vh !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            transform: translateY(-40px) !important;
        }

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

        <div class="upload-screen-active" style="display:none"></div>


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
        "📎 DROP OR UPLOAD",
        type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "dwg", "dxf"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.uploaded_file_size = uploaded_file.size
        st.session_state.uploaded_file_type = detect_file_type(uploaded_file.name)
        st.session_state.screen = "processing"
        st.rerun()


# Processing animation before the objects workspace.
def render_estimate_processing_screen():
    st.markdown(
        """
        <style>
        .stApp:has(.estimate-processing-active) div[data-testid="stButton"] {
            display: none !important;
        }

        .stApp:has(.estimate-processing-active) .block-container {
            padding-bottom: 48px !important;
        }
        </style>
        <div class="estimate-processing-active" style="display:none"></div>
        """,
        unsafe_allow_html=True,
    )
    render_screen_header("Preparing object estimates")

    progress = st.progress(0)
    status_placeholder = st.empty()

    steps = [
        "1/8 Decomposing detected objects...",
        "2/8 Mapping materials and consumables...",
        "3/8 Estimating carpentry and metal work...",
        "4/8 Estimating labor processes...",
        "5/8 Allocating equipment and machine costs...",
        "6/8 Allocating workshop overhead...",
        "7/8 Preparing object-level sale price inputs...",
        "8/8 Estimate workspace ready.",
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

def apply_screen_bottom_compact_class(class_name: str):
    st.markdown(
        f"""
        <style>
        .stApp:has(.{class_name}) .block-container {{
            padding-bottom: 48px !important;
        }}
        </style>
        <div class="{class_name}" style="display:none"></div>
        """,
        unsafe_allow_html=True,
    )

# File review screen: preview + detected objects + metadata.
def render_processing_screen():
    ensure_detection_state()
    apply_screen_bottom_compact_class("processing-screen-compact")

    if "metadata_extracted" not in st.session_state:
        st.session_state.metadata_extracted = False

    if not st.session_state.metadata_extracted:
        render_screen_header("Reading your RFQ package")

        progress = st.progress(0)
        status_placeholder = st.empty()

        steps = [
            "1/6 Detecting file type...",
            "2/6 Reading title block...",
            "3/6 Extracting project metadata...",
            "4/6 Detecting drawing pages...",
            "5/6 Identifying project objects...",
            "6/6 Project metadata extracted.",
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
        """
        <div class="screen-wrap">
            <div class="screen-block processing-title-block">
                <h1 style="
                    font-family: var(--mono) !important;
                    color: var(--accent-500) !important;
                    font-size: 40px !important;
                    line-height: 1.1 !important;
                    font-weight: 500 !important;
                    letter-spacing: -0.02em !important;
                    margin: 0 0 var(--s5) 0 !important;
                ">
                    File review
                </h1>
            </div>
        </div>
        """,
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

        rfq_source_path = Path("assets/RA-N01_20260216.pdf")

        st.markdown(
            """
            <style>
            div[class*="st-key-rfq_source_file_download"] button {
                display: block !important;
                width: auto !important;
                min-height: 0 !important;
                height: auto !important;
                margin: 0 !important;
                padding: 0 !important;
                border: 0 !important;
                border-radius: 0 !important;
                background: transparent !important;
                box-shadow: none !important;
                color: inherit !important;
                text-align: left !important;
                justify-content: flex-start !important;
            }

            div[class*="st-key-rfq_source_file_download"] button:hover,
            div[class*="st-key-rfq_source_file_download"] button:active,
            div[class*="st-key-rfq_source_file_download"] button:focus {
                border: 0 !important;
                background: transparent !important;
                box-shadow: none !important;
                color: inherit !important;
            }

            div[class*="st-key-rfq_source_file_download"] button div[data-testid="stMarkdownContainer"],
            div[class*="st-key-rfq_source_file_download"] button p {
                margin: 0 !important;
                padding: 0 !important;
                font: inherit !important;
                color: inherit !important;
                text-align: left !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if rfq_source_path.exists():
            st.download_button(
                "RA-N01_20260216.pdf",
                data=rfq_source_path.read_bytes(),
                file_name="RA-N01_20260216.pdf",
                mime="application/pdf",
                key="rfq_source_file_download",
                width="content",
            )
        else:
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
        if st.button("Back", key="processing_back", width="stretch"):
            st.session_state.metadata_extracted = False
            st.session_state.screen = "upload"
            st.rerun()

    with b1:
        if st.button(
            "Confirm object detection → Estimate",
            key="confirm_objects_continue",
            width="stretch",
        ):
            for object_key, name in st.session_state.detected_object_names.items():
                if object_key in st.session_state.objects:
                    st.session_state.objects[object_key]["name"] = name

            st.session_state.screen = "estimate_processing"
            st.rerun()

def open_object_detail_from_objects_screen(object_key: str):
    ensure_objects_state()
    request_scroll_to_top()

    st.session_state.current_object = object_key

    if "object_processing_completed" not in st.session_state:
        st.session_state.object_processing_completed = []

    if object_key in st.session_state.object_processing_completed:
        st.session_state.screen = "object_detail"
    else:
        st.session_state.screen = "object_processing"

# Objects summary screen: object rows, project-level costs, and proposal CTA.
def render_objects_screen():
    ensure_objects_state()

    st.markdown(
        """
        <style>

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] {
            display: flex !important;
            justify-content: center !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] > div {
            width: 188px !important;
        }

        /* Price input: keep only the actual BaseWeb input white, not every wrapper */
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input {
            background: var(--surface) !important;
            background-color: var(--surface) !important;
        }

        /* Actual visible input frame */
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"] {
            height: 40px !important;
            min-height: 40px !important;
            border: 1.5px solid var(--line-300) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            outline: none !important;
            opacity: 1 !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"]:hover {
            border-color: var(--ink-400) !important;
            box-shadow: none !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: var(--orange) !important;
            box-shadow: 0 0 0 2px rgba(242, 115, 69, 0.14) !important;
            outline: none !important;
        }

        /* Text field itself */
            .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input {
            box-sizing: border-box !important;
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            padding: 0 14px 0 14px !important;

            border: 0 !important;
            box-shadow: none !important;
            outline: none !important;

            color: var(--ink-900) !important;
            font-size: 18px !important;
            font-weight: 800 !important;
            line-height: normal !important;
            text-align: center !important;

            opacity: 1 !important;
            -webkit-text-fill-color: var(--ink-900) !important;
            transform: translateY(0px) !important;
     }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input:focus {
            border: 0 !important;
            box-shadow: none !important;
            outline: none !important;
        }

        /* Prevent grey flash during Streamlit rerun / disabled state */
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled),
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled) *,
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled) div,
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled) span,
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled) input {
            background: var(--surface) !important;
            background-color: var(--surface) !important;
            opacity: 1 !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"]:has(input:disabled) div[data-baseweb="input"],
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"][aria-disabled="true"],
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] div[data-baseweb="input"][data-disabled="true"] {
            height: 40px !important;
            min-height: 40px !important;
            border: 1.5px solid var(--line-300) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            outline: none !important;
            background: var(--surface) !important;
            background-color: var(--surface) !important;
            opacity: 1 !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input:disabled {
            box-sizing: border-box !important;
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            padding: 0 14px 0 14px !important;
            line-height: normal !important;
            color: var(--ink-900) !important;
            -webkit-text-fill-color: var(--ink-900) !important;
            background: var(--surface) !important;
            background-color: var(--surface) !important;
            opacity: 1 !important;
            transform: translateY(0px) !important;
        }

        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input:-webkit-autofill,
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input:-webkit-autofill:hover,
        .stApp:has(.objects-price-input-scope) div[data-testid="stTextInput"] input:-webkit-autofill:focus {
            -webkit-box-shadow: 0 0 0 1000px var(--surface) inset !important;
            -webkit-text-fill-color: var(--ink-900) !important;
        }
        </style>
        <div class="objects-price-input-scope" style="display:none"></div>
        """,
        unsafe_allow_html=True,
    )

    apply_screen_bottom_compact_class("objects-screen-compact")

    locked_values = locked_demo_values()
    locked_object_values = locked_values["objects"]
    locked_project_level_prices = locked_values["project_level_prices"]

    st.markdown(
        """
        <div class="screen-wrap">
            <div class="screen-block objects-title-block">
                <div class="orange-title">
                    <Set>Review objects → Set sale price → Generate proposal</div>
                </div>
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
        st.markdown("<div class='table-head center'>qty</div>", unsafe_allow_html=True)
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
        locked_object = locked_object_values.get(object_key, {})

        unit_cost = locked_object.get("unit_cost", 0)
        suggested_price = locked_object.get("suggested_price", 0)

        obj["unit_cost"] = unit_cost
        obj["suggested_price"] = suggested_price

        input_key = f"sale_price_input_{object_key}"
        input_source_key = f"{input_key}_unit_cost_source"

        if input_key not in st.session_state or st.session_state.get(input_source_key) != unit_cost:
            st.session_state[input_key] = format_money(suggested_price)
            st.session_state[input_source_key] = unit_cost

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

            review_label = "DONE" if obj.get("approved") else "REVIEW"
            review_type = "primary" if obj.get("approved") else "secondary"

            st.button(
                review_label,
                key=f"review_{object_key}",
                width="stretch",
                type=review_type,
                on_click=open_object_detail_from_objects_screen,
                args=(object_key,),
            )

        st.markdown("<div class='soft-line row-line'></div>", unsafe_allow_html=True)

    project_level_costs = project_level_self_costs()

    delivery_self_cost = project_level_costs["delivery"]
    installation_self_cost = project_level_costs["installation"]

    delivery_suggested = locked_project_level_prices["delivery"]
    installation_suggested = locked_project_level_prices["installation"]

    if (
        "delivery_price_input" not in st.session_state
        or st.session_state.get("delivery_price_input_locked_default") != delivery_suggested
    ):
        st.session_state.delivery_price_input = format_money(delivery_suggested)
        st.session_state.delivery_price_input_locked_default = delivery_suggested

    if (
        "installation_price_input" not in st.session_state
        or st.session_state.get("installation_price_input_locked_default") != installation_suggested
    ):
        st.session_state.installation_price_input = format_money(installation_suggested)
        st.session_state.installation_price_input_locked_default = installation_suggested

    d0, d1, d2, d3, d4, d_spacer, d5 = st.columns(object_col_weights)

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
        st.markdown(
            "<div class='table-value center'>1</div>",
            unsafe_allow_html=True,
        )

    with d2:
        st.markdown(
            f"<div class='table-value center'>{format_money(delivery_self_cost)}</div>",
            unsafe_allow_html=True,
        )

    with d3:
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

    with d4:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with d_spacer:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with d5:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("<div class='soft-line row-line'></div>", unsafe_allow_html=True)

    i0, i1, i2, i3, i4, i_spacer, i5 = st.columns(object_col_weights)

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
        st.markdown(
            "<div class='table-value center'>1</div>",
            unsafe_allow_html=True,
        )

    with i2:
        st.markdown(
            f"<div class='table-value center'>{format_money(installation_self_cost)}</div>",
            unsafe_allow_html=True,
        )

    with i3:
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

    with i4:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with i_spacer:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with i5:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    st.session_state.delivery_self_cost = delivery_self_cost
    st.session_state.installation_self_cost = installation_self_cost

    st.markdown("<div class='soft-line summary-top-line'></div>", unsafe_allow_html=True)

    project_price = objects_subtotal + delivery_price + installation_price
    vat = round(project_price * VAT_RATE)
    total = project_price + vat

    st.session_state.project_price = project_price
    st.session_state.vat = vat
    st.session_state.total_price = total
    st.session_state.delivery_price = delivery_price
    st.session_state.installation_price = installation_price

    all_objects_reviewed = all(
        obj.get("approved") for obj in st.session_state.objects.values()
    )

    if all_objects_reviewed:
        st.session_state.review_required_error = False

    summary_pdf_path = Path("assets/RA-N01_summary.pdf")

    s0, s_gap1, s1, s_gap2, s2, s_gap3, s3 = st.columns(
        [1.05, 0.55, 0.95, 0.55, 0.95, 0.55, 1.10]
    )

    with s0:
        summary_pdf_path = Path("assets/RA-N01_summary.pdf")

        if all_objects_reviewed and summary_pdf_path.exists():
            summary_pdf_b64 = base64.b64encode(summary_pdf_path.read_bytes()).decode("utf-8")
            summary_href = f"data:application/pdf;base64,{summary_pdf_b64}"
            summary_link_html = (
                f'<a class="project-summary-download-link" '
                f'href="{summary_href}" '
                f'download="RA-N01_summary.pdf">'
                f'<span class="project-summary-pdf-icon">PDF</span>'
                f'<span>Download PDF</span>'
                f'</a>'
            )

        elif all_objects_reviewed:
            summary_link_html = '<span class="project-summary-download-missing">PDF missing</span>'

        else:
            summary_link_html = (
                '<a class="project-summary-download-link locked" '
                'href="#review-required-message">'
                '<span class="project-summary-pdf-icon">PDF</span>'
                '<span>Download PDF</span>'
                '</a>'
            )

        st.markdown(
            f"""
            <div class="project-summary-cell project-side-summary">
                <div class="summary-title">Project Summary</div>
                <div class="project-summary-download-row">
                    {summary_link_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s_gap1:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with s1:
        st.markdown(
            f"""
            <div class="project-summary-cell project-side-summary center">
                <div class="summary-title">Project Price</div>
                <div class="summary-number">{format_money(project_price)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s_gap2:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with s2:
        st.markdown(
            f"""
            <div class="project-summary-cell project-side-summary center">
                <div class="summary-title">VAT 18%</div>
                <div class="summary-number">{format_money(vat)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s_gap3:
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with s3:
        st.markdown(
            f"""
            <div class="project-summary-cell project-total-cell">
                <div class="summary-title">Project Total</div>
                <div class="summary-number project-total-number">{format_money(total)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        ) 

    error_visible_class = (
        " visible"
        if st.session_state.get("review_required_error") and not all_objects_reviewed
        else ""
    )

    st.markdown(
        f"""
        <div id="review-required-message" class="review-required-error-wide{error_visible_class}">
            Review all objects first.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='soft-line summary-bottom-line'></div>", unsafe_allow_html=True)

    b0, b1 = st.columns([1, 1])

    with b0:
        if st.button("Back", key="objects_back", width="stretch"):
            st.session_state.screen = "processing"
            st.rerun()

    with b1:
        proposal_pdf_path = Path("assets/RA-N01_commercial_proposal.pdf")
        proposal_generated = st.session_state.get("proposal_generated", False)

        if all_objects_reviewed and proposal_pdf_path.exists():
            st.download_button(
                "Proposal Generated" if proposal_generated else "Generate proposal",
                data=proposal_pdf_path.read_bytes(),
                file_name="RA-N01_commercial_proposal.pdf",
                mime="application/pdf",
                key=(
                    "generate_proposal_download_done"
                    if proposal_generated
                    else "generate_proposal_download"
                ),
                width="stretch",
                type="primary" if proposal_generated else "secondary",
                on_click=mark_proposal_generated,
            )

        elif all_objects_reviewed:
            st.button(
                "Proposal PDF missing",
                key="generate_proposal_missing",
                width="stretch",
                disabled=True,
            )

        else:
            if st.button("Generate proposal", key="generate_proposal_locked", width="stretch"):
                st.session_state.review_required_error = True
                st.rerun()

def render_object_processing_screen():
    ensure_objects_state()

    object_key = st.session_state.get("current_object", "kitchen")
    obj = st.session_state.objects.get(object_key, st.session_state.objects["kitchen"])
    object_name = obj.get("name", "Object")

    st.markdown(
        """
        <style>
        .stApp:has(.object-processing-active) .block-container {
        padding-bottom: 48px !important;
        }

        .stApp:has(.object-processing-active) .block-container {
            padding-bottom: 48px !important;
        }
        </style>
        <div class="object-processing-active" style="display:none"></div>
        """,
        unsafe_allow_html=True,
    )

    render_screen_header(f"Estimating: {object_name}")

    progress = st.progress(0)
    status_placeholder = st.empty()

    steps = [
        f"1/6 Reading {object_name} geometry...",
        "2/6 Matching materials and finishes...",
        "3/6 Estimating fabrication operations...",
        "4/6 Calculating labor and machine time...",
        "5/6 Allocating overhead and reserves...",
        "6/6 Object estimate ready.",
    ]

    for i, step in enumerate(steps, start=1):
        status_placeholder.markdown(
            f"<div class='status-card'>{step}</div>",
            unsafe_allow_html=True,
        )
        progress.progress(i / len(steps))
        time.sleep(0.35)

    if "object_processing_completed" not in st.session_state:
        st.session_state.object_processing_completed = []

    if object_key not in st.session_state.object_processing_completed:
            st.session_state.object_processing_completed.append(object_key)

    st.session_state.screen = "object_detail"
    st.rerun()

# Object detail screen. In the old code, only Kitchen has a real card.
def render_object_detail_screen():
    ensure_objects_state()

    object_key = st.session_state.get("current_object", "kitchen")
    obj = st.session_state.objects.get(object_key, st.session_state.objects["kitchen"])

    if object_key not in OBJECT_DETAIL_CONFIG:
        render_screen_header(
            f"Object: {obj['name']}",
            "This object card will be added next.",
        )

        if st.button(
            "Back to objects",
            key=f"back_to_objects_{object_key}",
            width="stretch",
        ):
            st.session_state.screen = "objects"
            st.rerun()

        return

    object_config = OBJECT_DETAIL_CONFIG[object_key]
    state_prefix = object_config["state_prefix"]

    materials_state_key = f"{state_prefix}_materials_editor_df"
    labor_state_key = f"{state_prefix}_labor_editor_df"
    overhead_state_key = f"{state_prefix}_overhead_editor_df"

    init_object_editor_state(object_key)

    st.markdown(
        """
        <style>
        .object-detail-hero {
            display: grid !important;
            grid-template-columns: max-content max-content !important;
            column-gap: 52px !important;
            align-items: start !important;
            padding-top: 28px !important;
            margin-bottom: -66px !important;
        }

        .object-detail-title-block {
            margin: 0 !important;
            padding: 0 !important;
        }

        .object-detail-main-line {
            display: flex !important;
            align-items: baseline !important;
            gap: 10px !important;
            margin: 0 0 14px 0 !important;
            font-family: var(--mono) !important;
            font-size: 40px !important;
            line-height: 1.05 !important;
            letter-spacing: -0.04em !important;
            white-space: nowrap !important;
            color: var(--ink-900) !important;
            font-weight: 700 !important;
            margin-bottom: 18px !important;
        }

        .object-detail-main-value {
            color: var(--orange) !important;
            font-weight: 700 !important;
        }

        .object-detail-sub-line {
            display: flex !important;
            align-items: baseline !important;
            gap: 8px !important;
            margin: 0 !important;
            font-family: var(--mono) !important;
            font-size: 24px !important;
            line-height: 1.15 !important;
            letter-spacing: -0.025em !important;
            white-space: nowrap !important;
            color: var(--ink-700) !important;
            font-weight: 600 !important;
        }

        .object-detail-sub-value {
            color: var(--orange) !important;
            font-weight: 700 !important;
        }

        .object-detail-dot {
            color: var(--ink-400) !important;
            margin: 0 8px !important;
            font-weight: 500 !important;
        }

        .object-detail-info-row {
            display: flex !important;
            align-items: baseline !important;
            gap: 10px !important;
            margin: 0 0 8px 0 !important;
            font-size: 34px !important;
            line-height: 1.02 !important;
            letter-spacing: -0.8px !important;
            white-space: nowrap !important;
        }

        .object-detail-info-label {
            color: var(--ink-900) !important;
            font-weight: 500 !important;
        }

        .object-detail-info-value {
            color: var(--orange) !important;
            font-weight: 800 !important;
        }

        .object-detail-preview-img {
            display: block !important;
            width: 170px !important;
            height: 120px !important;
            object-fit: cover !important;
            border-radius: 10px !important;
        }

        .object-detail-hero-spacer {
            height: 0 !important;
        }

        .object-detail-preview-placeholder {
            width: 170px !important;
            height: 120px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 1px solid var(--line-200) !important;
            border-radius: 10px !important;
            color: var(--ink-500) !important;
            font-size: 14px !important;
            font-weight: 650 !important;
            background: var(--surface) !important;
        }

        .block-container {
            padding-bottom: 48px !important;
        }

        .object-section-header {
            display: grid !important;
            grid-template-columns:
                minmax(320px, 2.4fr)
                minmax(120px, 0.72fr)
                minmax(120px, 0.72fr)
                minmax(120px, 0.72fr)
                minmax(120px, 0.78fr) !important;
            align-items: end !important;
            column-gap: 0 !important;
            width: 100% !important;
        }

        .object-section-title {
            grid-column: 1 !important;
            align-self: end !important;
        }

        .object-section-metrics {
            display: contents !important;
        }

        .object-section-metric {
            min-width: 0 !important;
            text-align: center !important;
            justify-self: center !important;
        }

        .object-section-metric-col-2 {
            grid-column: 2 !important;
        }

        .object-section-metric-col-3 {
            grid-column: 3 !important;
        }

        .object-section-metric-col-4 {
            grid-column: 4 !important;
        }

        .object-section-metric-col-5 {
            grid-column: 5 !important;
        }

        .object-section-metric-total .object-section-metric-value {
            color: var(--orange) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    kitchen_preview_path = Path(object_config["preview_path"])
    kitchen_confidence = object_config["confidence"]

    if kitchen_preview_path.exists():
        preview_src = base64.b64encode(kitchen_preview_path.read_bytes()).decode("utf-8")
        preview_html = (
            f'<img class="object-detail-preview-img" '
            f'src="data:image/png;base64,{preview_src}" '
            f'alt="Kitchen preview">'
        )
    else:
        preview_html = '<div class="object-detail-preview-placeholder">Preview image</div>'

    hero_html = (
        '<div class="object-detail-hero">'
        '<div class="object-detail-title-block">'
        '<div class="object-detail-main-line">'
        '<span>OBJECT:</span>'
        f'<span class="object-detail-main-value">{obj["name"]}</span>'
        '</div>'
        '<div class="object-detail-sub-line">'
        '<span>QTY:</span>'
        f'<span class="object-detail-sub-value">{obj.get("qty", 1)}</span>'
        '<span class="object-detail-dot">·</span>'
        '<span>AI CONFIDENCE:</span>'
        f'<span class="object-detail-sub-value">{kitchen_confidence}%</span>'
        '</div>'
        '</div>'
        '<div>'
        f'{preview_html}'
        '</div>'
        '</div>'
    )

    st.markdown(hero_html, unsafe_allow_html=True)

    st.markdown("<div class='object-detail-hero-spacer'></div>", unsafe_allow_html=True)

    # Materials / hardware section

    materials_source = add_material_cost_column(st.session_state[materials_state_key])
    materials_cost = round(materials_source["Cost"].sum())
    materials_vat = round(materials_cost * VAT_RATE)
    materials_total = materials_cost + materials_vat

    section_header(
        "MATERIAL COST",
        "Cost",
        materials_cost,
        "VAT 18%",
        materials_vat,
        "Total",
        materials_total,
    )

    materials_grid = materials_source.copy()
    materials_grid["_display_group"] = materials_grid.apply(material_display_group, axis=1)
    materials_grid = order_grouped_rows(
        materials_grid,
        group_col="_display_group",
        group_order=MATERIAL_GROUP_ORDER,
    )

    materials_response = render_aggrid_editor(
        materials_grid,
        key=f"{state_prefix}_materials_aggrid",
        group_col="_display_group",
        auto_group_leaf_field="Item",
        editable_columns=["Item", "Unit", "Unit Cost", "Qty"],
        numeric_sum_columns=["Qty", "Cost"],
        hidden_columns=["Category"],
        visible_group_count=len(MATERIAL_GROUP_ORDER),
        cost_formula="materials",
    )

    update_aggrid_state_and_rerun(
        materials_state_key,
        materials_response,
        drop_columns=["Cost", "_display_group"],
    )

    # Labor cost section

    labor_source = add_labor_cost_column(st.session_state[labor_state_key])
    labor_hours = labor_source["Hours"].apply(safe_float).sum()
    labor_base = round(labor_source["Cost"].sum())
    employer_load = round(labor_base * EMPLOYER_LOAD_RATE)
    labor_total = labor_base + employer_load

    labor_section_header(
        "LABOR COST",
        labor_hours,
        labor_base,
        employer_load,
        labor_total,
    )

    labor_grid = labor_source.copy()
    labor_grid["_display_group"] = labor_grid.apply(labor_display_group, axis=1)
    labor_grid = order_grouped_rows(
        labor_grid,
        group_col="_display_group",
        group_order=LABOR_GROUP_ORDER,
    )

    labor_response = render_aggrid_editor(
        labor_grid,
        key=f"{state_prefix}_labor_aggrid",
        group_col="_display_group",
        auto_group_leaf_field="Work",
        editable_columns=["Work", "Role", "Hours", "Rate"],
        numeric_sum_columns=["Hours", "Cost"],
        hidden_columns=["Group"],
        visible_group_count=len(LABOR_GROUP_ORDER),
        cost_formula="labor",
    )

    update_aggrid_state_and_rerun(
        labor_state_key,
        labor_response,
        drop_columns=["Cost", "_display_group"],
    )

    # Overhead section

    overhead_percentage_base_cost = materials_cost + labor_total
    overhead_source = normalize_overhead_df(
        st.session_state[overhead_state_key],
        percentage_base_cost=overhead_percentage_base_cost,
    )
    overhead_cost = round(overhead_source["Cost"].sum())
    overhead_vat = vat_from_taxable_rows(overhead_source)
    overhead_total = overhead_cost + overhead_vat

    section_header(
        "OVERHEAD",
        "Cost",
        overhead_cost,
        "VAT",
        overhead_vat,
        "Total",
        overhead_total,
    )

    overhead_grid = overhead_source.copy()
    overhead_grid["_display_group"] = overhead_grid.apply(overhead_display_group, axis=1)
    overhead_grid = order_grouped_rows(
        overhead_grid,
        group_col="_display_group",
        group_order=OVERHEAD_GROUP_ORDER,
    )

    overhead_response = render_aggrid_editor(
        overhead_grid,
        key=f"{state_prefix}_overhead_aggrid",
        group_col="_display_group",
        auto_group_leaf_field="Group",
        editable_columns=["Group", "Monthly Cost", "Cost"],
        numeric_sum_columns=["Monthly Cost", "Cost"],
        hidden_columns=["VAT", "Overhead Group"],
        visible_group_count=len(OVERHEAD_GROUP_ORDER),
        cost_formula="overhead",
        percentage_base_cost=overhead_percentage_base_cost,
    )

    update_aggrid_state_and_rerun(
        overhead_state_key,
        overhead_response,
        drop_columns=["_display_group"],
    )

    # Self-cost summary

    self_cost_excl_vat = materials_cost + labor_total + overhead_cost
    self_cost_vat = materials_vat + overhead_vat
    self_cost_total = self_cost_excl_vat + self_cost_vat

    st.markdown(
        f"""
        <div class="object-final-summary">
            <div class="object-final-title">{object_config["self_cost_title"]}</div>
            <div class="object-final-metrics">
                <div>
                    <div class="object-final-label">Excl. VAT</div>
                    <div class="object-final-value">{format_money(self_cost_excl_vat)}</div>
                </div>
                <div>
                    <div class="object-final-label">VAT</div>
                    <div class="object-final-value">{format_money(self_cost_vat)}</div>
                </div>
                <div>
                    <div class="object-final-label">Total</div>
                    <div class="object-final-value object-final-total">{format_money(self_cost_total)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='object-detail-buttons-spacer'></div>", unsafe_allow_html=True)

    b0, b1 = st.columns([1, 1])

    with b0:
        if st.button(
            "Back to objects",
            key=f"back_to_objects_{object_key}",
            width="stretch",
        ):
            st.session_state.screen = "objects"
            st.rerun()

    with b1:
        if st.button(
            object_config["approve_label"],
            key=f"approve_{object_key}_estimate",
            width="stretch",
        ):
            st.session_state.objects[object_key]["approved"] = True
            st.session_state.objects[object_key]["unit_cost"] = self_cost_excl_vat
            st.session_state.objects[object_key]["suggested_price"] = round(self_cost_excl_vat * 1.30)
            st.session_state.objects[object_key]["sale_price"] = round(self_cost_excl_vat * 1.30)

            st.session_state.objects[object_key]["materials_cost"] = materials_cost
            st.session_state.objects[object_key]["materials_vat"] = materials_vat
            st.session_state.objects[object_key]["materials_total"] = materials_total

            st.session_state.objects[object_key]["labor_base"] = labor_base
            st.session_state.objects[object_key]["employer_load"] = employer_load
            st.session_state.objects[object_key]["labor_total"] = labor_total

            st.session_state.objects[object_key]["overhead_cost"] = overhead_cost
            st.session_state.objects[object_key]["overhead_vat"] = overhead_vat
            st.session_state.objects[object_key]["overhead_total"] = overhead_total

            st.session_state.objects[object_key]["self_cost_excl_vat"] = self_cost_excl_vat
            st.session_state.objects[object_key]["self_cost_vat"] = self_cost_vat
            st.session_state.objects[object_key]["self_cost_total"] = self_cost_total

            approved_input_key = f"sale_price_input_{object_key}"
            approved_source_key = f"{approved_input_key}_unit_cost_source"

            st.session_state[approved_input_key] = format_money(round(self_cost_excl_vat * 1.30))
            st.session_state[approved_source_key] = self_cost_excl_vat

            st.session_state.screen = "objects"
            st.rerun()

# Proposal preview screen. This is still a demo markdown preview.
def render_proposal_screen():
    ensure_objects_state()

    render_screen_header(
        "Proposal preview",
        "Client-facing draft generated from approved objects and project-level pricing.",
    )

    objects = st.session_state.objects
    final_price = st.session_state.get(
        "total_price",
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
| Delivery | {format_money(st.session_state.get("delivery_price", 0))} |
| Installation | {format_money(st.session_state.get("installation_price", 0))} |
| VAT 18% | {format_money(st.session_state.get("vat", 0))} |

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
    st.dataframe(purchasing, width="stretch", hide_index=True)

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
    st.dataframe(production, width="stretch", hide_index=True)

    nav_buttons("objects", None)

    if st.button("Start over", key="proposal_start_over", width="stretch"):
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Router
# -----------------------------------------------------------------------------

apply_css()
apply_bottom_action_button_css()

if "screen" not in st.session_state:
    st.session_state.screen = "upload"

current_route_signature = (
    st.session_state.get("screen"),
    st.session_state.get("current_object"),
)

previous_route_signature = st.session_state.get("_last_route_signature")

if (
    previous_route_signature is not None
    and previous_route_signature != current_route_signature
):
    request_scroll_to_top()

st.session_state._last_route_signature = current_route_signature

if st.session_state.screen == "upload":
    render_upload_screen()
elif st.session_state.screen == "processing":
    render_processing_screen()
elif st.session_state.screen == "estimate_processing":
    render_estimate_processing_screen()
elif st.session_state.screen == "objects":
    render_objects_screen()
elif st.session_state.screen == "object_processing":
    render_object_processing_screen()
elif st.session_state.screen == "object_detail":
    render_object_detail_screen()
elif st.session_state.screen == "proposal":
    render_proposal_screen()
else:
    st.session_state.screen = "upload"
    st.rerun()

run_scroll_to_top_if_requested()
