from uuid import uuid4
from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.use_cases.expense import PaymentCreateUseCase
from src.application.dtos import CreatePaymentDTO
from src.domain.expense import Subscription, Purchase, Payment, PaymentStatus, PaymentFactory
from src.domain.shared import Amount


@pytest.fixture
def payment_repository():
    return MagicMock()


@pytest.fixture
def expense_repository():
    return MagicMock()


@pytest.fixture
def subscription():
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly subscription',
        acquired_at=date(2025, 1, 1),
        amount=Amount(15),
        first_payment_date=date(2025, 1, 15),
        category_id=uuid4(),
        payments=[],
    )
    return subscription


@pytest.fixture
def purchase():
    purchase = Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='iPhone',
        cc_name='Phone purchase',
        acquired_at=date(2025, 1, 1),
        amount=Amount(1000),
        installments=3,
        first_payment_date=date(2025, 1, 15),
        category_id=uuid4(),
        payments=[],
    )
    return purchase


def test_payment_create_use_case_raises_when_expense_repository_not_provided(payment_repository):
    use_case = PaymentCreateUseCase(payment_repository, expense_repository=None)
    payment_data = CreatePaymentDTO(
        expense_id=uuid4(),
        amount=20.0,
        payment_date=date(2025, 2, 15),
    )
    
    with pytest.raises(ValueError, match='ExpenseRepository is required'):
        use_case.execute(payment_data)


def test_payment_create_use_case_raises_when_expense_not_found(payment_repository, expense_repository):
    expense_repository.get_by_filter.return_value = None
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=uuid4(),
        amount=20.0,
        payment_date=date(2025, 2, 15),
    )
    
    with pytest.raises(ValueError, match='Expense with ID .* not found'):
        use_case.execute(payment_data)


def test_payment_create_use_case_creates_payment_for_subscription(payment_repository, expense_repository, subscription):
    # Setup
    expense_repository.get_by_filter.return_value = subscription
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=subscription.id,
        amount=20.0,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    result = use_case.execute(payment_data)
    
    # Verify
    assert result is not None
    assert result.expense_id == subscription.id
    assert result.amount == 20.0
    
    # Verify subscription.add_new_payment was called (payment added to list)
    assert len(subscription.payments) == 2  # Original + new one
    
    # Verify expense_repository.update was called
    expense_repository.update.assert_called_once_with(subscription)
    
    # Verify payment_repository.create was NOT called (we use expense_repository.update instead)
    payment_repository.create.assert_not_called()


def test_payment_create_use_case_updates_subscription_installments(payment_repository, expense_repository, subscription):
    # Setup
    initial_installments = subscription.installments
    expense_repository.get_by_filter.return_value = subscription
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=subscription.id,
        amount=25.0,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    use_case.execute(payment_data)
    
    # Verify installments was updated
    assert subscription.installments == initial_installments + 1


def test_payment_create_use_case_orders_subscription_payments_by_date(payment_repository, expense_repository, subscription):
    # Setup - subscription already has one payment at 2025-01-15
    expense_repository.get_by_filter.return_value = subscription
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    # Add payment with earlier date
    payment_data = CreatePaymentDTO(
        expense_id=subscription.id,
        amount=25.0,
        payment_date=date(2025, 1, 10),  # Earlier than existing payment
    )
    
    # Execute
    use_case.execute(payment_data)
    
    # Verify payments are ordered by date
    assert len(subscription.payments) == 2
    assert subscription.payments[0].payment_date == date(2025, 1, 10)
    assert subscription.payments[1].payment_date >= date(2025, 1, 15)
    
    # Verify no_installment reflects the order
    assert subscription.payments[0].no_installment == 1
    assert subscription.payments[1].no_installment == 2


def test_payment_create_use_case_updates_subscription_amount_when_last_payment(payment_repository, expense_repository, subscription):
    # Setup
    expense_repository.get_by_filter.return_value = subscription
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    # Add payment with later date (will be the last)
    payment_data = CreatePaymentDTO(
        expense_id=subscription.id,
        amount=30.0,
        payment_date=date(2025, 3, 15),  # Later than existing payment
    )
    
    # Execute
    use_case.execute(payment_data)
    
    # Verify subscription amount was updated to match last payment
    assert subscription.amount.value == 30.0


def test_payment_create_use_case_creates_payment_for_purchase(payment_repository, expense_repository, purchase):
    # Setup
    expense_repository.get_by_filter.return_value = purchase
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=purchase.id,
        amount=50.0,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    result = use_case.execute(payment_data)
    
    # Verify
    assert result is not None
    assert result.expense_id == purchase.id
    assert result.amount == 50.0
    
    # Verify payment_repository.create was called (direct creation for non-subscription)
    payment_repository.create.assert_called_once()
    created_payment = payment_repository.create.call_args[0][0]
    assert isinstance(created_payment, Payment)
    assert created_payment.amount.value == 50.0
    
    # Verify expense_repository.update was NOT called
    expense_repository.update.assert_not_called()


def test_payment_create_use_case_returns_correct_dto_structure(payment_repository, expense_repository, subscription):
    # Setup
    expense_repository.get_by_filter.return_value = subscription
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=subscription.id,
        amount=20.0,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    result = use_case.execute(payment_data)
    
    # Verify DTO structure
    assert hasattr(result, 'id')
    assert hasattr(result, 'expense_id')
    assert hasattr(result, 'amount')
    assert hasattr(result, 'no_installment')
    assert hasattr(result, 'status')
    assert hasattr(result, 'payment_date')
    assert result.expense_id == subscription.id
    assert result.amount == 20.0
    assert result.payment_date == date(2025, 2, 15)


def test_payment_create_use_case_creates_payment_with_unconfirmed_status(payment_repository, expense_repository, purchase):
    # Setup
    expense_repository.get_by_filter.return_value = purchase
    use_case = PaymentCreateUseCase(payment_repository, expense_repository)
    
    payment_data = CreatePaymentDTO(
        expense_id=purchase.id,
        amount=100.0,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    result = use_case.execute(payment_data)
    
    # Verify status is UNCONFIRMED
    assert result.status == PaymentStatus.UNCONFIRMED
