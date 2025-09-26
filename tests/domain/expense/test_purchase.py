import copy
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Purchase, PaymentStatus, ExpenseStatus
from src.domain.shared import Amount


@pytest.fixture
def purchase() -> Purchase:
    return Purchase(
        id=uuid4(),
        account_id=uuid4(),
        title='Laptop',
        cc_name='A new laptop for work',
        acquired_at=date.today(),
        amount=Amount(1500),
        installments=3,
        first_payment_date=date.today(),
        category=MagicMock(),
        payments=[],
    )


def test_is_one_time_payment(purchase: Purchase):
    assert purchase.is_one_time_payment is False  # 3 installments
    purchase.installments = 1
    assert purchase.is_one_time_payment is True


def test_number_of_payments(purchase: Purchase):
    assert len(purchase.payments) == 3  # Should have 3 payments for 3 installments


def test_paid_and_pending_installments(purchase: Purchase):
    # Initially, no payments are made
    paid_amount = Amount(0)
    pending_amount = purchase.amount
    assert len(purchase.payments) == 3
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 3
    assert purchase.done_installments == 0
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    for payment in purchase.payments:
        assert payment.status == PaymentStatus.UNCONFIRMED
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the first installment
    payment_0 = copy.deepcopy(purchase.payments[0])
    payment_0.status = PaymentStatus.PAID
    purchase.update_payment(payment_0)
    paid_amount += payment_0.amount
    pending_amount -= payment_0.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 2
    assert purchase.done_installments == 1
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is False
    assert purchase.payments[2].is_final_status is False
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the second installment
    payment_1 = copy.deepcopy(purchase.payments[1])
    payment_1.status = PaymentStatus.PAID
    purchase.update_payment(payment_1)
    paid_amount += payment_1.amount
    pending_amount -= payment_1.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 1
    assert purchase.done_installments == 2
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is True
    assert purchase.payments[2].is_final_status is False
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_financing_amount == pending_amount
    assert purchase.status == ExpenseStatus.PENDING

    # Simulate paying the last installment
    payment_2 = copy.deepcopy(purchase.payments[2])
    payment_2.status = PaymentStatus.PAID
    purchase.update_payment(payment_2)
    paid_amount += payment_2.amount
    pending_amount -= payment_2.amount
    assert purchase.paid_amount == paid_amount
    assert purchase.pending_installments == 0
    assert purchase.done_installments == 3
    assert purchase.payments[0].is_final_status is True
    assert purchase.payments[1].is_final_status is True
    assert purchase.payments[2].is_final_status is True
    assert purchase.pending_amount == pending_amount
    assert purchase.pending_amount.value == 0.0
    assert purchase.pending_financing_amount.value == 0.0
    assert purchase.status == ExpenseStatus.FINISHED


def test_calculate_payments(purchase: Purchase):
    # Create a purchase with 5 installments
    purchase.installments = 5
    purchase.payments = []
    purchase.calculate_payments()
    assert len(purchase.payments) == 5
    total_amount = sum(payment.amount.value for payment in purchase.payments)
    assert total_amount == pytest.approx(purchase.amount.value)

    # Create a purchase with 1 installment
    purchase.installments = 1
    purchase.payments = []
    purchase.calculate_payments()
    assert len(purchase.payments) == 1
    total_amount = sum(payment.amount.value for payment in purchase.payments)
    assert total_amount == pytest.approx(purchase.amount.value)


def test_to_dict(purchase: Purchase):
    purchase_dict = purchase.to_dict()
    assert purchase_dict['id'] == str(purchase.id)
    assert purchase_dict['title'] == purchase.title
    assert purchase_dict['cc_name'] == purchase.cc_name
    assert purchase_dict['acquired_at'] == purchase.acquired_at.isoformat()
    assert purchase_dict['amount'] == purchase.amount.value
    assert purchase_dict['installments'] == purchase.installments
    assert purchase_dict['first_payment_date'] == purchase.first_payment_date.isoformat()
    assert len(purchase_dict['payments']) == len(purchase.payments)
    assert purchase_dict['status'] == purchase.status.value
