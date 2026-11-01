import requests
import streamlit as st


try:
    API_URL = st.secrets["API_URL"]
except (KeyError, FileNotFoundError):
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("Resume Matcher")
st.caption("Compare a PDF resume with historical job postings.")

resume_file = st.file_uploader(
    "Choose a text-based PDF resume",
    type=["pdf"],
)

if resume_file is not None:
    if st.button("Find matching jobs"):
        # Send the PDF bytes to FastAPI as a multipart file upload.
        uploaded_file = {
            "file": (
                resume_file.name,
                resume_file.getvalue(),
                "application/pdf",
            )
        }

        try:
            response = requests.post(
                f"{API_URL}/match/resume",
                files=uploaded_file,
                timeout=180,
            )
            response.raise_for_status()
            result = response.json()

            st.info(result["note"])

            for index, match in enumerate(result["matches"], start=1):
                with st.expander(
                    f"{index}. {match['job_title']} — {match['similarity_score']:.3f}"
                ):
                    st.write("**Role:**", match["role"])
                    st.write("**Location:**", match["location"])

                    missing = match["missing_skills"]
                    st.write(
                        "**Recognized missing skills:**",
                        ", ".join(missing) if missing else "None found",
                    )

        except requests.RequestException as error:
            st.error(f"Could not get matches from the API: {error}")