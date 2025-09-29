from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.expense import ExpenseCategoryCreateUseCase
from src.application.ports import ExpenseCategoryRepository
from src.domain.expense import ExpenseCategoryFactory
from src.application.dtos import ExpenseCategoryResponseDTO, CreateExpenseCategoryDTO


@pytest.fixture
def repo() -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.create.return_value = ExpenseCategoryFactory.create(
        id=uuid4(),
        owner_id=uuid4(),
        name='Food',
        description='Expenses for food and groceries',
        is_income=False,
    )
    return repo


def test_expense_category_create_use_case_success(repo: ExpenseCategoryRepository):
    use_case = ExpenseCategoryCreateUseCase(repo)
    create_dto = CreateExpenseCategoryDTO(
        owner_id=uuid4(),
        name='Food',
        description='Expenses for food and groceries',
        is_income=False,
    )
    new_category = use_case.execute(create_dto)

    assert new_category.name == create_dto.name, \
        f'Expected name {create_dto.name}, got {new_category.name}'
    assert new_category.description == create_dto.description, \
        f'Expected description {create_dto.description}, got {new_category.description}'
    assert new_category.is_income == create_dto.is_income, \
        f'Expected is_income {create_dto.is_income}, got {new_category.is_income}'
