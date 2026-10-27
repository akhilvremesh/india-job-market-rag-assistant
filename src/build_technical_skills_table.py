from pathlib import Path
import sqlite3

import pandas as pd

from src.technical_skill_matcher import extract_technical_skills


def build_technical_skill_rows(jobs):
    """Make one row per posting and recognized technical skill."""
    rows = []

    for _, job in jobs.iterrows():
        if pd.isna(job["Key Skills"]):
            continue

        job_id = str(job["Uniq Id"])
        skills = extract_technical_skills(job["Key Skills"])

        for skill in skills:
            rows.append({"job_id": job_id, "skill": skill})

    result = pd.DataFrame(rows, columns=["job_id", "skill"])
    return result.drop_duplicates(subset=["job_id", "skill"])


def main():
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "jobs.db"

    connection = sqlite3.connect(database_path)

    try:
        jobs = pd.read_sql_query(
            'SELECT "Uniq Id", "Key Skills" FROM job_postings_clean',
            connection,
        )

        technical_skills = build_technical_skill_rows(jobs)

        technical_skills.to_sql(
            "job_technical_skills",
            connection,
            if_exists="replace",
            index=False,
        )
    finally:
        connection.close()

    print(f"Cleaned postings checked: {len(jobs)}")
    print(f"Postings with recognized technical skills: "
          f"{technical_skills['job_id'].nunique()}")
    print(f"Technical job-skill rows saved: {len(technical_skills)}")
    print(f"Distinct technical skills found: "
          f"{technical_skills['skill'].nunique()}")


if __name__ == "__main__":
    main()