from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.expense import ExpenseCategoryCreateUseCase
from src.application.ports import ExpenseCategoryRepository
from src.domain.expense import ExpenseCategoryFactory
from src.application.dtos import ExpenseCategoryResponseDTO, CreateExpenseCategoryDTO
from tests.fixtures.auth_fixtures import user
from src.domain.auth import User


@pytest.fixture
def repo(user: User) -> ExpenseCategoryRepository:
    repo: ExpenseCategoryRepository = MagicMock(spec=ExpenseCategoryRepository)
    repo.create.return_value = ExpenseCategoryFactory.create(
        id=uuid4(),
        owner_id=user.id,
        name='Food',
        description='Expenses for food and groceries',
        is_income=False,
    )
    return repo


def test_expense_category_create_use_case_success(repo: ExpenseCategoryRepository, user: User):
    use_case = ExpenseCategoryCreateUseCase(repo)
    create_dto = CreateExpenseCategoryDTO(
        owner_id=user.id,
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
    assert new_category.owner_id == create_dto.owner_id, \
        f'Expected owner_id {create_dto.owner_id}, got {new_category.owner_id}'
    assert new_category.id is not None, 'Expected id to be set'
    assert isinstance(new_category, ExpenseCategoryResponseDTO), \
        f'Expected instance of ExpenseCategoryResponseDTO, got {type(new_category)}'
