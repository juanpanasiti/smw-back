from unittest import mock
from uuid import uuid4, UUID
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Payment, PaymentFactory, Purchase, Expense, PaymentStatus
from src.domain.shared import Amount


@pytest.fixture
def payment_dict() -> dict:
    return {
        'id': uuid4(),
        'expense_id': uuid4(),
        'amount': Amount(100),
        'no_installment': 1,
        'status': PaymentStatus.UNCONFIRMED,
        'payment_date': date.today(),
    }


def test_create_payment(payment_dict):
    payment = PaymentFactory.create(**payment_dict)
    assert isinstance(payment, Payment), f'Expected Payment instance, got {type(payment)}'
    assert payment.id == payment_dict['id'], f'Expected id {payment_dict["id"]}, got {payment.id}'
    assert isinstance(payment.expense_id, UUID), f'Expected expense_id to be UUID, got {type(payment.expense_id)}'
    assert payment.amount == payment_dict['amount'], f'Expected amount {payment_dict["amount"]}, got {payment.amount}'
    assert payment.no_installment == payment_dict['no_installment'], \
        f'Expected no_installment {payment_dict["no_installment"]}, got {payment.no_installment}'
    assert payment.status == payment_dict['status'], f'Expected status {payment_dict["status"]}, got {payment.status}'
    assert payment.payment_date == payment_dict['payment_date'], \
        f'Expected payment_date {payment_dict["payment_date"]}, got {payment.payment_date}'
