import time
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="RFQ-to-Estimate Copilot",
    page_icon="📐",
    layout="wide",
)


APP_TITLE = "RFQ-to-Estimate Copilot"
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


def load_demo_project():
    return {
        "Project ID": "RA-N01",
        "Project name": "RA-N01 — Kitchen / Island / Shelf package",
        "Company": COMPANY_NAME,
        "Author": "Abdallah",
        "Date": "16/02/2026",
        "Source file": "RA-N01_20260216.pdf",
        "Document type": "Technical drawing package / millwork RFQ",
        "Pages detected": "12",
        "Scale": "1:10",
        "Detected scope": "Kitchen, island, wall shelf, stainless steel elements, stone surfaces",
        "Confidence": "medium-high",
    }


def load_scope_items():
    return pd.DataFrame(
        [
            {
                "scope item": "main kitchen run",
                "zone": "kitchen",
                "qty": 1,
                "detected dimensions": "approx. 509.5 cm length, 294 cm height",
                "materials / finish": "stainless steel exterior, formica birman 2650 interior",
                "confidence": "87%",
                "status": "needs review",
            },
            {
                "scope item": "kitchen island",
                "zone": "island",
                "qty": 1,
                "detected dimensions": "approx. 449.5 cm length, 100–110 cm height",
                "materials / finish": "stainless steel exterior, stone marble laba rosa countertop/backplash",
                "confidence": "84%",
                "status": "needs review",
            },
            {
                "scope item": "upper shelf structure",
                "zone": "wall shelf",
                "qty": 1,
                "detected dimensions": "long open shelf with vertical partitions",
                "materials / finish": "oak veneer nextdoor / corten partitions",
                "confidence": "79%",
                "status": "needs review",
            },
            {
                "scope item": "tall side storage unit",
                "zone": "left side",
                "qty": 1,
                "detected dimensions": "approx. 60 cm width, 294 cm height",
                "materials / finish": "stainless steel / interior formica",
                "confidence": "76%",
                "status": "needs review",
            },
            {
                "scope item": "countertop surfaces",
                "zone": "kitchen + island",
                "qty": 2,
                "detected dimensions": "long surfaces, exact cutouts to verify",
                "materials / finish": "stone marble laba rosa",
                "confidence": "72%",
                "status": "missing supplier",
            },
            {
                "scope item": "backsplash surfaces",
                "zone": "kitchen + island",
                "qty": 2,
                "detected dimensions": "backsplash shown in drawings",
                "materials / finish": "stainless steel / stone marble laba rosa",
                "confidence": "68%",
                "status": "missing supplier",
            },
            {
                "scope item": "handles",
                "zone": "kitchen + island",
                "qty": 1,
                "detected dimensions": "domicile 05837.70.13 mentioned",
                "materials / finish": "handles domicile 05837.70.13",
                "confidence": "82%",
                "status": "verify quantity",
            },
            {
                "scope item": "toe kick",
                "zone": "kitchen + island",
                "qty": 1,
                "detected dimensions": "shown along lower run",
                "materials / finish": "metal / stainless steel by sample",
                "confidence": "75%",
                "status": "missing supplier",
            },
            {
                "scope item": "delivery and installation",
                "zone": "site",
                "qty": 1,
                "detected dimensions": "large custom installation",
                "materials / finish": "labor / site work",
                "confidence": "61%",
                "status": "requires site info",
            },
        ]
    )


def load_materials():
    return pd.DataFrame(
        [
            {
                "material": "stainless steel",
                "where detected": "kitchen exterior, island exterior, toe kick, countertop/backsplash notes",
                "supplier": "missing",
                "confidence": "86%",
            },
            {
                "material": "formica birman 2650",
                "where detected": "kitchen interior, island interior",
                "supplier": "not specified",
                "confidence": "88%",
            },
            {
                "material": "stone marble laba rosa",
                "where detected": "island countertop and backsplash",
                "supplier": "not specified",
                "confidence": "83%",
            },
            {
                "material": "oak veneer nextdoor",
                "where detected": "shelf exterior / partitions",
                "supplier": "by sample",
                "confidence": "78%",
            },
            {
                "material": "corten / tin corten",
                "where detected": "shelf partitions / detail notes",
                "supplier": "missing",
                "confidence": "74%",
            },
            {
                "material": "handles domicile 05837.70.13",
                "where detected": "kitchen + island handles",
                "supplier": "domicile",
                "confidence": "81%",
            },
        ]
    )


def load_missing_info():
    return pd.DataFrame(
        [
            {
                "missing / uncertain item": "stainless steel supplier",
                "why it matters": "affects metal price, lead time, finish quality",
                "suggested question": "Please confirm the stainless steel supplier / sample approval.",
                "priority": "high",
            },
            {
                "missing / uncertain item": "stone supplier and slab availability",
                "why it matters": "stone marble laba rosa cost depends on supplier, slab size, cutouts",
                "suggested question": "Please confirm supplier, slab thickness and availability for Laba Rosa.",
                "priority": "high",
            },
            {
                "missing / uncertain item": "handles quantity",
                "why it matters": "drawing mentions handle model but quantity needs validation",
                "suggested question": "Please confirm exact handle quantity for kitchen and island fronts.",
                "priority": "medium",
            },
            {
                "missing / uncertain item": "site access and installation constraints",
                "why it matters": "large island and kitchen run may require special delivery / lifting",
                "suggested question": "Please confirm floor, elevator dimensions, parking and installation hours.",
                "priority": "high",
            },
            {
                "missing / uncertain item": "final site measurement",
                "why it matters": "dimensions in drawings must be validated before production",
                "suggested question": "Should final measurement be included before manufacturing release?",
                "priority": "high",
            },
            {
                "missing / uncertain item": "appliance / sink / cutout confirmation",
                "why it matters": "cutouts affect stone, metal and cabinet production",
                "suggested question": "Please confirm sink, cooktop, appliance and ventilation cutout specifications.",
                "priority": "high",
            },
        ]
    )


def load_estimate_lines():
    return pd.DataFrame(
        [
            {
                "category": "cabinetry",
                "line item": "main kitchen run fabrication",
                "qty": 1,
                "unit": "lot",
                "direct cost": 14500,
                "labor hours": 54,
                "margin": "35%",
                "total": 22300,
            },
            {
                "category": "cabinetry",
                "line item": "kitchen island fabrication",
                "qty": 1,
                "unit": "lot",
                "direct cost": 11800,
                "labor hours": 42,
                "margin": "35%",
                "total": 17900,
            },
            {
                "category": "shelf",
                "line item": "upper open shelf with partitions",
                "qty": 1,
                "unit": "lot",
                "direct cost": 7600,
                "labor hours": 32,
                "margin": "35%",
                "total": 11900,
            },
            {
                "category": "metal",
                "line item": "stainless steel exterior / toe kick / panels",
                "qty": 1,
                "unit": "allowance",
                "direct cost": 9200,
                "labor hours": 18,
                "margin": "30%",
                "total": 13200,
            },
            {
                "category": "stone",
                "line item": "laba rosa countertop and backsplash allowance",
                "qty": 1,
                "unit": "allowance",
                "direct cost": 18500,
                "labor hours": 10,
                "margin": "25%",
                "total": 24500,
            },
            {
                "category": "hardware",
                "line item": "handles, hinges, slides and fittings",
                "qty": 1,
                "unit": "allowance",
                "direct cost": 4800,
                "labor hours": 0,
                "margin": "30%",
                "total": 6600,
            },
            {
                "category": "installation",
                "line item": "delivery and on-site installation",
                "qty": 1,
                "unit": "lot",
                "direct cost": 7200,
                "labor hours": 32,
                "margin": "30%",
                "total": 10200,
            },
            {
                "category": "project management",
                "line item": "shop drawings review, coordination, revisions",
                "qty": 1,
                "unit": "lot",
                "direct cost": 4200,
                "labor hours": 16,
                "margin": "30%",
                "total": 5900,
            },
        ]
    )


def load_drawing_pages():
    return pd.DataFrame(
        [
            {
                "page": "1",
                "detected content": "3D overview, material board, scope notes",
                "used for": "project metadata, materials, item list",
            },
            {
                "page": "2–8",
                "detected content": "plans, elevations, sections, dimensions",
                "used for": "dimensions, units, fabrication complexity",
            },
            {
                "page": "9–10",
                "detected content": "3D views of kitchen and island",
                "used for": "visual validation, scope confirmation",
            },
            {
                "page": "11–12",
                "detected content": "exploded parts / component references",
                "used for": "part count, production complexity",
            },
        ]
    )


def load_similar_projects():
    return pd.DataFrame(
        [
            {
                "similar project": "high-end residential kitchen with metal finish",
                "similarity": "84%",
                "historical price": "₪96,000",
                "note": "similar kitchen run and island scale",
            },
            {
                "similar project": "custom island with stone countertop",
                "similarity": "77%",
                "historical price": "₪48,000",
                "note": "similar stone and installation complexity",
            },
            {
                "similar project": "open wall shelf with veneer partitions",
                "similarity": "71%",
                "historical price": "₪21,000",
                "note": "similar shelf structure, different finish",
            },
        ]
    )


def show_processing_animation():
    steps = [
        "reading drawing package...",
        "detecting title block and project metadata...",
        "identifying millwork scope...",
        "extracting material notes...",
        "checking missing information...",
        "preparing estimate draft...",
    ]

    progress = st.progress(0)
    status = st.empty()

    for i, step in enumerate(steps, start=1):
        status.write(step)
        progress.progress(i / len(steps))
        time.sleep(0.25)

    status.success("analysis ready")


if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False

if "analysis_ready" not in st.session_state:
    st.session_state.analysis_ready = False


st.title(APP_TITLE)
st.caption("turn technical drawings, PDFs and RFQs into a structured estimate draft.")

st.markdown(
    """
<style>
.block-container {
    padding-top: 2rem;
}
.big-upload-box {
    border: 1px dashed #bbb;
    border-radius: 14px;
    padding: 26px;
    background: #fafafa;
}
.small-muted {
    color: #777;
    font-size: 0.9rem;
}
</style>
""",
    unsafe_allow_html=True,
)


if not st.session_state.analysis_ready:
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown("## drop your RFQ / drawing package")
        st.markdown(
            """
            <div class="big-upload-box">
            upload a PDF, drawing package, BOQ, image or Excel file.  
            this demo uses a real 8DOOR drawing package as the sample workflow.
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "drop your file here",
            type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "dwg", "dxf"],
            label_visibility="collapsed",
        )

        col_a, col_b = st.columns(2)
        start_sample = col_a.button("use sample RA-N01 drawing package", use_container_width=True)
        reset = col_b.button("reset", use_container_width=True)

        if reset:
            st.session_state.analysis_started = False
            st.session_state.analysis_ready = False
            st.rerun()

        if uploaded_file is not None:
            st.success("file detected")

            c1, c2, c3 = st.columns(3)
            c1.metric("filename", uploaded_file.name)
            c2.metric("type", detect_file_type(uploaded_file.name))
            c3.metric("size", format_file_size(uploaded_file.size))

            st.info(
                "demo mode: we detected your uploaded file, but this interactive demo "
                "uses the real 8DOOR sample drawing package RA-N01 to show the full workflow."
            )

            if st.button("analyze with sample workflow", use_container_width=True):
                st.session_state.analysis_started = True

        if start_sample:
            st.session_state.analysis_started = True

    with right:
        st.markdown("## what this demo shows")
        st.write("1. file intake")
        st.write("2. detected project metadata")
        st.write("3. extracted scope")
        st.write("4. materials and missing info")
        st.write("5. estimate draft")
        st.write("6. proposal preview")

        st.markdown("---")
        st.markdown("**sample file:** RA-N01_20260216.pdf")
        st.markdown("**company:** 8DOOR")
        st.markdown("**document type:** technical millwork drawing package")
        st.markdown("**pages:** 12")

    if st.session_state.analysis_started:
        st.markdown("---")
        show_processing_animation()
        st.session_state.analysis_ready = True
        st.rerun()


else:
    project = load_demo_project()
    scope_df = load_scope_items()
    materials_df = load_materials()
    missing_df = load_missing_info()
    estimate_df = load_estimate_lines()
    pages_df = load_drawing_pages()
    similar_df = load_similar_projects()

    st.markdown("## detected project")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("project", project["Project ID"])
    m2.metric("company", project["Company"])
    m3.metric("pages", project["Pages detected"])
    m4.metric("document type", "drawings")
    m5.metric("confidence", project["Confidence"])

    with st.expander("project metadata", expanded=True):
        meta_df = pd.DataFrame(
            [{"field": key, "detected value": value} for key, value in project.items()]
        )
        st.dataframe(meta_df, use_container_width=True, hide_index=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "drawing package",
            "extracted scope",
            "materials",
            "missing info",
            "estimate draft",
            "proposal preview",
        ]
    )

    with tab1:
        st.markdown("### drawing package analysis")
        st.write(
            "the system classifies the PDF as a technical millwork drawing package, "
            "not a text RFQ. it uses title blocks, material notes, dimensions, 3D views "
            "and exploded components to prepare the first estimate draft."
        )
        st.dataframe(pages_df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### extracted scope")
        st.write("draft scope extracted from drawings. estimator should review before pricing.")
        edited_scope = st.data_editor(
            scope_df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

    with tab3:
        st.markdown("### detected materials and finishes")
        edited_materials = st.data_editor(
            materials_df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

    with tab4:
        st.markdown("### missing information")
        st.write("questions that should be confirmed before final quotation.")
        edited_missing = st.data_editor(
            missing_df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

        st.markdown("#### clarification message draft")
        st.markdown(
            """
Hi,

before we finalize the quotation for RA-N01, please confirm:

- stainless steel supplier / approved sample;
- Laba Rosa stone supplier, slab thickness and availability;
- exact handle quantity for kitchen and island;
- site access, elevator dimensions, parking and installation constraints;
- final site measurement before production;
- sink / cooktop / appliance / ventilation cutout specifications.

Once confirmed, we can update the estimate and prepare the final proposal.
"""
        )

    with tab5:
        st.markdown("### estimate draft")
        st.write("first structured draft. prices are demo estimates and require human review.")

        edited_estimate = st.data_editor(
            estimate_df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

        total = int(edited_estimate["total"].sum())
        direct_cost = int(edited_estimate["direct cost"].sum())
        labor_hours = int(edited_estimate["labor hours"].sum())

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("direct cost", f"₪{direct_cost:,.0f}")
        c2.metric("labor hours", f"{labor_hours}")
        c3.metric("suggested price", f"₪{total:,.0f}")
        c4.metric("estimate confidence", "medium")

        st.markdown("#### pricing options")
        pricing_options = pd.DataFrame(
            [
                {"option": "lean", "description": "minimum allowance, estimator review required", "price": f"₪{int(total * 0.92):,}"},
                {"option": "standard", "description": "recommended draft price", "price": f"₪{total:,}"},
                {"option": "premium", "description": "higher buffer for stone/metal uncertainty", "price": f"₪{int(total * 1.15):,}"},
            ]
        )
        st.dataframe(pricing_options, use_container_width=True, hide_index=True)

        st.markdown("#### similar past projects")
        st.dataframe(similar_df, use_container_width=True, hide_index=True)

    with tab6:
        total = int(estimate_df["total"].sum())
        lean = int(total * 0.92)
        premium = int(total * 1.15)

        st.markdown("### commercial proposal preview")

        proposal = f"""
# commercial proposal

**project:** RA-N01 — kitchen / island / shelf package  
**company:** {COMPANY_NAME}  
**document:** technical drawing package dated 16/02/2026  
**prepared from:** RA-N01_20260216.pdf  

## scope included

- main kitchen run fabrication
- kitchen island fabrication
- upper open shelf with partitions
- tall side storage unit
- stainless steel exterior / toe kick / panels
- formica birman 2650 interior finish
- oak veneer / corten shelf elements
- stone marble laba rosa countertop and backsplash allowance
- hardware allowance
- delivery and installation

## pricing options

| option | price |
|---|---:|
| lean | ₪{lean:,} |
| standard | ₪{total:,} |
| premium | ₪{premium:,} |

## assumptions

- final site measurement is required before production release
- stainless steel supplier / sample must be confirmed
- stone supplier, slab thickness and cutouts must be confirmed
- handle quantity must be verified
- appliance, sink and ventilation cutouts must be confirmed
- installation assumes standard access, elevator availability and regular working hours

## not included

- electrical work
- plumbing
- stone supplier price changes after quotation
- special lifting / crane / non-standard access
- after-hours installation
- changes after production approval

## status

this is an AI-assisted draft. final quotation requires estimator review and approval.
"""
        st.markdown(proposal)

    st.markdown("---")
    if st.button("start over", use_container_width=True):
        st.session_state.analysis_started = False
        st.session_state.analysis_ready = False
        st.rerun()