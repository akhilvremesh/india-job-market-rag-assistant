import requests
import streamlit as st


try:
    API_URL = st.secrets["API_URL"]
except (KeyError, FileNotFoundError):
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Salary Predictor", page_icon="💰")
st.title("Salary Predictor")
st.caption("Estimate a listed salary midpoint using the historical 2019 model.")

# Collect the job details when the user clicks the button.
with st.form("salary_form"):
    job_title = st.text_input("Job title", value="Python Data Analyst")
    key_skills = st.text_input("Skills", value="Python, SQL, pandas")
    functional_area = st.text_input(
        "Functional area",
        value="Data Science and Analytics",
    )
    role = st.text_input("Role", value="Data Analyst")
    location = st.text_input("City", value="Bengaluru")
    role_category = st.text_input("Role category", value="Programming & Design")
    industry = st.text_input(
        "Industry",
        value="IT-Software, Software Services",
    )
    experience = st.number_input(
        "Experience (years)",
        min_value=0.0,
        max_value=50.0,
        value=2.5,
        step=0.5,
    )

    submitted = st.form_submit_button("Estimate salary")

if submitted:
    # Send the form values to the FastAPI prediction endpoint.
    payload = {
        "job_title": job_title,
        "key_skills": key_skills,
        "functional_area": functional_area,
        "role": role,
        "location": location,
        "role_category": role_category,
        "industry": industry,
        "experience_mid_years": experience,
    }

    try:
        response = requests.post(
            f"{API_URL}/predict/salary",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        st.metric(
            "Estimated listed salary midpoint",
            f"{result['predicted_salary_lpa']:.2f} LPA",
        )
        st.info(result["note"])
    except requests.RequestException as error:
        st.error(f"Could not get a prediction from the API: {error}")