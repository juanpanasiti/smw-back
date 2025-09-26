import copy
from re import sub
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Subscription, PaymentStatus, PaymentFactory
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


def test_remove_payment(subscription: Subscription):
    payment_to_remove = subscription.payments[0]
    subscription.remove_payment(payment_to_remove.id)
    assert len(subscription.payments) == 0, \
        f'Expected 0 payments, got {len(subscription.payments)}'


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
