import re


def parse_salary_lpa(value):
    """Return (minimum, maximum, midpoint) salary in LPA, or None."""
    if value is None:
        return None

    text = str(value).strip().casefold()

    if not text:
        return None

    # Recognize amounts stated directly in lakh or LPA.
    is_lpa = bool(
        re.search(r"\b(?:lpa|lac|lakh|lakhs|lcs|lacs)\b", text)
    )

    # Recognize monthly salary descriptions.
    is_monthly = (
        "per month" in text
        or "monthly" in text
        or "p.m" in text
        or bool(re.search(r"\bpm\b", text))
    )

    # Recognize annual salary descriptions.
    is_annual = (
    "per annum" in text
    or "per year" in text
    or "p.a" in text
    or bool(re.search(r"\bpa\b", text))
    )

    # Ignore amounts without a salary unit or pay period.
    if not (is_lpa or is_monthly or is_annual):
        return None

    # Capture each number and an optional suffix such as "Cr", "LPA", or "k".
    matches = re.findall(
        r"(\d[\d,]*(?:\.\d+)?)\s*"
        r"(crores?|cr|lakhs?|lacs?|lcs|lac|lpa|k)?\b",
        text,
    )

    if not matches:
        return None

    amounts_lpa = []

    for number_text, unit in matches[:2]:
        amount = float(number_text.replace(",", ""))

        if unit in {"cr", "crore", "crores"}:
            # One crore is 100 lakh, so it equals 100 LPA.
            amount_lpa = amount * 100

        elif unit in {"lpa", "lac", "lakh", "lakhs", "lacs", "lcs"}:
            # These suffixes already express the amount in lakh per year.
            amount_lpa = amount

        else:
            # "k" means thousand rupees; an unsuffixed number is treated
            # as rupees unless the full salary text says LPA.
            amount_rupees = amount * 1_000 if unit == "k" else amount

            if is_lpa:
                amount_lpa = amount_rupees
            elif is_monthly:
                amount_lpa = amount_rupees * 12 / 100_000
            else:
                amount_lpa = amount_rupees / 100_000

        amounts_lpa.append(amount_lpa)

    minimum = min(amounts_lpa)
    maximum = max(amounts_lpa)
    midpoint = (minimum + maximum) / 2

    return minimum, maximum, midpoint