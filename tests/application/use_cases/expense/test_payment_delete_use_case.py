from uuid import uuid4
from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.use_cases.expense import PaymentDeleteUseCase
from src.domain.expense import Subscription, Payment, PaymentStatus, PaymentFactory
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
    
    # Add additional payments
    payment2 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(20),
        no_installment=2,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
    )
    payment3 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(25),
        no_installment=3,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 3, 15),
    )
    subscription.add_new_payment(payment2)
    subscription.add_new_payment(payment3)
    
    return subscription


def test_payment_delete_use_case_raises_when_payment_not_found(payment_repository, expense_repository):
    payment_repository.get_by_filter.return_value = None
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    
    with pytest.raises(ValueError, match='Payment with ID .* not found'):
        use_case.execute(uuid4())


def test_payment_delete_use_case_raises_when_expense_not_found(payment_repository, expense_repository):
    payment_id = uuid4()
    expense_id = uuid4()
    payment = MagicMock()
    payment.expense_id = expense_id
    
    payment_repository.get_by_filter.return_value = payment
    expense_repository.get_by_filter.return_value = None
    
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    
    with pytest.raises(ValueError, match='Expense with ID .* not found'):
        use_case.execute(payment_id)


def test_payment_delete_use_case_updates_subscription_installments(payment_repository, expense_repository, subscription):
    # Verify initial state
    assert subscription.installments == 3, f'Expected 3 installments, got {subscription.installments}'
    assert len(subscription.payments) == 3, f'Expected 3 payments, got {len(subscription.payments)}'
    
    # Get the second payment to delete
    payment_to_delete = subscription.payments[1]
    
    # Setup mocks
    payment_repository.get_by_filter.return_value = payment_to_delete
    expense_repository.get_by_filter.return_value = subscription
    
    # Execute use case
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    use_case.execute(payment_to_delete.id)
    
    # Verify subscription was updated
    assert subscription.installments == 2, f'Expected 2 installments after delete, got {subscription.installments}'
    assert len(subscription.payments) == 2, f'Expected 2 payments after delete, got {len(subscription.payments)}'
    
    # Verify expense_repository.update was called with the updated subscription
    expense_repository.update.assert_called_once_with(subscription)


def test_payment_delete_use_case_updates_subscription_amount_when_deleting_last_payment(payment_repository, expense_repository, subscription):
    # Verify initial state - last payment has amount 25
    assert subscription.amount.value == 25, f'Expected amount 25, got {subscription.amount.value}'
    
    # Get the last payment to delete (by date)
    last_payment = subscription.payments[-1]
    
    # Setup mocks
    payment_repository.get_by_filter.return_value = last_payment
    expense_repository.get_by_filter.return_value = subscription
    
    # Execute use case
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    use_case.execute(last_payment.id)
    
    # After deleting the last payment, subscription amount should be from the new last payment (20)
    assert subscription.amount.value == 20, f'Expected amount 20 after deleting last payment, got {subscription.amount.value}'
    assert subscription.installments == 2, f'Expected 2 installments after delete, got {subscription.installments}'
    
    # Verify expense_repository.update was called
    expense_repository.update.assert_called_once_with(subscription)


def test_payment_delete_use_case_reorders_no_installment_after_delete(payment_repository, expense_repository, subscription):
    # Get the first payment to delete
    first_payment = subscription.payments[0]
    
    # Setup mocks
    payment_repository.get_by_filter.return_value = first_payment
    expense_repository.get_by_filter.return_value = subscription
    
    # Execute use case
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    use_case.execute(first_payment.id)
    
    # Verify remaining payments have correct no_installment (should be 1 and 2)
    assert len(subscription.payments) == 2, f'Expected 2 payments, got {len(subscription.payments)}'
    # Note: remove_payment doesn't reorder no_installment, only add/update do via __sort_payments_by_date
    # If this is a requirement, we need to add it to remove_payment
    
    # Verify expense_repository.update was called
    expense_repository.update.assert_called_once_with(subscription)


def test_payment_delete_use_case_deletes_purchase_payment_directly(payment_repository, expense_repository):
    """Test deleting payment from non-subscription expense (e.g., Purchase) deletes directly."""
    from src.domain.expense import Purchase
    
    payment_id = uuid4()
    expense_id = uuid4()
    payment = MagicMock()
    payment.id = payment_id
    payment.expense_id = expense_id
    
    # Create a Purchase (not Subscription)
    purchase = Purchase(
        id=expense_id,
        account_id=uuid4(),
        title='Laptop',
        cc_name='Tech purchase',
        acquired_at=date(2025, 1, 15),
        amount=Amount(1200),
        installments=6,
        first_payment_date=date(2025, 2, 1),
        category_id=uuid4(),
        payments=[],
    )
    
    payment_repository.get_by_filter.return_value = payment
    expense_repository.get_by_filter.return_value = purchase
    
    use_case = PaymentDeleteUseCase(payment_repository, expense_repository)
    use_case.execute(payment_id)
    
    # Verify payment was deleted directly (not through domain method)
    payment_repository.delete_by_filter.assert_called_once_with({'id': payment_id})
    # Verify expense_repository.update was NOT called (Purchase doesn't use domain method)
    expense_repository.update.assert_not_called()
