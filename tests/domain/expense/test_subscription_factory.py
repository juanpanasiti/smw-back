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
        'account_id': uuid4(),
        'title': 'Netflix',
        'cc_name': 'Monthly subscription for Netflix',
        'acquired_at': date.today(),
        'amount': Amount(15),
        'first_payment_date': date.today(),
        'category_id': uuid4(),
        'payments': [],
    }


def test_create_subscription(subscription_dict):
    subscription = SubscriptionFactory.create(**subscription_dict)
    assert isinstance(subscription, Subscription), f'Expected Subscription instance, got {type(subscription)}'
    assert subscription.id == subscription_dict['id'], f'Expected id {subscription_dict["id"]}, got {subscription.id}'
    assert subscription.account_id == subscription_dict['account_id'], f'Expected account_id {subscription_dict["account_id"]}, got {subscription.account_id}'
    assert subscription.title == subscription_dict['title'], f'Expected title {subscription_dict["title"]}, got {subscription.title}'
    assert subscription.cc_name == subscription_dict['cc_name'], f'Expected cc_name {subscription_dict["cc_name"]}, got {subscription.cc_name}'
    assert subscription.acquired_at == subscription_dict['acquired_at'], \
        f'Expected acquired_at {subscription_dict["acquired_at"]}, got {subscription.acquired_at}'
    assert subscription.amount == subscription_dict['amount'], f'Expected amount {subscription_dict["amount"]}, got {subscription.amount}'
    assert subscription.first_payment_date == subscription_dict['first_payment_date'], \
        f'Expected first_payment_date {subscription_dict["first_payment_date"]}, got {subscription.first_payment_date}'


def test_create_subscription_invalid_id_none(subscription_dict):
    """Test subscription creation fails with None id."""
    subscription_dict['id'] = None
    with pytest.raises(ValueError, match='id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_id_type(subscription_dict):
    """Test subscription creation fails with invalid id type."""
    subscription_dict['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_account_id_none(subscription_dict):
    """Test subscription creation fails with None account_id."""
    subscription_dict['account_id'] = None
    with pytest.raises(ValueError, match='account_id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_account_id_type(subscription_dict):
    """Test subscription creation fails with invalid account_id type."""
    subscription_dict['account_id'] = 123
    with pytest.raises(ValueError, match='account_id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_title_none(subscription_dict):
    """Test subscription creation fails with None title."""
    subscription_dict['title'] = None
    with pytest.raises(ValueError, match='title must be a non-empty string'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_title_empty(subscription_dict):
    """Test subscription creation fails with empty title."""
    subscription_dict['title'] = '   '
    with pytest.raises(ValueError, match='title must be a non-empty string'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_cc_name_none(subscription_dict):
    """Test subscription creation fails with None cc_name."""
    subscription_dict['cc_name'] = None
    with pytest.raises(ValueError, match='cc_name must be a non-empty string'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_cc_name_empty(subscription_dict):
    """Test subscription creation fails with empty cc_name."""
    subscription_dict['cc_name'] = ''
    with pytest.raises(ValueError, match='cc_name must be a non-empty string'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_acquired_at_none(subscription_dict):
    """Test subscription creation fails with None acquired_at."""
    subscription_dict['acquired_at'] = None
    with pytest.raises(ValueError, match='acquired_at must be a date'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_acquired_at_type(subscription_dict):
    """Test subscription creation fails with invalid acquired_at type."""
    subscription_dict['acquired_at'] = 'not-a-date'
    with pytest.raises(ValueError, match='acquired_at must be a date'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_amount_none(subscription_dict):
    """Test subscription creation fails with None amount."""
    subscription_dict['amount'] = None
    with pytest.raises(ValueError, match='amount must be a positive number'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_amount_type(subscription_dict):
    """Test subscription creation fails with invalid amount type."""
    subscription_dict['amount'] = 100
    with pytest.raises(ValueError, match='amount must be a positive number'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_first_payment_date_none(subscription_dict):
    """Test subscription creation fails with None first_payment_date."""
    subscription_dict['first_payment_date'] = None
    with pytest.raises(ValueError, match='first_payment_date must be a date'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_first_payment_date_type(subscription_dict):
    """Test subscription creation fails with invalid first_payment_date type."""
    subscription_dict['first_payment_date'] = 'invalid'
    with pytest.raises(ValueError, match='first_payment_date must be a date'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_category_id_none(subscription_dict):
    """Test subscription creation fails with None category_id."""
    subscription_dict['category_id'] = None
    with pytest.raises(ValueError, match='category_id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_category_id_type(subscription_dict):
    """Test subscription creation fails with invalid category_id type."""
    subscription_dict['category_id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='category_id must be a UUID'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_payments_none(subscription_dict):
    """Test subscription creation fails with None payments."""
    subscription_dict['payments'] = None
    with pytest.raises(ValueError, match='payments must be a list of Payment instances'):
        SubscriptionFactory.create(**subscription_dict)


def test_create_subscription_invalid_payments_not_list(subscription_dict):
    """Test subscription creation fails when payments is not a list."""
    subscription_dict['payments'] = 'not-a-list'
    with pytest.raises(ValueError, match='payments must be a list of Payment instances'):
        SubscriptionFactory.create(**subscription_dict)
