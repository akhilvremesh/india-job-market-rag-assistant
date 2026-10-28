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

def test_location_and_phone_text_is_not_treated_as_salary():
    value = "Chennai, Salem, Vellore. Whatsapp 9876543210"
    assert parse_salary_lpa(value) is None


def test_ambiguous_pay_band_is_not_treated_as_annual_salary():
    value = "INR Pay Band 3 (Rs.15600-39100) with AGP"
    assert parse_salary_lpa(value) is None


def test_converts_explicit_monthly_salary_to_annual_lpa():
    assert parse_salary_lpa("INR 50,000 - 1,00,000 P.M.") == (
        6.0,
        12.0,
        9.0,
    )

def test_parses_crore_salary():
    assert parse_salary_lpa("INR 1 Cr & above PA.") == (
        100.0,
        100.0,
        100.0,
    )


def test_parses_monthly_salary_in_thousands():
    assert parse_salary_lpa("12k to 15k CTC per month") == (
        1.44,
        1.8,
        1.62,
    )


def test_parses_lakh_abbreviation():
    assert parse_salary_lpa("Salary up to 2.5 Lcs PA") == (
        2.5,
        2.5,
        2.5,
    )

def test_ignores_annual_leave_days():
    text = "annual Paid Leaves for 30-45 days; tax Free Salary"
    assert parse_salary_lpa(text) is None


def test_ignores_half_yearly_increment_text():
    text = "5 day's working, half yearly increments, Friendly Culture"
    assert parse_salary_lpa(text) is None