from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.expense import ExpenseCategoryUpdateUseCase
from src.application.ports import ExpenseCategoryRepository
from src.domain.expense import ExpenseCategoryFactory, ExpenseCategory
from src.application.dtos import UpdateExpenseCategoryDTO


def get_fake_expense_category(filter: dict) -> ExpenseCategory:
    return ExpenseCategoryFactory.create(
        **filter,
        owner_id=uuid4(),
        name='Groceries',
        description='Monthly grocery shopping',
        is_income=False,
    )


def update_fake_expense_category(category: ExpenseCategory) -> ExpenseCategory:
    return category


@pytest.fixture
def expense_category() -> UpdateExpenseCategoryDTO:
    return UpdateExpenseCategoryDTO(
        name='Groceries',
        description='Monthly grocery shopping',
        is_income=False,
    )


@pytest.fixture
def repo() -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.get_by_filter.side_effect = get_fake_expense_category
    repo.update.side_effect = update_fake_expense_category
    return repo


@pytest.fixture
def repo_no_category() -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.get_by_filter.return_value = None
    return repo


def test_expense_category_update_use_case_success(repo: ExpenseCategoryRepository, expense_category: UpdateExpenseCategoryDTO):
    use_case = ExpenseCategoryUpdateUseCase(repo)
    category_id = uuid4()
    updated_category = use_case.execute(category_id, expense_category)
    assert updated_category.id == category_id
    assert updated_category.name == expense_category.name
    assert updated_category.description == expense_category.description
    assert updated_category.is_income == expense_category.is_income


def test_expense_category_update_use_case_not_found(repo_no_category: ExpenseCategoryRepository, expense_category: UpdateExpenseCategoryDTO):
    use_case = ExpenseCategoryUpdateUseCase(repo_no_category)
    category_id = uuid4()
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(category_id, expense_category)
