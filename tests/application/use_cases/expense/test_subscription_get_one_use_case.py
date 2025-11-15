from unittest.mock import MagicMock
from uuid import uuid4, UUID

import pytest

from src.application.use_cases.expense import SubscriptionGetOneUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import ExpenseResponseDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from tests.fixtures.expense_fixtures import subscription  # noqa: F401
from src.domain.expense import Subscription


def get_fake_subscription(id: UUID, subscription: Subscription) -> Subscription:
    subscription.id = id
    return subscription


@pytest.fixture
def repo(subscription: Subscription) -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.side_effect = lambda filter: get_fake_subscription(filter['id'], subscription)
    return repo


def test_subscription_get_one_use_case_success(repo: ExpenseRepository, subscription: Subscription):
    use_case = SubscriptionGetOneUseCase(repo)
    subscription_id = uuid4()

    expense_response = use_case.execute(subscription_id)

    assert isinstance(expense_response, ExpenseResponseDTO), \
        f'Expected instance of ExpenseResponseDTO, got {type(expense_response)}'
    assert expense_response.id == subscription_id, \
        f'Expected id {subscription_id}, got {expense_response.id}'
    assert expense_response.title == subscription.title, \
        f'Expected title {subscription.title}, got {expense_response.title}'


def test_subscription_get_one_use_case_not_found():
    repo = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.return_value = None
    use_case = SubscriptionGetOneUseCase(repo)
    subscription_id = uuid4()
    with pytest.raises(ValueError, match='Subscription not found'):
        use_case.execute(subscription_id)
