import pytest
from uuid import uuid4
from datetime import date

from src.domain.expense import Expense, ExpenseCategory, Purchase
from src.domain.expense.enums import ExpenseType, ExpenseStatus, PaymentStatus
from src.domain.expense.exceptions import ExpenseNotImplementedOperation
from src.domain.shared import Amount
from src.domain.shared.value_objects.month import Month
from src.domain.shared.value_objects.year import Year


@pytest.fixture
def sample_category() -> ExpenseCategory:
    return ExpenseCategory(
        id=uuid4(),
        owner_id=uuid4(),
        name='Test Category',
        description='Test Description',
        is_income=False,
    )


@pytest.fixture
def base_expense(sample_category: ExpenseCategory) -> Expense:
    """Create a Purchase instance to test base Expense functionality."""
    return Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='Test Expense',
        cc_name='Test Card',
        acquired_at=date(2025, 1, 1),
        amount=Amount(100.0),
        installments=3,
        first_payment_date=date(2025, 2, 1),
        category_id=sample_category.id,
        payments=[],
    )


def test_expense_paid_amount_not_implemented(base_expense: Expense) -> None:
    """Test that paid_amount is implemented for Purchase."""
    # This test just ensures the property can be accessed
    result = base_expense.paid_amount
    assert isinstance(result, Amount)


def test_expense_pending_installments_not_implemented(base_expense: Expense) -> None:
    """Test that pending_installments is implemented for Purchase."""
    result = base_expense.pending_installments
    assert isinstance(result, int)


def test_expense_done_installments_not_implemented(base_expense: Expense) -> None:
    """Test that done_installments is implemented for Purchase."""
    result = base_expense.done_installments
    assert isinstance(result, int)


def test_expense_pending_financing_amount_not_implemented(base_expense: Expense) -> None:
    """Test that pending_financing_amount is implemented for Purchase."""
    result = base_expense.pending_financing_amount
    assert isinstance(result, Amount)


def test_expense_pending_amount_not_implemented(base_expense: Expense) -> None:
    """Test that pending_amount is implemented for Purchase."""
    result = base_expense.pending_amount
    assert isinstance(result, Amount)


def test_expense_calculate_payments_not_implemented(base_expense: Expense) -> None:
    """Test that calculate_payments is implemented for Purchase."""
    # Should not raise exception
    base_expense.calculate_payments()
    assert len(base_expense.payments) > 0


def test_expense_get_payments_invalid_parameters(base_expense: Expense) -> None:
    """Test that get_payments raises ValueError when only month or year is provided."""
    with pytest.raises(ValueError, match='Both month and year must be provided together'):
        base_expense.get_payments(month=Month(1), year=None)
    
    with pytest.raises(ValueError, match='Both month and year must be provided together'):
        base_expense.get_payments(month=None, year=Year(2025))


def test_expense_get_payments_no_filter(base_expense: Expense) -> None:
    """Test get_payments without filtering returns all payments."""
    base_expense.calculate_payments()
    all_payments = base_expense.get_payments()
    assert len(all_payments) == len(base_expense.payments)


def test_expense_get_payments_with_month_year_filter(base_expense: Expense) -> None:
    """Test get_payments with month and year filter."""
    base_expense.calculate_payments()
    # Filter by the first payment date (February 2025)
    filtered = base_expense.get_payments(month=Month(2), year=Year(2025))
    assert len(filtered) >= 1
    for payment in filtered:
        assert payment.payment_date.month == Month(2)
        assert payment.payment_date.year == Year(2025)


def test_expense_abstract_methods_raise_not_implemented():
    """Test that abstract methods raise ExpenseNotImplementedOperation when called from base Expense."""
    # Create a minimal concrete subclass that doesn't override abstract methods
    class MinimalExpense(Expense):
        def __init__(self):
            super().__init__(
                id=uuid4(),
                account_id=uuid4(),
                title='Test',
                cc_name='Card',
                acquired_at=date(2025, 1, 1),
                amount=Amount(100),
                installments=1,
                first_payment_date=date(2025, 2, 1),
                status=ExpenseStatus.ACTIVE,
                expense_type=ExpenseType.PURCHASE,
                category_id=uuid4(),
                payments=[],
            )
        
        def to_dict(self, include_relations: bool = False) -> dict:
            return {}
    
    expense = MinimalExpense()
    
    # Test all abstract methods raise ExpenseNotImplementedOperation
    with pytest.raises(ExpenseNotImplementedOperation, match='paid_amount.*not implemented'):
        _ = expense.paid_amount
    
    with pytest.raises(ExpenseNotImplementedOperation, match='pending_installments.*not implemented'):
        _ = expense.pending_installments
    
    with pytest.raises(ExpenseNotImplementedOperation, match='done_installments.*not implemented'):
        _ = expense.done_installments
    
    with pytest.raises(ExpenseNotImplementedOperation, match='pending_financing_amount.*not implemented'):
        _ = expense.pending_financing_amount
    
    with pytest.raises(ExpenseNotImplementedOperation, match='pending_amount.*not implemented'):
        _ = expense.pending_amount
    
    with pytest.raises(ExpenseNotImplementedOperation, match='calculate_payments.*not implemented'):
        expense.calculate_payments()
