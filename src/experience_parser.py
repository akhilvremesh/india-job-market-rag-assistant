import re


def parse_experience_years(value):
    """Return (minimum, maximum, midpoint) years, or None if not parseable."""
    if value is None:
        return None

    text = str(value).strip().casefold()

    # Extract up to two numbers from ranges such as "2 - 5 yrs"
    numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if not numbers:
        return None

    years = [float(number) for number in numbers[:2]]

    # Treat a single number such as "5 years" as a 5-to-5 range
    minimum = min(years)
    maximum = max(years)
    midpoint = (minimum + maximum) / 2

    return minimum, maximum, midpoint