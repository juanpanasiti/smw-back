from uuid import uuid4
from datetime import date

import pytest

from src.domain.expense import Purchase, PurchaseFactory, Subscription, SubscriptionFactory
from src.domain.account import CreditCard
from src.domain.shared import Amount


@pytest.fixture
def purchase(main_credit_card: CreditCard) -> Purchase:
    return PurchaseFactory.create(
        id=uuid4(),
        account_id=main_credit_card.id,
        title='Some Purchase',
        cc_name='merpago*someplace',
        acquired_at=date.today(),
        amount=Amount(150.75),
        installments=1,
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[],
    )


@pytest.fixture
def subscription(main_credit_card: CreditCard) -> Subscription:
    return SubscriptionFactory.create(
        id=uuid4(),
        account_id=main_credit_card.id,
        title='Some Subscription',
        cc_name='merpago*someplace',
        acquired_at=date.today(),
        amount=Amount(150.75),
        installments=1,
        first_payment_date=date.today(),
        category_id=uuid4(),
        payments=[],
    )
