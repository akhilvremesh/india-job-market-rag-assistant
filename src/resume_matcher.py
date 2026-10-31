import re
import sqlite3
from pathlib import Path

import pandas as pd
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TECHNICAL_SKILLS = [
    "python", "java", "sql", "javascript", "html", "css",
    "react", "node.js", "mysql", "linux", "aws", "azure",
    "git", "docker", "machine learning", "data analysis",
    "excel", "tableau", "power bi",
]


def extract_resume_text(pdf_path: str | Path) -> str:
    """Extract and combine selectable text from all pages in a PDF."""
    reader = PdfReader(str(pdf_path))
    page_texts = []

    for page in reader.pages:
        page_texts.append(page.extract_text() or "")

    return "\n".join(page_texts).strip()


def match_resume_to_jobs(
    resume_text: str,
    jobs_df: pd.DataFrame,
    top_n: int = 5,
) -> pd.DataFrame:
    """Rank job postings by text similarity and list missing technical skills."""
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    # Combine each posting's title, role, and skills into searchable text.
    job_texts = (
        jobs_df["Job Title"].fillna("").astype(str)
        + " "
        + jobs_df["Role"].fillna("").astype(str)
        + " "
        + jobs_df["Key Skills"].fillna("").astype(str)
    )

    # Convert the resume and postings into word-based numeric vectors.
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )
    all_vectors = vectorizer.fit_transform(
        [resume_text, *job_texts.tolist()]
    )

    # Compare the resume vector with each posting vector.
    scores = cosine_similarity(
        all_vectors[0:1],
        all_vectors[1:],
    ).flatten()

    results = jobs_df[
        ["Uniq Id", "Job Title", "Role", "Location"]
    ].copy()
    results["match_score"] = scores

    # Match whole skill names, so "java" does not match "javascript".
    def contains_skill(text: str, skill: str) -> bool:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None

    # Find skills requested by each posting but absent from the resume.
    def missing_skills(job_text: str) -> list[str]:
        return [
            skill
            for skill in TECHNICAL_SKILLS
            if contains_skill(job_text, skill)
            and not contains_skill(resume_text, skill)
        ]

    results["missing_skills"] = [
        missing_skills(text)
        for text in job_texts
    ]

    return (
        results.sort_values("match_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    # Build database and resume paths from the project root.
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "jobs.db"
    resume_path = project_root / "data" / "resume.pdf"

    # Extract selectable text from the resume PDF.
    resume_text = extract_resume_text(resume_path)

    # Load the posting fields used by the matcher.
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

    # Find and print the five closest text matches.
    matches = match_resume_to_jobs(resume_text, jobs, top_n=5)

    print("Top job matches:")
    for _, match in matches.iterrows():
        print(f"\nTitle: {match['Job Title']}")
        print(f"Role: {match['Role']}")
        print(f"Location: {match['Location']}")
        print(f"Text similarity: {match['match_score']:.3f}")

        missing = ", ".join(match["missing_skills"]) or "None"
        print("Missing skills:", missing)