from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.expense import ExpenseGetPaginatedUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import ExpenseResponseDTO
from tests.fixtures.expense_fixtures import purchase, subscription  # noqa: F401
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401


@pytest.fixture
def repo(purchase, subscription) -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.count_by_filter.return_value = 2
    repo.get_many_by_filter.return_value = [
        purchase,
        subscription
    ]

    return repo


def test_expense_get_paginated_use_case_success(repo: ExpenseRepository):
    use_case = ExpenseGetPaginatedUseCase(repo)
    filter = {'account_id': uuid4()}
    limit = 10
    offset = 0

    paginated_response = use_case.execute(filter, limit, offset)

    assert paginated_response.pagination.total_items == 2, \
        f'Expected total_items 2, got {paginated_response.pagination.total_items}'
    assert len(paginated_response.items) == 2, \
        f'Expected 2 items, got {len(paginated_response.items)}'
    assert all(isinstance(item, ExpenseResponseDTO) for item in paginated_response.items), \
        'All items should be instances of ExpenseResponseDTO'
