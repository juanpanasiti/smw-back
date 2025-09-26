from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import PurchaseFactory, Purchase, ExpenseCategory as Category
from src.domain.account import Account
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
