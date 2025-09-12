from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import SubscriptionFactory, Subscription, PaymentStatus, ExpenseCategory as Category
from src.domain.account import Account
from src.domain.shared import Amount


@pytest.fixture
def subscription_dict() -> dict:
    return {
        'id': uuid4(),
        'account': MagicMock(spec=Account),
        'title': 'Netflix',
        'cc_name': 'Monthly subscription for Netflix',
        'acquired_at': date.today(),
        'amount': Amount(15),
        'first_payment_date': date.today(),
        'category': MagicMock(spec=Category),
        'payments': [],
    }


def test_create_subscription(subscription_dict):
    subscription = SubscriptionFactory.create(**subscription_dict)
    assert isinstance(subscription, Subscription), f'Expected Subscription instance, got {type(subscription)}'
    assert subscription.id == subscription_dict['id'], f'Expected id {subscription_dict["id"]}, got {subscription.id}'
    assert subscription.account == subscription_dict['account'], f'Expected account {subscription_dict["account"]}, got {subscription.account}'
    assert subscription.title == subscription_dict['title'], f'Expected title {subscription_dict["title"]}, got {subscription.title}'
    assert subscription.cc_name == subscription_dict['cc_name'], f'Expected cc_name {subscription_dict["cc_name"]}, got {subscription.cc_name}'
    assert subscription.acquired_at == subscription_dict['acquired_at'], \
        f'Expected acquired_at {subscription_dict["acquired_at"]}, got {subscription.acquired_at}'
    assert subscription.amount == subscription_dict['amount'], f'Expected amount {subscription_dict["amount"]}, got {subscription.amount}'
    assert subscription.first_payment_date == subscription_dict['first_payment_date'], \
        f'Expected first_payment_date {subscription_dict["first_payment_date"]}, got {subscription.first_payment_date}'
