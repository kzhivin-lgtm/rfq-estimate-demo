import streamlit as st

st.set_page_config(
    page_title="RFQ-to-Estimate Copilot",
    layout="wide",
)

st.title("RFQ-to-Estimate Copilot")
st.write("Demo app is running.")

st.markdown("---")

uploaded_file = st.file_uploader(
    "Drop your RFQ file here",
    type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "dwg", "dxf"],
)

if uploaded_file is not None:
    st.success("File detected")

    st.write("Filename:", uploaded_file.name)
    st.write("Size:", f"{uploaded_file.size / 1024:.1f} KB")
    st.info(
        "Demo mode: we detected your file, but this demo will use a sample RFQ "
        "to show the full workflow."
    )