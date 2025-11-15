import copy
from re import sub
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Subscription, Payment, PaymentStatus, PaymentFactory
from src.domain.shared import Amount


@pytest.fixture
def subscription() -> Subscription:
    return Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly subscription for Netflix',
        acquired_at=date.today(),
        amount=Amount(15),
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[],
    )


def test_is_one_time_payment(subscription: Subscription):
    assert subscription.is_one_time_payment is False, \
        f'Expected is_one_time_payment to be False, got {subscription.is_one_time_payment}'


def test_paid_amount(subscription: Subscription):
    '''Debe ser 0 si no hay pagos realizados, luego sumar solo los pagos con status PAID'''
    assert subscription.paid_amount == Amount(0), \
        f'Expected paid_amount to be 0, got {subscription.paid_amount}'

    subscription.payments = [
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(5),
            no_installment=1,
            status=PaymentStatus.PAID,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(10),
            no_installment=2,
            status=PaymentStatus.PAID,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(15),
            no_installment=3,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=date.today(),
        ),
    ]

    assert subscription.paid_amount == Amount(15), \
        f'Expected paid_amount to be 15, got {subscription.paid_amount}'


def test_pending_installments(subscription: Subscription):
    assert subscription.pending_installments == 1, \
        f'Expected pending_installments to be 1, got {subscription.pending_installments}'

    subscription.payments = [
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(5),
            no_installment=1,
            status=PaymentStatus.PAID,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(10),
            no_installment=2,
            status=PaymentStatus.CONFIRMED,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(15),
            no_installment=3,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=date.today(),
        ),
    ]
    assert subscription.pending_installments == 2, \
        f'Expected pending_installments to be 2, got {subscription.pending_installments}'


def test_done_installments(subscription: Subscription):
    assert subscription.done_installments == 0, \
        f'Expected done_installments to be 0, got {subscription.done_installments}'

    subscription.payments = [
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(5),
            no_installment=1,
            status=PaymentStatus.PAID,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(10),
            no_installment=2,
            status=PaymentStatus.CONFIRMED,
            payment_date=date.today(),
        ),
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(15),
            no_installment=3,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=date.today(),
        ),
    ]
    assert subscription.done_installments == 1, \
        f'Expected done_installments to be 1, got {subscription.done_installments}'


def test_pending_financing_amount(subscription: Subscription):
    assert subscription.pending_financing_amount == Amount(0), \
        f'Expected pending_financing_amount to be 0, got {subscription.pending_financing_amount}'


def test_pending_amount(subscription: Subscription):
    assert subscription.pending_amount == subscription.payments[0].amount, \
        f'Expected pending_amount to be {subscription.payments[0].amount}, got {subscription.pending_amount}'

    subscription.payments.append(
        PaymentFactory.create(
            id=uuid4(),
            expense_id=subscription.id,
            amount=Amount(10),
            no_installment=2,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=date.today(),
        )
    )
    assert subscription.pending_amount == Amount(25), \
        f'Expected pending_amount to be 25, got {subscription.pending_amount}'

    subscription.payments[0].status = PaymentStatus.PAID
    assert subscription.pending_amount == Amount(10), \
        f'Expected pending_amount to be 10, got {subscription.pending_amount}'

    subscription.payments.clear()
    assert subscription.pending_amount == Amount(0), \
        f'Expected pending_amount to be 0, got {subscription.pending_amount}'


def test_add_new_payment(subscription: Subscription):
    initial_installments = subscription.installments
    new_payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(25),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date.today(),
    )
    subscription.add_new_payment(new_payment)
    assert len(subscription.payments) == 2, \
        f'Expected 2 payments, got {len(subscription.payments)}'
    assert subscription.amount == new_payment.amount, \
        f'Expected subscription amount to be {new_payment.amount}, got {subscription.amount}'
    assert subscription.installments == 2, \
        f'Expected installments to be 2, got {subscription.installments}'


def test_remove_payment(subscription: Subscription):
    payment_to_remove = subscription.payments[0]
    subscription.remove_payment(payment_to_remove.id)
    assert len(subscription.payments) == 0, \
        f'Expected 0 payments, got {len(subscription.payments)}'
    assert subscription.installments == 0, \
        f'Expected installments to be 0, got {subscription.installments}'


def test_update_payment(subscription: Subscription):
    original_payment = copy.deepcopy(subscription.payments[0])
    updated_payment = copy.deepcopy(original_payment)
    updated_payment.amount = Amount(25)
    subscription.update_payment(original_payment.id, updated_payment)
    assert len(subscription.payments) == 1, \
        f'Expected 1 payment, got {len(subscription.payments)}'
    assert subscription.payments[0].amount == Amount(25), \
        f'Expected payment amount to be 25, got {subscription.payments[0].amount}'
    assert subscription.amount == Amount(25), \
        f'Expected subscription amount to be 25, got {subscription.amount}'


def test_to_dict(subscription: Subscription):
    subscription_dict = subscription.to_dict(include_relationships=True)
    assert subscription_dict['id'] == str(subscription.id), \
        f'Expected id to be {subscription.id}, got {subscription_dict["id"]}'
    assert subscription_dict['account_id'] == str(subscription.account_id), \
        f'Expected account_id to be {subscription.account_id}, got {subscription_dict["account_id"]}'
    assert subscription_dict['category_id'] == str(subscription.category_id), \
        f'Expected category_id to be {subscription.category_id}, got {subscription_dict["category_id"]}'
    assert len(subscription_dict['payments']) == len(subscription.payments), \
        f'Expected {len(subscription.payments)} payments, got {len(subscription_dict["payments"])}'
    for pdict, payment in zip(subscription_dict['payments'], subscription.payments):
        assert pdict == payment.to_dict(), \
            f'Expected payment dict to be {payment.to_dict()}, got {pdict}'


def test_subscription_amount_updates_with_last_payment_on_add():
    '''When adding a new payment, if it becomes the last payment by date, subscription amount should update.'''
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
    
    # Add first payment (will be the last one)
    first_payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(15),
        no_installment=1,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 1, 15),
    )
    subscription.add_new_payment(first_payment)
    assert subscription.amount.value == 15, \
        f'Expected subscription amount to be 15, got {subscription.amount.value}'
    
    # Add second payment with later date and different amount (becomes the new last)
    second_payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(20),
        no_installment=2,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
    )
    subscription.add_new_payment(second_payment)
    assert subscription.amount.value == 20, \
        f'Expected subscription amount to be 20 (last payment amount), got {subscription.amount.value}'
    
    # Add third payment with earlier date (not the last, amount should not change)
    third_payment = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(10),
        no_installment=3,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 1, 10),
    )
    subscription.add_new_payment(third_payment)
    assert subscription.amount.value == 20, \
        f'Expected subscription amount to remain 20 (last payment by date), got {subscription.amount.value}'


def test_subscription_amount_updates_with_last_payment_on_update():
    '''When updating a payment that is the last by date, subscription amount should update.'''
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
    
    # Add payments
    payment1 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(15),
        no_installment=1,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 1, 15),
    )
    payment2 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(15),
        no_installment=2,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
    )
    subscription.add_new_payment(payment1)
    subscription.add_new_payment(payment2)
    
    # Update the last payment's amount
    updated_payment2 = copy.deepcopy(payment2)
    updated_payment2.amount = Amount(25)
    subscription.update_payment(payment2.id, updated_payment2)
    assert subscription.amount.value == 25, \
        f'Expected subscription amount to be 25 (updated last payment), got {subscription.amount.value}'
    
    # Update a non-last payment (should not affect subscription amount)
    updated_payment1 = copy.deepcopy(payment1)
    updated_payment1.amount = Amount(100)
    subscription.update_payment(payment1.id, updated_payment1)
    assert subscription.amount.value == 25, \
        f'Expected subscription amount to remain 25, got {subscription.amount.value}'


def test_subscription_amount_updates_when_payment_date_changes_order():
    '''When updating payment_date changes which payment is last, subscription amount should update accordingly.'''
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
    
    # Add payments
    payment1 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(10),
        no_installment=1,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 1, 15),
    )
    payment2 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(20),
        no_installment=2,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
    )
    subscription.add_new_payment(payment1)
    subscription.add_new_payment(payment2)
    
    # Initially, payment2 is last (amount should be 20)
    assert subscription.amount.value == 20, \
        f'Expected subscription amount to be 20, got {subscription.amount.value}'
    
    # Update payment2's date to be earlier than payment1
    updated_payment2 = copy.deepcopy(payment2)
    updated_payment2.payment_date = date(2025, 1, 10)
    subscription.update_payment(payment2.id, updated_payment2)
    
    # Now payment1 is the last, so subscription amount should be 10
    assert subscription.amount.value == 10, \
        f'Expected subscription amount to be 10 (payment1 is now last), got {subscription.amount.value}'


def test_subscription_installments_updates_with_payments():
    '''Test that installments count updates correctly when adding/removing payments.'''
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
    
    # Initially has 1 payment (created automatically)
    assert subscription.installments == 1, \
        f'Expected installments to be 1, got {subscription.installments}'
    assert len(subscription.payments) == 1, \
        f'Expected 1 payment, got {len(subscription.payments)}'
    
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
    assert subscription.installments == 2, \
        f'Expected installments to be 2 after adding payment, got {subscription.installments}'
    
    # Add third payment
    payment3 = PaymentFactory.create(
        id=uuid4(),
        expense_id=subscription.id,
        amount=Amount(25),
        no_installment=3,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 3, 15),
    )
    subscription.add_new_payment(payment3)
    assert subscription.installments == 3, \
        f'Expected installments to be 3 after adding another payment, got {subscription.installments}'
    
    # Remove one payment
    subscription.remove_payment(payment2.id)
    assert subscription.installments == 2, \
        f'Expected installments to be 2 after removing payment, got {subscription.installments}'
    
    # Remove another payment
    subscription.remove_payment(payment3.id)
    assert subscription.installments == 1, \
        f'Expected installments to be 1 after removing another payment, got {subscription.installments}'


def test_subscription_loaded_from_db_with_multiple_payments_has_correct_installments():
    '''Test that when loading a subscription from DB with multiple payments, installments is correctly calculated.'''
    # Simulate loading a subscription from database with 3 payments already present
    payment1 = PaymentFactory.create(
        id=uuid4(),
        expense_id=uuid4(),  # Will be replaced by subscription id
        amount=Amount(15),
        no_installment=1,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 1, 15),
    )
    payment2 = PaymentFactory.create(
        id=uuid4(),
        expense_id=uuid4(),  # Will be replaced by subscription id
        amount=Amount(20),
        no_installment=2,
        status=PaymentStatus.PAID,
        payment_date=date(2025, 2, 15),
    )
    payment3 = PaymentFactory.create(
        id=uuid4(),
        expense_id=uuid4(),  # Will be replaced by subscription id
        amount=Amount(25),
        no_installment=3,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 3, 15),
    )
    
    # Create subscription with existing payments (as if loaded from DB)
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly subscription',
        acquired_at=date(2025, 1, 1),
        amount=Amount(25),
        first_payment_date=date(2025, 1, 15),
        category_id=uuid4(),
        payments=[payment1, payment2, payment3],
    )
    
    # Update payment expense_ids to match subscription
    for payment in subscription.payments:
        payment.expense_id = subscription.id
    
    # Verify installments matches the number of payments provided
    assert subscription.installments == 3, \
        f'Expected installments to be 3 (from loaded payments), got {subscription.installments}'
    assert len(subscription.payments) == 3, \
        f'Expected 3 payments, got {len(subscription.payments)}'


def test_add_new_payment_raises_when_expense_id_mismatch():
    """Test that adding a payment with wrong expense_id raises ValueError."""
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly',
        acquired_at=date.today(),
        amount=Amount(10),
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[]
    )
    
    wrong_payment = Payment(
        id=uuid4(),
        expense_id=uuid4(),  # Different expense_id
        amount=Amount(10),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date.today(),
        is_last_payment=False
    )
    
    with pytest.raises(ValueError, match='Payment expense ID does not match subscription ID'):
        subscription.add_new_payment(wrong_payment)


def test_remove_payment_raises_when_not_found():
    """Test that removing a non-existent payment raises PaymentNotFoundInExpenseException."""
    from src.domain.expense.exceptions import PaymentNotFoundInExpenseException
    
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly',
        acquired_at=date.today(),
        amount=Amount(10),
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[]
    )
    
    non_existent_id = uuid4()
    with pytest.raises(PaymentNotFoundInExpenseException, match=f'Payment with ID {non_existent_id} not found'):
        subscription.remove_payment(non_existent_id)


def test_update_payment_raises_when_not_found():
    """Test that updating a non-existent payment raises PaymentNotFoundInExpenseException."""
    from src.domain.expense.exceptions import PaymentNotFoundInExpenseException
    
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly',
        acquired_at=date.today(),
        amount=Amount(10),
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[]
    )
    
    non_existent_id = uuid4()
    updated_payment = Payment(
        id=non_existent_id,
        expense_id=subscription.id,
        amount=Amount(20),
        no_installment=1,
        status=PaymentStatus.PAID,
        payment_date=date.today(),
        is_last_payment=False
    )
    
    with pytest.raises(PaymentNotFoundInExpenseException, match=f'Payment with ID {non_existent_id} not found'):
        subscription.update_payment(non_existent_id, updated_payment)


def test_get_next_payment_raises_when_factor_is_zero():
    """Test that get_next_payment raises ValueError when factor is zero or negative."""
    subscription = Subscription(
        id=uuid4(),
        account_id=uuid4(),
        title='Netflix',
        cc_name='Monthly',
        acquired_at=date.today(),
        amount=Amount(10),
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[]
    )
    
    with pytest.raises(ValueError, match='Factor must be greater than zero'):
        subscription.get_next_payment(Amount(0))
    
    with pytest.raises(ValueError, match='Factor must be greater than zero'):
        subscription.get_next_payment(Amount(-1))



