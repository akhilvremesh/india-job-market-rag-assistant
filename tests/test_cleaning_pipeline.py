import pandas as pd

from src.cleaning_pipeline import clean_jobs_dataframe


def test_pipeline_trims_deduplicates_and_parses_salary():
    sample_jobs = pd.DataFrame(
        [
            {
                "Uniq Id": "job-1",
                "Job Title": " Python Developer ",
                "Job Salary": "6-10 LPA",
                "Location": " Bangalore ",
            },
            {
                "Uniq Id": "job-1",
                "Job Title": "Duplicate posting",
                "Job Salary": "Not Disclosed by Recruiter",
                "Location": "Mumbai",
            },
            {
                "Uniq Id": "job-2",
                "Job Title": "   ",
                "Job Salary": "INR 3,00,000 - 7,00,000 PA",
                "Location": "Pune",
            },
        ]
    )

    cleaned = clean_jobs_dataframe(sample_jobs)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["Job Title"] == "Python Developer"
    assert cleaned.iloc[0]["Location"] == "Bengaluru"
    assert cleaned.iloc[0]["salary_min_lpa"] == 6.0
    assert cleaned.iloc[0]["salary_max_lpa"] == 10.0
    assert cleaned.iloc[0]["salary_mid_lpa"] == 8.0