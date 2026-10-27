import re


def parse_salary_lpa(value):
    """Return (minimum, maximum, midpoint) salary in LPA, or None."""
    if value is None:
        return None

    text = str(value).strip().casefold()

    if not text:
        return None

    # Detect explicit salary units or periods
    is_lpa = bool(re.search(r"\b(?:lpa|lac|lakh|lakhs)\b", text))

    is_monthly = (
        "per month" in text
        or "monthly" in text
        or "p.m" in text
        or bool(re.search(r"\bpm\b", text))
    )

    is_annual = (
        "per annum" in text
        or "per year" in text
        or "annual" in text
        or "yearly" in text
        or "p.a" in text
        or bool(re.search(r"\bpa\b", text))
    )

    # Bare numbers or currency alone are too ambiguous to interpret safely
    if not (is_lpa or is_monthly or is_annual):
        return None

    text = text.replace(",", "")
    numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if not numbers:
        return None

    amounts = [float(number) for number in numbers[:2]]

    if is_monthly:
        amounts = [amount * 12 / 100_000 for amount in amounts]
    elif not is_lpa:
        amounts = [amount / 100_000 for amount in amounts]

    minimum = min(amounts)
    maximum = max(amounts)
    midpoint = (minimum + maximum) / 2

    return minimum, maximum, midpoint