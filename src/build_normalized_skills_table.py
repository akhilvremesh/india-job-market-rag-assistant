from pathlib import Path
import sqlite3

import pandas as pd

from src.skill_dictionary import extract_skills


def main():
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "jobs.db"

    connection = sqlite3.connect(database_path)

    try:
        jobs = pd.read_sql_query(
            'SELECT "Uniq Id", "Key Skills" FROM job_postings_clean',
            connection,
        )

        rows = []

        for _, job in jobs.iterrows():
            if pd.isna(job["Key Skills"]):
                continue

            job_id = str(job["Uniq Id"])

            for skill in extract_skills(job["Key Skills"]):
                rows.append({"job_id": job_id, "skill": skill})

        # Build a table with one row per unique job-skill pair
        skills = pd.DataFrame(rows, columns=["job_id", "skill"])
        skills = skills.drop_duplicates(subset=["job_id", "skill"])

        skills.to_sql(
            "job_skills_normalized",
            connection,
            if_exists="replace",
            index=False,
        )

    finally:
        connection.close()

    print(f"Cleaned job postings checked: {len(jobs)}")
    print(f"Normalized job-skill rows saved: {len(skills)}")
    print(f"Distinct normalized skill names: {skills['skill'].nunique()}")


if __name__ == "__main__":
    main()