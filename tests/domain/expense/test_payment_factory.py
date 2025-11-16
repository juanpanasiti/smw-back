from uuid import uuid4, UUID
from datetime import date

import pytest

from src.domain.expense import Payment, PaymentFactory, PaymentStatus
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


def test_create_payment_invalid_id_none(payment_dict):
    """Test payment creation fails with None id (bug: raises RuntimeError)."""
    payment_dict['id'] = None
    with pytest.raises(RuntimeError):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_id_type(payment_dict):
    """Test payment creation fails with invalid id type (bug: raises RuntimeError)."""
    payment_dict['id'] = 'not-a-uuid'
    with pytest.raises(RuntimeError):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_expense_id_none(payment_dict):
    """Test payment creation fails with None expense_id."""
    payment_dict['expense_id'] = None
    with pytest.raises(ValueError, match='expense_id must be an instance of UUID'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_expense_id_type(payment_dict):
    """Test payment creation fails with invalid expense_id type."""
    payment_dict['expense_id'] = 123
    with pytest.raises(ValueError, match='expense_id must be an instance of UUID'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_amount_none(payment_dict):
    """Test payment creation fails with None amount."""
    payment_dict['amount'] = None
    with pytest.raises(ValueError, match='amount must be an instance of Amount'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_amount_type(payment_dict):
    """Test payment creation fails with invalid amount type."""
    payment_dict['amount'] = 100
    with pytest.raises(ValueError, match='amount must be an instance of Amount'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_no_installment_none(payment_dict):
    """Test payment creation fails with None no_installment."""
    payment_dict['no_installment'] = None
    with pytest.raises(ValueError, match='no_installment must be at least 1'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_no_installment_zero(payment_dict):
    """Test payment creation fails with zero no_installment."""
    payment_dict['no_installment'] = 0
    with pytest.raises(ValueError, match='no_installment must be at least 1'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_status_none(payment_dict):
    """Test payment creation fails with None status."""
    payment_dict['status'] = None
    with pytest.raises(ValueError, match='status must be an instance of PaymentStatus enum'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_status_type(payment_dict):
    """Test payment creation fails with invalid status type."""
    payment_dict['status'] = 'PAID'
    with pytest.raises(ValueError, match='status must be an instance of PaymentStatus enum'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_payment_date_none(payment_dict):
    """Test payment creation fails with None payment_date."""
    payment_dict['payment_date'] = None
    with pytest.raises(ValueError, match='payment_date must be a date'):
        PaymentFactory.create(**payment_dict)


def test_create_payment_invalid_payment_date_type(payment_dict):
    """Test payment creation fails with invalid payment_date type."""
    payment_dict['payment_date'] = 'invalid'
    with pytest.raises(ValueError, match='payment_date must be a date'):
        PaymentFactory.create(**payment_dict)
