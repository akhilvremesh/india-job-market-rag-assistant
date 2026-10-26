def parse_key_skills(value):
    """Split one pipe-separated skills cell into cleaned skill names."""

    # Missing values, such as None or pandas NaN, produce an empty list.
    if not isinstance(value, str):
        return []

    # Split on |, remove surrounding spaces, lowercase, and skip empty entries.
    skills = [
        skill.strip().lower()
        for skill in value.split("|")
        if skill.strip()
    ]

    return skills