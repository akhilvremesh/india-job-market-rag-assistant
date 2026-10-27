from src.experience_parser import parse_experience_years


def test_parses_experience_range():
    assert parse_experience_years("2 - 5 yrs") == (2.0, 5.0, 3.5)


def test_parses_single_experience_value():
    assert parse_experience_years("5 years") == (5.0, 5.0, 5.0)


def test_reversed_range_is_returned_in_order():
    assert parse_experience_years("5 - 2 yrs") == (2.0, 5.0, 3.5)


def test_missing_or_unparseable_experience_returns_none():
    assert parse_experience_years("Not Mentioned") is None
    assert parse_experience_years(None) is None