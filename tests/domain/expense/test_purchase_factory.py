from uuid import uuid4
from datetime import date

import pytest

from src.domain.expense import PurchaseFactory, Purchase
from src.domain.shared import Amount


@pytest.fixture
def purchase_dict() -> dict:
    return {
        'id': uuid4(),
        'account_id': uuid4(),
        'title': 'Laptop',
        'cc_name': 'A new laptop for work',
        'acquired_at': date.today(),
        'amount': Amount(1500),
        'installments': 3,
        'first_payment_date': date.today(),
        'category_id':  uuid4(),
        'payments': [],
    }


def test_create_purchase(purchase_dict):
    purchase = PurchaseFactory.create(**purchase_dict)
    assert isinstance(purchase, Purchase), f'Expected Purchase instance, got {type(purchase)}'
    assert purchase.id == purchase_dict['id'], f'Expected id {purchase_dict["id"]}, got {purchase.id}'
    assert purchase.account_id == purchase_dict['account_id'], f'Expected account_id {purchase_dict["account_id"]}, got {purchase.account_id}'
    assert purchase.title == purchase_dict['title'], f'Expected title {purchase_dict["title"]}, got {purchase.title}'
    assert purchase.cc_name == purchase_dict['cc_name'], f'Expected cc_name {purchase_dict["cc_name"]}, got {purchase.cc_name}'
    assert purchase.acquired_at == purchase_dict['acquired_at'], f'Expected acquired_at {purchase_dict["acquired_at"]}, got {purchase.acquired_at}'
    assert purchase.amount == purchase_dict['amount'], f'Expected amount {purchase_dict["amount"]}, got {purchase.amount}'
    assert purchase.installments == purchase_dict['installments'], f'Expected installments {purchase_dict["installments"]}, got {purchase.installments}'
    assert purchase.first_payment_date == purchase_dict['first_payment_date'], \
        f'Expected first_payment_date {purchase_dict["first_payment_date"]}, got {purchase.first_payment_date}'
    assert purchase.category_id == purchase_dict['category_id'], \
        f'Expected category_id {purchase_dict["category_id"]}, got {purchase.category_id}'
    assert purchase.payments == purchase_dict['payments'], \
        f'Expected payments {purchase_dict["payments"]}, got {purchase.payments}'


def test_create_purchase_invalid_id_none(purchase_dict):
    """Test purchase creation fails with None id."""
    purchase_dict['id'] = None
    with pytest.raises(ValueError, match='id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_id_type(purchase_dict):
    """Test purchase creation fails with invalid id type."""
    purchase_dict['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_account_id_none(purchase_dict):
    """Test purchase creation fails with None account_id."""
    purchase_dict['account_id'] = None
    with pytest.raises(ValueError, match='account_id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_account_id_type(purchase_dict):
    """Test purchase creation fails with invalid account_id type."""
    purchase_dict['account_id'] = 123
    with pytest.raises(ValueError, match='account_id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_title_none(purchase_dict):
    """Test purchase creation fails with None title."""
    purchase_dict['title'] = None
    with pytest.raises(ValueError, match='title must be a non-empty string'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_title_empty(purchase_dict):
    """Test purchase creation fails with empty title."""
    purchase_dict['title'] = '   '
    with pytest.raises(ValueError, match='title must be a non-empty string'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_cc_name_none(purchase_dict):
    """Test purchase creation fails with None cc_name."""
    purchase_dict['cc_name'] = None
    with pytest.raises(ValueError, match='cc_name must be a non-empty string'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_cc_name_empty(purchase_dict):
    """Test purchase creation fails with empty cc_name."""
    purchase_dict['cc_name'] = ''
    with pytest.raises(ValueError, match='cc_name must be a non-empty string'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_acquired_at_none(purchase_dict):
    """Test purchase creation fails with None acquired_at."""
    purchase_dict['acquired_at'] = None
    with pytest.raises(ValueError, match='acquired_at must be a date'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_acquired_at_type(purchase_dict):
    """Test purchase creation fails with invalid acquired_at type."""
    purchase_dict['acquired_at'] = 'not-a-date'
    with pytest.raises(ValueError, match='acquired_at must be a date'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_amount_none(purchase_dict):
    """Test purchase creation fails with None amount."""
    purchase_dict['amount'] = None
    with pytest.raises(ValueError, match='amount must be a valid Amount instance'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_amount_type(purchase_dict):
    """Test purchase creation fails with invalid amount type."""
    purchase_dict['amount'] = 100
    with pytest.raises(ValueError, match='amount must be a valid Amount instance'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_installments_none(purchase_dict):
    """Test purchase creation fails with None installments."""
    purchase_dict['installments'] = None
    with pytest.raises(ValueError, match='installments must be a positive integer'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_installments_zero(purchase_dict):
    """Test purchase creation fails with zero installments."""
    purchase_dict['installments'] = 0
    with pytest.raises(ValueError, match='installments must be a positive integer'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_first_payment_date_none(purchase_dict):
    """Test purchase creation fails with None first_payment_date."""
    purchase_dict['first_payment_date'] = None
    with pytest.raises(ValueError, match='first_payment_date must be a date'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_first_payment_date_type(purchase_dict):
    """Test purchase creation fails with invalid first_payment_date type."""
    purchase_dict['first_payment_date'] = 'invalid'
    with pytest.raises(ValueError, match='first_payment_date must be a date'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_category_id_none(purchase_dict):
    """Test purchase creation fails with None category_id."""
    purchase_dict['category_id'] = None
    with pytest.raises(ValueError, match='category_id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_category_id_type(purchase_dict):
    """Test purchase creation fails with invalid category_id type."""
    purchase_dict['category_id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='category_id must be a UUID'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_payments_none(purchase_dict):
    """Test purchase creation fails with None payments."""
    purchase_dict['payments'] = None
    with pytest.raises(ValueError, match='payments must be a list of Payment instances'):
        PurchaseFactory.create(**purchase_dict)


def test_create_purchase_invalid_payments_not_list(purchase_dict):
    """Test purchase creation fails when payments is not a list."""
    purchase_dict['payments'] = 'not-a-list'
    with pytest.raises(ValueError, match='payments must be a list of Payment instances'):
        PurchaseFactory.create(**purchase_dict)
