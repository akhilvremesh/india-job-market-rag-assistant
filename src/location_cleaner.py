import re


# Standardize only clear city-name variants
LOCATION_ALIASES = {
    "bangalore": "Bengaluru",
    "gurugram": "Gurgaon",
    "delhi ncr": "Delhi NCR",
}


def normalize_location(value):
    """Clean a location while preserving multiple locations in the value."""
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    # Split values such as "Delhi NCR,Gurgaon,Noida" at commas
    parts = re.split(r"\s*,\s*", text)

    cleaned_parts = []

    for part in parts:
        part = re.sub(r"\s+", " ", part).strip()

        if not part:
            continue

        # Standardize known aliases; title-case other location names
        location = LOCATION_ALIASES.get(part.casefold(), part.title())

        # Keep the first occurrence, so "Mumbai,Mumbai" becomes "Mumbai"
        if location not in cleaned_parts:
            cleaned_parts.append(location)

    return ", ".join(cleaned_parts) if cleaned_parts else None