from src.salary_parser import parse_salary_lpa


def test_parses_lpa_range():
    assert parse_salary_lpa("6-10 LPA") == (6.0, 10.0, 8.0)


def test_parses_annual_rupees():
    assert parse_salary_lpa("INR 3,00,000 - 7,00,000 PA") == (
        3.0,
        7.0,
        5.0,
    )


def test_undisclosed_salary_returns_none():
    assert parse_salary_lpa("Not Disclosed by Recruiter") is None