from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.expense import SubscriptionDeleteUseCase
from src.application.ports import ExpenseRepository
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from src.domain.account import CreditCard


@pytest.fixture
def repo() -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.delete_by_filter.return_value = None
    return repo


def test_subscription_delete_use_case_success(repo: ExpenseRepository, main_credit_card: CreditCard):
    use_case = SubscriptionDeleteUseCase(repo)
    subscription_id = uuid4()

    response = use_case.execute(subscription_id)

    assert response is None, f'Expected None, got {response}'
    repo.delete_by_filter.assert_called_once_with({'id': subscription_id})  # type: ignore
