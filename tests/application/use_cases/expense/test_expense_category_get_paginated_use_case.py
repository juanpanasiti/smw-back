from unittest.mock import MagicMock

import pytest

from src.application.use_cases.expense import ExpenseCategoryGetPaginatedUseCase
from src.application.ports import ExpenseCategoryRepository
from tests.fixtures.auth_fixtures import user
from src.domain.auth import User
from src.application.dtos import PaginatedResponse


@pytest.fixture
def repo(user: User) -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.get_many_by_filter.return_value = []
    return repo


def test_expense_category_get_paginated_use_case_success(repo: ExpenseCategoryRepository, user: User):
    use_case = ExpenseCategoryGetPaginatedUseCase(
        expense_category_repository=repo)
    result = use_case.execute(filter={'owner_id': user.id}, limit=10, offset=0)
    assert isinstance(result, PaginatedResponse), \
        f'Expected PaginatedResponse, got {type(result)}'
