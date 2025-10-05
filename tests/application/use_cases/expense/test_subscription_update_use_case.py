from unittest.mock import MagicMock

import pytest

from src.application.use_cases.expense import SubscriptionUpdateUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import UpdateSubscriptionDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from tests.fixtures.expense_fixtures import subscription  # noqa: F401
from src.domain.expense import Subscription


def get_fake_subscription(filter: dict, subscription: Subscription) -> Subscription:
    subscription.id = filter.get('id', subscription.id)
    return subscription


@pytest.fixture
def repo(subscription: Subscription) -> ExpenseRepository:
    repo: ExpenseRepository = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.side_effect = lambda filter: get_fake_subscription(filter, subscription)
    repo.update.side_effect = lambda subscription: subscription
    return repo


def test_subscription_update_use_case_success(repo: ExpenseRepository, subscription: Subscription):
    use_case = SubscriptionUpdateUseCase(repo)
    subscription_id = subscription.id
    update_data = UpdateSubscriptionDTO(
        cc_name='updated*ccname',
        title='Updated Subscription Title',
    )
    updated_subscription = use_case.execute(subscription_id, update_data)
    assert updated_subscription.id == subscription_id
    assert updated_subscription.cc_name == update_data.cc_name
    assert updated_subscription.title == update_data.title
    assert updated_subscription.acquired_at == subscription.acquired_at
