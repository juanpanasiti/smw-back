from src.infrastructure.repositories.expense_category_repository_sql import ExpenseCategoryRepositorySQL
from src.infrastructure.database.models.expense_category_model import ExpenseCategoryModel
import pytest
import copy
from uuid import uuid4

from src.infrastructure.repositories import ExpenseCategoryRepositorySQL
from src.infrastructure.database.models import ExpenseCategoryModel
from src.domain.expense import ExpenseCategory as ExpenseCategoryEntity, ExpenseCategoryFactory
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401
from tests.fixtures.auth_fixtures import user as user_entity  # noqa: F401


@pytest.fixture
def expense_category_repo(sqlite_session) -> ExpenseCategoryRepositorySQL:
    return ExpenseCategoryRepositorySQL(model=ExpenseCategoryModel, session_factory=sqlite_session)


@pytest.fixture
def expense_category(user_entity) -> ExpenseCategoryEntity:
    return ExpenseCategoryFactory.create(
        id=uuid4(),
        owner_id=user_entity.id,
        name='Groceries',
        description='Monthly groceries',
        is_income=False,
    )


def test_expense_category_repository_sql_init(expense_category_repo: ExpenseCategoryRepositorySQL):
    assert isinstance(expense_category_repo, ExpenseCategoryRepositorySQL)
    assert hasattr(expense_category_repo, 'create')
    assert hasattr(expense_category_repo, 'get_many_by_filter')
    assert hasattr(expense_category_repo, 'count_by_filter')
    assert hasattr(expense_category_repo, 'update')
    assert hasattr(expense_category_repo, 'delete_by_filter')


def test_expense_category_repository_get_filter_params(expense_category_repo: ExpenseCategoryRepositorySQL):
    params = {
        'owner_id': uuid4(),
        'name': 'Test',
        'other': 'skip',
    }
    f = expense_category_repo._get_filter_params(params)
    assert 'owner_id' in f and 'name' in f
    assert 'other' not in f


def test_expense_category_repository_create(expense_category_repo: ExpenseCategoryRepositorySQL, expense_category: ExpenseCategoryEntity):
    created = expense_category_repo.create(expense_category)
    assert isinstance(created, ExpenseCategoryEntity)
    assert created.name == expense_category.name
    assert expense_category_repo.count_by_filter(filter={'id': expense_category.id}) == 1


def test_expense_category_repository_get_many_by_filter(expense_category_repo: ExpenseCategoryRepositorySQL, expense_category: ExpenseCategoryEntity):
    for i in range(4):
        c = copy.deepcopy(expense_category)
        c.id = uuid4()
        c.name = f'Cat{i}'
        expense_category_repo.create(c)
    assert expense_category_repo.count_by_filter() == 4


def test_expense_category_repository_get_by_filter(expense_category_repo: ExpenseCategoryRepositorySQL, expense_category: ExpenseCategoryEntity):
    created = expense_category_repo.create(expense_category)
    fetched = expense_category_repo.get_by_filter({'id': created.id})
    assert fetched is not None
    assert fetched.id == created.id


def test_expense_category_repository_update(expense_category_repo: ExpenseCategoryRepositorySQL, expense_category: ExpenseCategoryEntity):
    created = expense_category_repo.create(expense_category)
    created.name = 'Updated Name'
    updated = expense_category_repo.update(created)
    assert updated.name == 'Updated Name'


def test_expense_category_repository_delete_by_filter(expense_category_repo: ExpenseCategoryRepositorySQL, expense_category: ExpenseCategoryEntity):
    created = expense_category_repo.create(expense_category)
    assert expense_category_repo.count_by_filter(filter={'id': created.id}) == 1
    expense_category_repo.delete_by_filter({'id': created.id})
    assert expense_category_repo.count_by_filter(filter={'id': created.id}) == 0


def test_expense_category_repo_interface():
    repo = ExpenseCategoryRepositorySQL(ExpenseCategoryModel)
    assert hasattr(repo, 'create')
    assert hasattr(repo, 'get_by_filter')
