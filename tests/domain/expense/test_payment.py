from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Payment, PaymentStatus, Purchase, Subscription
from src.domain.shared import Amount


@pytest.fixture
def payment() -> Payment:
    expense = MagicMock()
    return Payment(
        id=uuid4(),
        expense=expense,
        amount=Amount(100),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date.today()
    )


def test_is_final_status(payment):
    assert payment.is_final_status is False  # Initial status is UNCONFIRMED
    payment.status = PaymentStatus.CONFIRMED
    assert payment.is_final_status is False
    payment.status = PaymentStatus.PAID
    assert payment.is_final_status is True
    payment.status = PaymentStatus.CANCELED
    assert payment.is_final_status is True
    payment.status = PaymentStatus.SIMULATED
    assert payment.is_final_status is False


def test_is_last_purchase_payment(payment):
    payment.status = PaymentStatus.UNCONFIRMED
    purchase = MagicMock(spec=Purchase)
    subscription = MagicMock(spec=Subscription)
    payment.expense = subscription
    assert payment.is_last_payment is False
    payment.expense = purchase
    purchase.status = PaymentStatus.PAID
    assert payment.is_last_payment is False
    purchase.status = PaymentStatus.CONFIRMED
    purchase.pending_installments = 1
    assert payment.is_last_payment is True


def test_to_dict(payment: Payment):
    payment_dict = payment.to_dict(include_relationships=False)
    assert isinstance(payment_dict, dict)
    assert 'id' in payment_dict
    assert 'expense' in payment_dict
    assert 'amount' in payment_dict
    assert 'no_installment' in payment_dict
    assert 'status' in payment_dict
    assert 'payment_date' in payment_dict
    assert isinstance(payment_dict['expense'], str)
    assert isinstance(payment_dict['amount'], float)
    assert isinstance(payment_dict['no_installment'], int)
    assert payment_dict['status'] in {status.value for status in PaymentStatus}
