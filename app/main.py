import sqlite3
from io import BytesIO
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from pypdf import PdfReader

from src.resume_matcher import match_resume_to_jobs


# Locate the project files relative to this file.
project_root = Path(__file__).resolve().parent.parent
database_path = project_root / "data" / "jobs.db"
model_path = project_root / "models" / "salary_xgb_pipeline.joblib"

# Load the saved salary prediction pipeline once when the API starts.
salary_model = joblib.load(model_path)

app = FastAPI(
    title="Job Market Intelligence API",
    description="API for historical job market analysis and salary prediction.",
    version="0.1.0",
)


class SalaryPredictionRequest(BaseModel):
    """Validate job details sent to the salary prediction endpoint."""

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
    """Predict a historical listed salary midpoint in LPA."""
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
        "note": (
            "Estimate from historical 2019 listed salaries; "
            "not a current offer guarantee."
        ),
    }


@app.post("/match/resume")
async def match_resume(file: UploadFile = File(...)):
    """Rank historical postings against an uploaded PDF resume."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

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

    with sqlite3.connect(database_path) as connection:
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


@app.get("/dashboard/summary")
def dashboard_summary():
    """Return posting and salary summaries for the dashboard."""
    with sqlite3.connect(database_path) as connection:
        total_postings = pd.read_sql_query(
            "SELECT COUNT(*) AS count FROM job_postings_clean",
            connection,
        )["count"].iloc[0]

        salary_data = pd.read_sql_query(
            """
            SELECT salary_mid_lpa
            FROM job_postings_clean
            WHERE salary_mid_lpa IS NOT NULL
            """,
            connection,
        )["salary_mid_lpa"]

        top_locations = pd.read_sql_query(
            """
            SELECT Location AS location, COUNT(*) AS posting_count
            FROM job_postings_clean
            WHERE Location IS NOT NULL AND TRIM(Location) != ''
            GROUP BY Location
            ORDER BY posting_count DESC
            LIMIT 10
            """,
            connection,
        )

    return {
        "total_postings": int(total_postings),
        "postings_with_salary": int(salary_data.count()),
        "mean_salary_lpa": (
            round(float(salary_data.mean()), 2)
            if not salary_data.empty
            else None
        ),
        "median_salary_lpa": (
            round(float(salary_data.median()), 2)
            if not salary_data.empty
            else None
        ),
        "top_locations": top_locations.to_dict(orient="records"),
    }

@app.get("/dashboard/skills")
def dashboard_skills(role: str | None = None, location: str | None = None):
    """Return the most requested technical skills, optionally filtered by role and city."""
    query = """
        SELECT
            skills.skill,
            COUNT(DISTINCT skills.job_id) AS posting_count
        FROM job_technical_skills AS skills
        JOIN job_postings_clean AS jobs
            ON jobs."Uniq Id" = skills.job_id
        WHERE 1 = 1
    """
    parameters = []

    # Add filters only when the caller provides them.
    if role:
        query += ' AND jobs."Role" = ?'
        parameters.append(role)

    if location:
        query += ' AND jobs."Location" LIKE ?'
        parameters.append(f"%{location}%")

    query += """
        GROUP BY skills.skill
        ORDER BY posting_count DESC
        LIMIT 15
    """

    with sqlite3.connect(database_path) as connection:
        skills = pd.read_sql_query(query, connection, params=parameters)

    return {
        "role": role,
        "location": location,
        "skills": skills.to_dict(orient="records"),
    }

@app.get("/dashboard/salary-by-experience")
def salary_by_experience():
    """Return listed salary summaries grouped by experience band."""
    import re

    with sqlite3.connect(database_path) as connection:
        rows = pd.read_sql_query(
            """
            SELECT
                "Job Experience Required" AS experience,
                salary_mid_lpa
            FROM job_postings_clean
            WHERE salary_mid_lpa IS NOT NULL
              AND "Job Experience Required" IS NOT NULL
            """,
            connection,
        )

    def experience_midpoint(value):
        numbers = re.findall(r"\d+(?:\.\d+)?", str(value))
        if not numbers:
            return None

        values = [float(number) for number in numbers[:2]]
        return sum(values) / len(values)

    rows["experience_mid_years"] = rows["experience"].map(experience_midpoint)
    rows = rows.dropna(subset=["experience_mid_years"])

    def experience_band(years):
        if years <= 2:
            return "Up to 2"
        if years <= 5:
            return "Over 2 to 5"
        if years <= 10:
            return "Over 5 to 10"
        return "Over 10"

    rows["experience_band"] = rows["experience_mid_years"].map(experience_band)

    summary = (
        rows.groupby("experience_band")["salary_mid_lpa"]
        .agg(posting_count="count", median_salary_lpa="median", mean_salary_lpa="mean")
        .reindex(["Up to 2", "Over 2 to 5", "Over 5 to 10", "Over 10"])
        .dropna()
        .reset_index()
    )

    summary["median_salary_lpa"] = summary["median_salary_lpa"].round(2)
    summary["mean_salary_lpa"] = summary["mean_salary_lpa"].round(2)

    return {"salary_by_experience": summary.to_dict(orient="records")}