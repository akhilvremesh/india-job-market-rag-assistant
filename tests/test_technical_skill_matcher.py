import pandas as pd

from src.build_technical_skills_table import build_technical_skill_rows
from src.technical_skill_matcher import extract_technical_skills


def test_finds_technical_skills():
    assert extract_technical_skills("SQL | Python 3 | pandas") == [
        "sql",
        "python",
        "pandas",
    ]


def test_standardizes_aliases_and_removes_duplicates():
    assert extract_technical_skills("JS | JavaScript") == ["javascript"]


def test_ignores_terms_outside_the_technical_dictionary():
    assert extract_technical_skills("Sales | Recruitment | Python") == [
        "python"
    ]


def test_missing_input_returns_empty_list():
    assert extract_technical_skills(None) == []


def test_builds_one_row_per_posting_and_technical_skill():
    jobs = pd.DataFrame(
        [
            {
                "Uniq Id": "job-1",
                "Key Skills": "JS | JavaScript | Python 3 | Sales",
            },
            {
                "Uniq Id": "job-2",
                "Key Skills": "SQL | pandas",
            },
        ]
    )

    result = build_technical_skill_rows(jobs)

    actual = set(zip(result["job_id"], result["skill"]))

    assert actual == {
        ("job-1", "javascript"),
        ("job-1", "python"),
        ("job-2", "sql"),
        ("job-2", "pandas"),
    }

def test_matches_skills_next_to_pipe_separators():
    assert extract_technical_skills("SQL|Python|JavaScript|HTML") == [
        "sql",
        "python",
        "javascript",
        "html",
    ]
def test_does_not_match_java_inside_javascript():
    assert extract_technical_skills("JavaScript") == ["javascript"]


def test_does_not_join_separate_entries_into_one_phrase():
    assert extract_technical_skills("data|analysis") == []

def test_js_in_framework_names_is_not_javascript():
    assert extract_technical_skills("React.Js | Node.js") == [
        "react",
        "node.js",
    ]