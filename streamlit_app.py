import requests
import streamlit as st


# Set the browser tab title and use a wide layout.
st.set_page_config(
    page_title="Job Market Intelligence",
    page_icon="📊",
    layout="wide",
)

API_URL = "http://127.0.0.1:8000"

st.title("Job Market Intelligence Platform")
st.write(
    "Explore historical job market patterns, estimate listed salaries, "
    "and compare a resume with job postings."
)

st.info(
    "The job dataset contains historical 2019 postings. "
    "It does not show currently available jobs."
)

# Check whether FastAPI is reachable.
try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    response.raise_for_status()
    st.success("Backend API is running.")
except requests.RequestException:
    st.error(
        "Could not reach the backend. Start FastAPI in another terminal with: "
        "`python -m uvicorn app.main:app --reload`"
    )

st.subheader("Project features")
st.markdown(
    """
    - **Dashboard:** explore skills, locations, and salary patterns.
    - **Salary predictor:** estimate a historical listed salary midpoint.
    - **Resume matcher:** find similar postings and recognized missing skills.
    """
)