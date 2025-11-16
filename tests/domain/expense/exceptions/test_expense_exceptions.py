import pytest
from src.domain.expense.exceptions.expense_exceptions import (
    ExpenseStatusException,
    ExpenseInvalidOperation,
    ExpenseNotImplementedOperation,
)


def test_expense_status_exception_initialization() -> None:
    """Test that ExpenseStatusException can be initialized."""
    exception = ExpenseStatusException('Invalid status transition')
    assert exception.message == 'Invalid status transition'
    assert exception.code == 'EXPENSE_STATUS_EXCEPTION'


def test_expense_status_exception_str_representation() -> None:
    """Test that exception string representation includes code and message."""
    exception = ExpenseStatusException('Cannot transition from PAID to PENDING')
    assert str(exception) == 'EXPENSE_STATUS_EXCEPTION: Cannot transition from PAID to PENDING'


def test_expense_invalid_operation_initialization() -> None:
    """Test that ExpenseInvalidOperation can be initialized."""
    exception = ExpenseInvalidOperation('Invalid operation')
    assert exception.message == 'Invalid operation'
    assert exception.code == 'EXPENSE_INVALID_OPERATION'


def test_expense_invalid_operation_str_representation() -> None:
    """Test that exception string representation includes code and message."""
    exception = ExpenseInvalidOperation('Cannot add payment to finalized expense')
    assert str(exception) == 'EXPENSE_INVALID_OPERATION: Cannot add payment to finalized expense'


def test_expense_not_implemented_operation_initialization() -> None:
    """Test that ExpenseNotImplementedOperation can be initialized."""
    exception = ExpenseNotImplementedOperation()
    assert exception.message == 'This operation is not implemented for this expense type.'
    assert exception.code == 'EXPENSE_NOT_IMPLEMENTED_OPERATION'


def test_expense_not_implemented_operation_custom_message() -> None:
    """Test that ExpenseNotImplementedOperation accepts custom message."""
    exception = ExpenseNotImplementedOperation('Method not available for Purchase')
    assert exception.message == 'Method not available for Purchase'
    assert exception.code == 'EXPENSE_NOT_IMPLEMENTED_OPERATION'


def test_expense_not_implemented_operation_str_representation() -> None:
    """Test that exception string representation includes code and message."""
    exception = ExpenseNotImplementedOperation()
    expected = 'EXPENSE_NOT_IMPLEMENTED_OPERATION: This operation is not implemented for this expense type.'
    assert str(exception) == expected


def test_all_exceptions_can_be_raised() -> None:
    """Test that all expense exceptions can be raised."""
    with pytest.raises(ExpenseStatusException):
        raise ExpenseStatusException('Test')
    
    with pytest.raises(ExpenseInvalidOperation):
        raise ExpenseInvalidOperation('Test')
    
    with pytest.raises(ExpenseNotImplementedOperation):
        raise ExpenseNotImplementedOperation('Test')
