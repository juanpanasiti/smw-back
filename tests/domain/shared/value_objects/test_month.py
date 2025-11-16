import pytest
from src.domain.shared.value_objects.month import Month


def test_month_valid_values() -> None:
    """Test that valid month values work correctly."""
    for i in range(1, 13):
        month = Month(i)
        assert month == i


def test_month_invalid_value_too_low() -> None:
    """Test that month below 1 raises ValueError."""
    with pytest.raises(ValueError, match='Month must be between 1 and 12'):
        Month(0)


def test_month_invalid_value_too_high() -> None:
    """Test that month above 12 raises ValueError."""
    with pytest.raises(ValueError, match='Month must be between 1 and 12'):
        Month(13)


def test_month_none_value() -> None:
    """Test that None value raises ValueError."""
    with pytest.raises(ValueError, match='Month must be between 1 and 12'):
        Month(None)


def test_month_str_representation() -> None:
    """Test that month string representation is zero-padded."""
    assert str(Month(1)) == '01'
    assert str(Month(9)) == '09'
    assert str(Month(10)) == '10'
    assert str(Month(12)) == '12'
