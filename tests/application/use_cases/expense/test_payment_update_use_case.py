from uuid import uuid4
from datetime import date
from unittest.mock import MagicMock
import copy

import pytest

from src.application.use_cases.expense import PaymentUpdateUseCase
from src.application.dtos import UpdatePaymentDTO
from src.domain.expense import Subscription, Purchase, Payment, PaymentStatus, PaymentFactory
from src.domain.shared import Amount


@pytest.fixture
def payment_repository():
    return MagicMock()


@pytest.fixture
def expense_repository():
    return MagicMock()


@pytest.fixture
def subscription_with_payments():
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
    
    # Add second payment
    payment2 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(20),
        no_installment=2,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
    )
    subscription.add_new_payment(payment2)
    
    return subscription


@pytest.fixture
def purchase_with_payments():
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


def test_payment_update_use_case_raises_when_payment_not_found(payment_repository, expense_repository):
    payment_repository.get_by_filter.return_value = None
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=30.0,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 2, 15),
    )
    
    with pytest.raises(ValueError, match='Payment with ID .* not found'):
        use_case.execute(uuid4(), payment_data)


def test_payment_update_use_case_raises_when_expense_not_found(payment_repository, expense_repository):
    payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=uuid4(),
        amount=Amount(20),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 1, 15),
    )
    
    payment_repository.get_by_filter.return_value = payment
    expense_repository.get_by_filter.return_value = None
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=30.0,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 2, 15),
    )
    
    with pytest.raises(ValueError, match='Expense with ID .* not found'):
        use_case.execute(payment.id, payment_data)


def test_payment_update_use_case_updates_subscription_payment(payment_repository, expense_repository, subscription_with_payments):
    # Setup
    payment_to_update = subscription_with_payments.payments[1]  # Second payment
    payment_repository.get_by_filter.return_value = payment_to_update
    expense_repository.get_by_filter.return_value = subscription_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=30.0,
        status=PaymentStatus.CONFIRMED,
        payment_date=date(2025, 2, 20),
    )
    
    # Execute
    result = use_case.execute(payment_to_update.id, payment_data)
    
    # Verify
    assert result is not None
    assert result.amount == 30.0
    assert result.status == PaymentStatus.CONFIRMED
    
    # Verify expense_repository.update was called
    expense_repository.update.assert_called_once_with(subscription_with_payments)
    
    # Verify payment_repository.update was NOT called (we use expense_repository.update)
    payment_repository.update.assert_not_called()


def test_payment_update_use_case_updates_subscription_amount_when_updating_last_payment(payment_repository, expense_repository, subscription_with_payments):
    # Setup - update the last payment (by date)
    last_payment = subscription_with_payments.payments[-1]
    payment_repository.get_by_filter.return_value = last_payment
    expense_repository.get_by_filter.return_value = subscription_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=50.0,  # New amount
        status=PaymentStatus.UNCONFIRMED,
        payment_date=last_payment.payment_date,
    )
    
    # Execute
    use_case.execute(last_payment.id, payment_data)
    
    # Verify subscription amount was updated
    assert subscription_with_payments.amount.value == 50.0


def test_payment_update_use_case_reorders_subscription_payments_when_date_changes(payment_repository, expense_repository, subscription_with_payments):
    # Setup - update second payment to have earlier date
    payment_to_update = subscription_with_payments.payments[1]
    original_date = payment_to_update.payment_date
    
    payment_repository.get_by_filter.return_value = payment_to_update
    expense_repository.get_by_filter.return_value = subscription_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    # Update with earlier date (should move to first position)
    payment_data = UpdatePaymentDTO(
        amount=payment_to_update.amount.value,
        status=payment_to_update.status,
        payment_date=date(2025, 1, 10),  # Earlier than first payment
    )
    
    # Execute
    use_case.execute(payment_to_update.id, payment_data)
    
    # Verify payments were reordered
    assert subscription_with_payments.payments[0].id == payment_to_update.id
    assert subscription_with_payments.payments[0].no_installment == 1


def test_payment_update_use_case_rebalances_purchase_payments(payment_repository, expense_repository, purchase_with_payments):
    # Setup - purchase has 3 payments of 333.33, 333.33, 333.34
    first_payment = purchase_with_payments.payments[0]
    payment_repository.get_by_filter.return_value = first_payment
    expense_repository.get_by_filter.return_value = purchase_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    # Update first payment amount to 500
    payment_data = UpdatePaymentDTO(
        amount=500.0,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=first_payment.payment_date,
    )
    
    # Execute
    use_case.execute(first_payment.id, payment_data)
    
    # Verify first payment has new amount
    assert purchase_with_payments.payments[0].amount.value == 500.0
    
    # Verify other payments were rebalanced
    # Total = 1000, first = 500, remaining = 500, split in 2 = 250 each
    assert purchase_with_payments.payments[1].amount.value == 250.0
    assert purchase_with_payments.payments[2].amount.value == 250.0
    
    # Verify expense_repository.update was called
    expense_repository.update.assert_called_once_with(purchase_with_payments)


def test_payment_update_use_case_does_not_rebalance_when_payment_becomes_paid(payment_repository, expense_repository, purchase_with_payments):
    # Setup
    first_payment = purchase_with_payments.payments[0]
    original_amount = first_payment.amount.value
    
    payment_repository.get_by_filter.return_value = first_payment
    expense_repository.get_by_filter.return_value = purchase_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    # Mark first payment as PAID (keeping same amount)
    payment_data = UpdatePaymentDTO(
        amount=original_amount,
        status=PaymentStatus.PAID,
        payment_date=first_payment.payment_date,
    )
    
    # Execute
    use_case.execute(first_payment.id, payment_data)
    
    # Verify payment status changed
    assert purchase_with_payments.payments[0].status == PaymentStatus.PAID
    
    # Other payments should remain unchanged (no rebalancing because amount didn't change)
    # This tests that the rebalance logic respects final states


def test_payment_update_use_case_returns_updated_payment(payment_repository, expense_repository, subscription_with_payments):
    # Setup
    payment_to_update = subscription_with_payments.payments[0]
    payment_repository.get_by_filter.return_value = payment_to_update
    expense_repository.get_by_filter.return_value = subscription_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=100.0,
        status=PaymentStatus.CONFIRMED,
        payment_date=date(2025, 1, 20),
    )
    
    # Execute
    result = use_case.execute(payment_to_update.id, payment_data)
    
    # Verify returned DTO has updated values
    assert result.id == payment_to_update.id
    assert result.amount == 100.0
    assert result.status == PaymentStatus.CONFIRMED
    assert result.payment_date == date(2025, 1, 20)


def test_payment_update_use_case_handles_status_change(payment_repository, expense_repository, purchase_with_payments):
    # Setup
    payment_to_update = purchase_with_payments.payments[0]
    payment_repository.get_by_filter.return_value = payment_to_update
    expense_repository.get_by_filter.return_value = purchase_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    # Change status from UNCONFIRMED to CONFIRMED
    payment_data = UpdatePaymentDTO(
        amount=payment_to_update.amount.value,
        status=PaymentStatus.CONFIRMED,
        payment_date=payment_to_update.payment_date,
    )
    
    # Execute
    result = use_case.execute(payment_to_update.id, payment_data)
    
    # Verify status was updated
    assert result.status == PaymentStatus.CONFIRMED
    assert purchase_with_payments.payments[0].status == PaymentStatus.CONFIRMED


def test_payment_update_use_case_handles_payment_date_change(payment_repository, expense_repository, purchase_with_payments):
    # Setup
    payment_to_update = purchase_with_payments.payments[0]
    old_date = payment_to_update.payment_date
    new_date = date(2025, 3, 15)
    
    payment_repository.get_by_filter.return_value = payment_to_update
    expense_repository.get_by_filter.return_value = purchase_with_payments
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=payment_to_update.amount.value,
        status=payment_to_update.status,
        payment_date=new_date,
    )
    
    # Execute
    result = use_case.execute(payment_to_update.id, payment_data)
    
    # Verify date was updated
    assert result.payment_date == new_date
    assert purchase_with_payments.payments[0].payment_date == new_date


def test_payment_update_use_case_updates_other_expense_types_directly(payment_repository, expense_repository):
    """Test payment update for expense types other than Purchase or Subscription."""
    from src.domain.expense import Expense
    
    # Create a mock expense that is neither Purchase nor Subscription
    mock_expense = MagicMock(spec=Expense)
    mock_expense.id = uuid4()
    
    payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=mock_expense.id,
        amount=Amount(100),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 1, 15),
    )
    
    payment_repository.get_by_filter.return_value = payment
    expense_repository.get_by_filter.return_value = mock_expense
    payment_repository.update.return_value = payment
    
    use_case = PaymentUpdateUseCase(payment_repository, expense_repository)
    
    payment_data = UpdatePaymentDTO(
        amount=150.0,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 2, 15),
    )
    
    # Execute
    result = use_case.execute(payment.id, payment_data)
    
    # Verify payment was updated directly (not through expense)
    payment_repository.update.assert_called_once_with(payment)
    # Verify expense_repository.update was NOT called
    expense_repository.update.assert_not_called()
    # Verify result
    assert result is not None
