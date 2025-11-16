from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.expense import ExpenseCategoryDeleteUseCase
from src.application.ports import ExpenseCategoryRepository
from tests.fixtures.auth_fixtures import user
from src.domain.auth import User


@pytest.fixture
def repo(user: User) -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.delete_by_filter.return_value = None
    return repo


@pytest.fixture
def repo_fail() -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.delete_by_filter.side_effect = Exception('Database error')
    return repo


def test_expense_category_delete_use_case_success(repo: ExpenseCategoryRepository):
    use_case = ExpenseCategoryDeleteUseCase(repo)
    result = use_case.execute(uuid4())
    assert result is None, f'Expected None, got {type(result)}'


def test_expense_category_delete_use_case_fail(repo_fail: ExpenseCategoryRepository):
    use_case = ExpenseCategoryDeleteUseCase(repo_fail)
    with pytest.raises(Exception):
        use_case.execute(uuid4())
