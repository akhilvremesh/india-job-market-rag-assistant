import sqlite3
import pandas as pd


# Each pair is the label to put in the document and its CSV/SQLite column.
JOB_FIELDS = [
    ("Job title", "Job Title"),
    ("Role", "Role"),
    ("Role category", "Role Category"),
    ("Functional area", "Functional Area"),
    ("Industry", "Industry"),
    ("Location", "Location"),
    ("Experience", "Job Experience Required"),
    ("Skills", "Key Skills"),
    ("Salary", "Job Salary"),
]


def clean_field(value):
    """Return clean text, or empty text when a field is missing."""
    if pd.isna(value):
        return ""

    return str(value).strip()


def build_job_document(row):
    """Turn one job row into readable text for semantic search."""
    lines = []

    for label, column in JOB_FIELDS:
        value = clean_field(row[column])

        # Leave missing fields out instead of writing "nan".
        if value:
            lines.append(f"{label}: {value}")

    return "\n".join(lines)


def load_job_documents(database_path="data/jobs.db"):
    """Load cleaned jobs and create one document string for each job."""
    connection = sqlite3.connect(database_path)

    jobs = pd.read_sql_query(
        "SELECT * FROM job_postings_clean",
        connection,
    )

    connection.close()

    # apply() runs build_job_document once for each row.
    jobs["document"] = jobs.apply(build_job_document, axis=1)

    # Chroma requires document IDs to be strings.
    jobs["document_id"] = jobs["Uniq Id"].astype(str)

    return jobs


if __name__ == "__main__":
    jobs = load_job_documents()

    print(f"Documents created: {len(jobs)}")

    # Show three examples to check the text and IDs.
    for _, row in jobs.head(3).iterrows():
        print(f"\nDocument ID: {row['document_id']}")
        print(row["document"])
        print("-" * 60)