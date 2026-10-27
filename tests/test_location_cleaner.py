from src.location_cleaner import normalize_location


def test_trims_and_capitalizes_location():
    assert normalize_location("  mumbai  ") == "Mumbai"


def test_standardizes_city_alias():
    assert normalize_location("Bangalore") == "Bengaluru"


def test_preserves_multiple_locations():
    assert normalize_location("Delhi NCR,Gurgaon,Noida") == (
        "Delhi NCR, Gurgaon, Noida"
    )


def test_removes_repeated_location():
    assert normalize_location("Mumbai,Mumbai") == "Mumbai"


def test_empty_location_returns_none():
    assert normalize_location("  ") is None