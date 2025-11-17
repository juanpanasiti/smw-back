import pytest
from uuid import uuid4
from datetime import date

from src.domain.expense import Period, PeriodPayment
from src.domain.expense.enums import PaymentStatus, ExpenseStatus
from src.domain.account.enums import AccountType
from src.domain.shared import Amount, Month, Year


@pytest.fixture
def sample_period_payments() -> list[PeriodPayment]:
    """Create sample period payments for testing."""
    expense_id_1 = uuid4()
    expense_id_2 = uuid4()
    expense_id_3 = uuid4()
    account_id = uuid4()
    
    return [
        PeriodPayment(
            # Payment data
            payment_id=uuid4(),
            amount=Amount(100.0),
            status=PaymentStatus.PAID,
            payment_date=date(2025, 11, 15),
            no_installment=1,
            is_last_payment=False,
            # Expense data
            expense_id=expense_id_1,
            expense_title="Test Expense 1",
            expense_cc_name="TEST1",
            expense_acquired_at=date(2025, 11, 1),
            expense_installments=1,
            expense_status=ExpenseStatus.ACTIVE,
            expense_category_name="Category 1",
            # Account data
            account_id=account_id,
            account_alias="Test Card",
            account_is_enabled=True,
            account_type=AccountType.CREDIT_CARD,
        ),
        PeriodPayment(
            # Payment data
            payment_id=uuid4(),
            amount=Amount(200.0),
            status=PaymentStatus.CONFIRMED,
            payment_date=date(2025, 12, 15),
            no_installment=2,
            is_last_payment=False,
            # Expense data
            expense_id=expense_id_2,
            expense_title="Test Expense 2",
            expense_cc_name="TEST2",
            expense_acquired_at=date(2025, 12, 1),
            expense_installments=3,
            expense_status=ExpenseStatus.ACTIVE,
            expense_category_name="Category 2",
            # Account data
            account_id=account_id,
            account_alias="Test Card",
            account_is_enabled=True,
            account_type=AccountType.CREDIT_CARD,
        ),
        PeriodPayment(
            # Payment data
            payment_id=uuid4(),
            amount=Amount(150.0),
            status=PaymentStatus.CANCELED,
            payment_date=date(2026, 1, 15),
            no_installment=3,
            is_last_payment=True,
            # Expense data
            expense_id=expense_id_3,
            expense_title="Test Expense 3",
            expense_cc_name="TEST3",
            expense_acquired_at=date(2026, 1, 1),
            expense_installments=3,
            expense_status=ExpenseStatus.CANCELLED,
            expense_category_name=None,
            # Account data
            account_id=account_id,
            account_alias="Test Card",
            account_is_enabled=True,
            account_type=AccountType.CREDIT_CARD,
        ),
    ]


@pytest.fixture
def period(sample_period_payments: list[PeriodPayment]) -> Period:
    """Create a period for testing."""
    return Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=[sample_period_payments[0]],  # Only November payment
    )


def test_period_period_str(period: Period) -> None:
    """Test period_str property returns correct format."""
    assert period.period_str == '11/2025'


def test_period_total_amount(sample_period_payments: list[PeriodPayment]) -> None:
    """Test total_amount calculates sum of all payments."""
    period = Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=sample_period_payments,
    )
    assert period.total_amount.value == 450.0  # 100 + 200 + 150


def test_period_total_paid_amount(sample_period_payments: list[PeriodPayment]) -> None:
    """Test total_paid_amount calculates sum of paid payments."""
    period = Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=sample_period_payments,
    )
    assert period.total_paid_amount.value == 100.0  # Only first payment is paid


def test_period_total_pending_amount(sample_period_payments: list[PeriodPayment]) -> None:
    """Test total_pending_amount calculates sum of pending payments."""
    # Create new payment with UNCONFIRMED status which counts as pending
    pending_payment = PeriodPayment(
        # Payment data
        payment_id=uuid4(),
        amount=Amount(200.0),
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 12, 15),
        no_installment=2,
        is_last_payment=False,
        # Expense data
        expense_id=uuid4(),
        expense_title="Pending Expense",
        expense_cc_name="PEND",
        expense_acquired_at=date(2025, 12, 1),
        expense_installments=1,
        expense_status=ExpenseStatus.ACTIVE,
        expense_category_name=None,
        # Account data
        account_id=uuid4(),
        account_alias="Test Card",
        account_is_enabled=True,
        account_type=AccountType.CREDIT_CARD,
    )
    period = Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=[sample_period_payments[0], pending_payment],
    )
    # total_pending_amount checks for status == UNCONFIRMED
    assert period.total_pending_amount.value == 200.0


def test_period_pending_payments(sample_period_payments: list[PeriodPayment]) -> None:
    """Test pending_payments returns non-final status payments."""
    period = Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=sample_period_payments,
    )
    pending = period.pending_payments
    # PAID and CANCELED are final, so only CONFIRMED is not final
    assert len(pending) == 1


def test_period_completed_payments(sample_period_payments: list[PeriodPayment]) -> None:
    """Test completed_payments returns final status payments."""
    period = Period(
        id=uuid4(),
        month=Month(11),
        year=Year(2025),
        payments=sample_period_payments,
    )
    completed = period.completed_payments
    # PAID and CANCELED are final
    assert len(completed) == 2


def test_period_total_payments(period: Period) -> None:
    """Test total_payments returns count of payments."""
    assert period.total_payments == 1


def test_period_to_dict_without_relationships(period: Period) -> None:
    """Test to_dict without relationships returns payment IDs."""
    result = period.to_dict(include_relationships=False)
    assert 'id' in result
    assert 'month' in result
    assert 'year' in result
    assert 'payments' in result
    assert isinstance(result['payments'][0], str)  # Payment ID as string


def test_period_to_dict_with_relationships(period: Period) -> None:
    """Test to_dict with relationships returns payment dicts."""
    result = period.to_dict(include_relationships=True)
    assert 'payments' in result
    assert isinstance(result['payments'][0], dict)  # Payment as dict


def test_period_add_payment_success(period: Period) -> None:
    """Test adding a new payment to period."""
    new_payment = PeriodPayment(
        # Payment data
        payment_id=uuid4(),
        amount=Amount(50.0),
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 11, 20),
        no_installment=4,
        is_last_payment=False,
        # Expense data
        expense_id=uuid4(),
        expense_title="New Expense",
        expense_cc_name="NEW",
        expense_acquired_at=date(2025, 11, 1),
        expense_installments=1,
        expense_status=ExpenseStatus.ACTIVE,
        expense_category_name=None,
        # Account data
        account_id=uuid4(),
        account_alias="Test Card",
        account_is_enabled=True,
        account_type=AccountType.CREDIT_CARD,
    )
    initial_count = period.total_payments
    period.add_payment(new_payment)
    assert period.total_payments == initial_count + 1


def test_period_add_payment_duplicate(period: Period) -> None:
    """Test adding duplicate payment doesn't add twice."""
    existing_payment = period.payments[0]
    initial_count = period.total_payments
    period.add_payment(existing_payment)
    assert period.total_payments == initial_count  # No change


def test_period_add_payment_invalid_type(period: Period) -> None:
    """Test adding non-PeriodPayment object raises ValueError."""
    with pytest.raises(ValueError, match='payment must be an instance of PeriodPayment'):
        period.add_payment('not-a-payment')  # type: ignore


def test_period_fill_from_account(period: Period, sample_period_payments: list[PeriodPayment]) -> None:
    """Test fill_from_account adds payments from account."""
    from unittest.mock import MagicMock
    
    mock_account = MagicMock()
    # Mock get_payments to return payments for November 2025
    mock_account.get_payments.return_value = [sample_period_payments[0]]
    
    initial_count = period.total_payments
    period.fill_from_account(mock_account)
    
    # Verify get_payments was called with correct month and year
    mock_account.get_payments.assert_called_once_with(Month(11), Year(2025))


def test_period_fill_from_account_with_invalid_payment(period: Period) -> None:
    """Test fill_from_account handles ValueError exceptions gracefully."""
    from unittest.mock import MagicMock, PropertyMock
    
    # Create a mock payment that will raise ValueError when added
    mock_invalid_payment = MagicMock()
    type(mock_invalid_payment).id = PropertyMock(side_effect=ValueError("Invalid payment"))
    
    mock_account = MagicMock()
    mock_account.get_payments.return_value = [mock_invalid_payment]
    
    initial_count = period.total_payments
    # Should not raise exception, just continue
    period.fill_from_account(mock_account)
    assert period.total_payments == initial_count  # No change due to exception
