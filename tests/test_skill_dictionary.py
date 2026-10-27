from src.skill_dictionary import extract_skills


def test_standardizes_known_aliases():
    assert extract_skills("JS | Python 3 | SQL") == [
        "javascript",
        "python",
        "sql",
    ]


def test_removes_duplicate_skills_from_one_posting():
    assert extract_skills("Python | python | PY") == ["python"]


def test_keeps_unknown_skill_in_lowercase():
    assert extract_skills("Power BI") == ["power bi"]


def test_missing_skills_return_empty_list():
    assert extract_skills(None) == []