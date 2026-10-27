import re


def parse_salary_lpa(value):
    """Return (minimum, maximum, midpoint) salary in LPA, or None."""
    if value is None:
        return None

    text = str(value).strip().lower()

    if not text:
        return None

    # Remove commas so "3,00,000" becomes "300000"
    text = text.replace(",", "")

    # Find salary numbers, including decimals such as "6.5"
    numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if not numbers:
        return None

    amounts = [float(number) for number in numbers[:2]]

    # Convert monthly rupees to annual LPA
    is_monthly = "per month" in text or "p.m" in text or "pm" in text

    # LPA/lakh amounts are already in lakhs
    is_lpa = any(word in text for word in ["lpa", "lakh", "lac"])

    if is_monthly:
        amounts = [amount * 12 / 100_000 for amount in amounts]
    elif not is_lpa:
        # Other numeric salary amounts are treated as annual rupees
        amounts = [amount / 100_000 for amount in amounts]

    minimum = min(amounts)
    maximum = max(amounts)
    midpoint = (minimum + maximum) / 2

    return minimum, maximum, midpoint
    