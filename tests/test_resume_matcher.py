import pandas as pd

from src import resume_matcher


class FakePage:
    """Stand-in for one PDF page."""

    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


def test_extract_resume_text_joins_pages(monkeypatch, tmp_path):
    """Text from each page should be joined with a newline."""
    fake_pages = [FakePage("Python and SQL"), FakePage("Data analysis")]

    class FakePdfReader:
        def __init__(self, path):
            self.pages = fake_pages

    monkeypatch.setattr(resume_matcher, "PdfReader", FakePdfReader)

    result = resume_matcher.extract_resume_text(tmp_path / "sample.pdf")

    assert result == "Python and SQL\nData analysis"


def test_extract_resume_text_handles_empty_page(monkeypatch, tmp_path):
    """A page without extractable text should not cause an error."""

    class FakePdfReader:
        def __init__(self, path):
            self.pages = [FakePage(None), FakePage("Python")]

    monkeypatch.setattr(resume_matcher, "PdfReader", FakePdfReader)

    result = resume_matcher.extract_resume_text(tmp_path / "sample.pdf")

    assert result == "Python"


def test_match_resume_to_jobs_ranks_similar_job_and_finds_missing_skills():
    """A similar Python job should rank first and report absent job skills."""
    jobs = pd.DataFrame(
        [
            {
                "Uniq Id": "job-1",
                "Job Title": "Python Data Analyst",
                "Role": "Data Analyst",
                "Location": "Bengaluru",
                "Key Skills": "Python SQL AWS data analysis",
            },
            {
                "Uniq Id": "job-2",
                "Job Title": "Java Web Developer",
                "Role": "Software Developer",
                "Location": "Mumbai",
                "Key Skills": "Java HTML CSS",
            },
        ]
    )

    resume = "Python SQL data analysis"

    matches = resume_matcher.match_resume_to_jobs(
        resume,
        jobs,
        top_n=2,
    )

    assert matches.iloc[0]["Uniq Id"] == "job-1"
    assert "aws" in matches.iloc[0]["missing_skills"]
    assert len(matches) == 2