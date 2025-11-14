import pytest
from src.domain.expense.exceptions.payment_exceptions import PaymentNotFoundInExpenseException


def test_payment_not_found_exception_initialization() -> None:
    """Test that PaymentNotFoundInExpenseException can be initialized."""
    exception = PaymentNotFoundInExpenseException('Payment not found')
    assert exception.message == 'Payment not found'
    assert exception.code == 'PAYMENT_NOT_FOUND_IN_EXPENSE_EXCEPTION'


def test_payment_not_found_exception_str_representation() -> None:
    """Test that exception string representation includes code and message."""
    exception = PaymentNotFoundInExpenseException('Payment with ID 123 not found')
    assert str(exception) == 'PAYMENT_NOT_FOUND_IN_EXPENSE_EXCEPTION: Payment with ID 123 not found'


def test_payment_not_found_exception_can_be_raised() -> None:
    """Test that exception can be raised properly."""
    with pytest.raises(PaymentNotFoundInExpenseException) as exc_info:
        raise PaymentNotFoundInExpenseException('Payment does not exist')
    
    assert exc_info.value.message == 'Payment does not exist'
