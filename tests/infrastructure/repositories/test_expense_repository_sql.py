import pytest
import copy
from uuid import uuid4

from src.infrastructure.repositories import ExpenseRepositorySQL
from src.infrastructure.database.models import ExpenseModel, PaymentModel
from src.domain.expense import Purchase as PurchaseEntity
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401
from tests.fixtures.expense_fixtures import purchase  # noqa: F401
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401


@pytest.fixture
def expense_repo(sqlite_session) -> ExpenseRepositorySQL:
    return ExpenseRepositorySQL(model=ExpenseModel, session_factory=sqlite_session)


def test_expense_repository_sql_init(expense_repo: ExpenseRepositorySQL):
    assert isinstance(expense_repo, ExpenseRepositorySQL)
    assert hasattr(expense_repo, 'create')
    assert hasattr(expense_repo, 'get_many_by_filter')
    assert hasattr(expense_repo, 'count_by_filter')
    assert hasattr(expense_repo, 'update')
    assert hasattr(expense_repo, 'delete_by_filter')


def test_expense_repository_get_filter_params(expense_repo: ExpenseRepositorySQL):
    params = {
        'account_id': uuid4(),
        'category_id': uuid4(),
        'expense_type': 'purchase',
        'status': 'active',
        'other_param': 'skip',
    }
    filter_params = expense_repo._get_filter_params(params)
    assert 'account_id' in filter_params
    assert 'category_id' in filter_params
    assert 'expense_type' in filter_params
    assert 'status' in filter_params
    assert 'other_param' not in filter_params


def test_expense_repository_create(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    assert isinstance(created, PurchaseEntity)
    assert created.title == purchase.title
    assert expense_repo.count_by_filter(filter={'id': purchase.id}) == 1


def test_expense_repository_create_persists_payments(
    expense_repo: ExpenseRepositorySQL,
    sqlite_session,
    purchase: PurchaseEntity,
):
    created = expense_repo.create(purchase)
    assert len(created.payments) == purchase.installments

    with sqlite_session() as session:
        stored_payments = session.query(PaymentModel).filter_by(expense_id=purchase.id).all()
        assert len(stored_payments) == purchase.installments


def test_expense_repository_get_many_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    for i in range(3):
        exp = copy.deepcopy(purchase)
        exp.id = uuid4()
        exp.title = f'Expense{i}'
        exp.payments = []
        exp.calculate_payments()
        expense_repo.create(exp)
    total = expense_repo.count_by_filter()
    assert total == 3


def test_expense_repository_get_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    fetched = expense_repo.get_by_filter({'id': created.id})
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == created.title


def test_expense_repository_update(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    created.title = 'Updated Expense Title'
    updated = expense_repo.update(created)
    assert updated.title == 'Updated Expense Title'


def test_expense_repository_delete_by_filter(expense_repo: ExpenseRepositorySQL, purchase: PurchaseEntity):
    created = expense_repo.create(purchase)
    cnt = expense_repo.count_by_filter(filter={'id': created.id})
    assert cnt == 1
    expense_repo.delete_by_filter({'id': created.id})
    cnt_after = expense_repo.count_by_filter(filter={'id': created.id})
    assert cnt_after == 0
