import copy
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

import pytest

from src.domain.expense import Subscription, PaymentStatus, ExpenseStatus
from src.domain.shared import Amount


@pytest.fixture
def subscription() -> Subscription:
    return Subscription(
        id=uuid4(),
        account=MagicMock(),
        title='Netflix',
        cc_name='Monthly subscription for Netflix',
        acquired_at=date.today(),
        amount=Amount(15),
        first_payment_date=date.today(),
        category=MagicMock(),
        payments=[],
    )


def test_is_one_time_payment(subscription: Subscription):
    assert subscription.is_one_time_payment is False, \
        f'Expected is_one_time_payment to be False, got {subscription.is_one_time_payment}'
