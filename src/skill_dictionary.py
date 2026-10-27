# Map known skill spellings and abbreviations to one standard name
SKILL_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",
    "py": "python",
    "python 3": "python",
    "python": "python",
    "sql": "sql",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
}


def extract_skills(value):
    """Return standardized skills from a pipe-separated Key Skills value."""
    if value is None:
        return []

    found_skills = []

    # The source field separates skills using the | character
    for item in str(value).split("|"):
        skill = " ".join(item.casefold().split())

        if not skill:
            continue

        # Use a standard name for known variants; keep other values as-is
        canonical_skill = SKILL_ALIASES.get(skill, skill)

        # Keep each skill only once per posting, in its original order
        if canonical_skill not in found_skills:
            found_skills.append(canonical_skill)

    return found_skills