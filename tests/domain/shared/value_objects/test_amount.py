import pytest

from src.domain.shared.value_objects.amount import Amount


def test_amount_init_with_float():
    """Test Amount initialization with float value."""
    amount = Amount(10.5)
    assert amount.value == 10.5
    assert amount.precision == 2


def test_amount_init_with_int():
    """Test Amount initialization with int value."""
    amount = Amount(10)
    assert amount.value == 10.0
    assert amount.precision == 2


def test_amount_init_with_custom_precision():
    """Test Amount initialization with custom precision."""
    amount = Amount(10.12345, precision=3)
    assert amount.value == 10.123
    assert amount.precision == 3


def test_amount_init_negative_precision():
    """Test Amount initialization fails with negative precision."""
    with pytest.raises(ValueError, match='Precision must be a non-negative integer'):
        Amount(10, precision=-1)


def test_amount_str():
    """Test Amount string representation."""
    amount = Amount(10.5)
    assert str(amount) == '10.50'


def test_amount_add_valid():
    """Test Amount addition with another Amount."""
    a1 = Amount(10.5)
    a2 = Amount(5.25)
    result = a1 + a2
    assert result.value == 15.75
    assert result.precision == 2


def test_amount_add_invalid_type():
    """Test Amount addition fails with non-Amount type."""
    amount = Amount(10)
    with pytest.raises(TypeError, match='Can only add Decimal to Decimal'):
        _ = amount + 5


def test_amount_sub_valid():
    """Test Amount subtraction with another Amount."""
    a1 = Amount(10.5)
    a2 = Amount(5.25)
    result = a1 - a2
    assert result.value == 5.25
    assert result.precision == 2


def test_amount_sub_invalid_type():
    """Test Amount subtraction fails with non-Amount type."""
    amount = Amount(10)
    with pytest.raises(TypeError, match='Can only subtract Decimal from Decimal'):
        _ = amount - 5


def test_amount_eq_with_amount():
    """Test Amount equality with another Amount."""
    a1 = Amount(10.5)
    a2 = Amount(10.5)
    assert a1 == a2


def test_amount_eq_with_float():
    """Test Amount equality with float."""
    amount = Amount(10.5)
    assert amount == 10.5


def test_amount_eq_with_int():
    """Test Amount equality with int."""
    amount = Amount(10)
    assert amount == 10


def test_amount_repr():
    """Test Amount repr representation."""
    amount = Amount(10.5, precision=2)
    assert repr(amount) == 'Amount(value=10.5, precision=2)'


def test_amount_eq_with_invalid_type():
    """Test Amount equality with invalid type returns NotImplemented."""
    amount = Amount(10)
    result = amount.__eq__('invalid')
    assert result is NotImplemented
