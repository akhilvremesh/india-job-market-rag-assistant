from pathlib import Path
import sqlite3

import pandas as pd

from src.location_cleaner import normalize_location
from src.salary_parser import parse_salary_lpa


def clean_jobs_dataframe(df):
    """Clean job rows and add parsed salary columns."""
    cleaned = df.copy()

    # Trim extra spaces from text values without changing non-text values
    for column in cleaned.columns:
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Remove repeated posting IDs, keeping the first occurrence
    if "Uniq Id" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset="Uniq Id", keep="first")

    # Remove rows whose job title is missing or empty after trimming
    if "Job Title" in cleaned.columns:
        has_title = cleaned["Job Title"].notna() & cleaned["Job Title"].ne("")
        cleaned = cleaned.loc[has_title].copy()

    # Normalize non-missing locations
    if "Location" in cleaned.columns:
        cleaned["Location"] = cleaned["Location"].map(
            lambda value: (
                normalize_location(value)
                if not pd.isna(value)
                else None
            )
        )

    # Parse salary into minimum, maximum, and midpoint values in LPA
    if "Job Salary" in cleaned.columns:
        parsed_salaries = cleaned["Job Salary"].map(parse_salary_lpa)

        cleaned["salary_min_lpa"] = parsed_salaries.map(
            lambda result: result[0] if result is not None else None
        )
        cleaned["salary_max_lpa"] = parsed_salaries.map(
            lambda result: result[1] if result is not None else None
        )
        cleaned["salary_mid_lpa"] = parsed_salaries.map(
            lambda result: result[2] if result is not None else None
        )

    return cleaned


def main():
    """Read raw jobs, clean them, and replace the clean database table."""
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "jobs.db"

    connection = sqlite3.connect(database_path)

    try:
        raw_jobs = pd.read_sql_query(
            "SELECT * FROM job_postings_raw",
            connection,
        )

        clean_jobs = clean_jobs_dataframe(raw_jobs)

        clean_jobs.to_sql(
            "job_postings_clean",
            connection,
            if_exists="replace",
            index=False,
        )
    finally:
        connection.close()

    print(f"Raw rows: {len(raw_jobs)}")
    print(f"Clean rows: {len(clean_jobs)}")
    print("Updated table: job_postings_clean")


if __name__ == "__main__":
    main()