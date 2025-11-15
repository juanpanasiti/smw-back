from unittest.mock import MagicMock
from uuid import uuid4, UUID

import pytest

from src.application.use_cases.expense import PurchaseGetOneUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import ExpenseResponseDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from tests.fixtures.expense_fixtures import purchase  # noqa: F401
from src.domain.expense import Purchase


def get_fake_purchase(id: UUID, purchase: Purchase) -> Purchase:
    purchase.id = id
    return purchase


@pytest.fixture
def repo(purchase: Purchase) -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.side_effect = lambda filter: get_fake_purchase(filter['id'], purchase)
    return repo


def test_purchase_get_one_use_case_success(repo: ExpenseRepository, purchase: Purchase):
    use_case = PurchaseGetOneUseCase(repo)
    purchase_id = uuid4()

    expense_response = use_case.execute(purchase_id)

    assert isinstance(expense_response, ExpenseResponseDTO), \
        f'Expected instance of ExpenseResponseDTO, got {type(expense_response)}'
    assert expense_response.id == purchase_id, \
        f'Expected id {purchase_id}, got {expense_response.id}'
    assert expense_response.title == purchase.title, \
        f'Expected title {purchase.title}, got {expense_response.title}'


def test_purchase_get_one_use_case_not_found():
    repo = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.return_value = None
    use_case = PurchaseGetOneUseCase(repo)
    purchase_id = uuid4()
    with pytest.raises(ValueError, match='Purchase not found'):
        use_case.execute(purchase_id)
