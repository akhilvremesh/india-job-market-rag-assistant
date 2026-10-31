from pathlib import Path
from io import BytesIO

from fastapi import File, HTTPException, UploadFile
from pypdf import PdfReader
import sqlite3
from src.resume_matcher import match_resume_to_jobs
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field


# Locate and load the saved salary model from the project folder.
project_root = Path(__file__).resolve().parent.parent
model_path = project_root / "models" / "salary_xgb_pipeline.joblib"
salary_model = joblib.load(model_path)

app = FastAPI(
    title="Job Market Intelligence API",
    description="API for historical job market analysis and salary prediction.",
    version="0.1.0",
)


class SalaryPredictionRequest(BaseModel):
    """Validated job details sent to the salary prediction endpoint."""

    job_title: str = Field(min_length=1, examples=["Python Data Analyst"])
    key_skills: str = Field(default="", examples=["Python, SQL, pandas"])
    functional_area: str = Field(default="", examples=["Data Science and Analytics"])
    role: str = Field(default="Software Developer", examples=["Data Analyst"])
    location: str = Field(default="Bengaluru", examples=["Bengaluru"])
    role_category: str = Field(default="Programming & Design")
    industry: str = Field(default="IT-Software, Software Services")
    experience_mid_years: float | None = Field(default=None, ge=0, le=50)


@app.get("/health")
def health_check():
    """Report that the API is running."""
    return {"status": "ok"}


@app.post("/predict/salary")
def predict_salary(request: SalaryPredictionRequest):
    """Predict the historical listed salary midpoint in LPA."""
    # Build one row using the same feature names expected by the trained pipeline.
    input_row = pd.DataFrame(
        [
            {
                "job_text": (
                    f"{request.job_title} "
                    f"{request.key_skills} "
                    f"{request.functional_area}"
                ),
                "Role": request.role,
                "Location": request.location,
                "Role Category": request.role_category,
                "Industry": request.industry,
                "experience_mid_years": request.experience_mid_years,
            }
        ]
    )

    predicted_salary = float(salary_model.predict(input_row)[0])

    return {
        "predicted_salary_lpa": round(predicted_salary, 2),
        "note": "Estimate from historical 2019 listed salaries; not a current offer guarantee.",
    }
@app.post("/match/resume")
async def match_resume(file: UploadFile = File(...)):
    """Rank job postings against an uploaded PDF resume."""
    # Accept PDF uploads only.
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    # Read the uploaded PDF in memory; it is not saved to disk.
    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        resume_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please upload a valid text-based PDF.",
        ) from error

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="No selectable text was found in the PDF. Scanned resumes need OCR.",
        )

    # Read searchable postings from the project SQLite database.
    with sqlite3.connect(project_root / "data" / "jobs.db") as connection:
        jobs = pd.read_sql_query(
            """
            SELECT
                "Uniq Id",
                "Job Title",
                "Role",
                "Location",
                "Key Skills"
            FROM job_postings_clean
            """,
            connection,
        )

    matches = match_resume_to_jobs(resume_text, jobs, top_n=5)

    # Convert pandas rows into JSON-friendly dictionaries.
    return {
        "matches": [
            {
                "job_id": row["Uniq Id"],
                "job_title": row["Job Title"],
                "role": row["Role"],
                "location": row["Location"],
                "similarity_score": round(float(row["match_score"]), 3),
                "missing_skills": row["missing_skills"],
            }
            for _, row in matches.iterrows()
        ],
        "note": "Similarity measures text overlap; it is not a hiring probability.",
    }