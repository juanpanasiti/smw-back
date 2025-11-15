import pytest
from src.domain.shared.value_objects.year import Year


def test_year_valid_values() -> None:
    """Test that valid year values work correctly."""
    assert Year(2000) == 2000
    assert Year(2024) == 2024
    assert Year(2025) == 2025
    assert Year(3000) == 3000


def test_year_invalid_value_below_2000() -> None:
    """Test that year below 2000 raises ValueError."""
    with pytest.raises(ValueError, match='Year must be a positive integer greater than 2000'):
        Year(1999)


def test_year_invalid_value_none() -> None:
    """Test that None value raises ValueError."""
    with pytest.raises(ValueError, match='Year must be a positive integer greater than 2000'):
        Year(None)


def test_year_str_representation() -> None:
    """Test that year string representation works correctly."""
    assert str(Year(2025)) == '2025'
    assert str(Year(2000)) == '2000'
