import pytest
import copy
from uuid import uuid4
from datetime import date

from src.infrastructure.repositories import PaymentRepositorySQL
from src.infrastructure.database.models import PaymentModel
from src.domain.expense import Payment as PaymentEntity, PaymentFactory, PaymentStatus
from src.domain.shared import Amount
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401


@pytest.fixture
def payment_repo(sqlite_session) -> PaymentRepositorySQL:
    return PaymentRepositorySQL(model=PaymentModel, session_factory=sqlite_session)


@pytest.fixture
def payment() -> PaymentEntity:
    return PaymentFactory.create(
        id=uuid4(),
        expense_id=uuid4(),
        amount=Amount(100.0),
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date.today(),
        is_last_payment=False,
    )


def test_payment_repository_sql_init(payment_repo: PaymentRepositorySQL):
    assert isinstance(payment_repo, PaymentRepositorySQL)
    assert hasattr(payment_repo, 'create')
    assert hasattr(payment_repo, 'get_many_by_filter')
    assert hasattr(payment_repo, 'count_by_filter')
    assert hasattr(payment_repo, 'update')
    assert hasattr(payment_repo, 'delete_by_filter')


def test_payment_repository_get_filter_params(payment_repo: PaymentRepositorySQL):
    params = {
        'expense_id': uuid4(),
        'no_installment': 1,
        'status': 'paid',
        'other_param': 'skip',
    }
    filter_params = payment_repo._get_filter_params(params)
    assert 'expense_id' in filter_params
    assert 'no_installment' in filter_params
    assert 'status' in filter_params
    assert 'other_param' not in filter_params


def test_payment_repository_create(payment_repo: PaymentRepositorySQL, payment: PaymentEntity):
    created = payment_repo.create(payment)
    assert isinstance(created, PaymentEntity)
    assert created.no_installment == payment.no_installment
    assert payment_repo.count_by_filter(filter={'id': payment.id}) == 1


def test_payment_repository_get_many_by_filter(payment_repo: PaymentRepositorySQL, payment: PaymentEntity):
    for i in range(3):
        p = copy.deepcopy(payment)
        p.id = uuid4()
        p.no_installment = i + 1
        payment_repo.create(p)
    total = payment_repo.count_by_filter()
    assert total == 3


def test_payment_repository_get_by_filter(payment_repo: PaymentRepositorySQL, payment: PaymentEntity):
    created = payment_repo.create(payment)
    fetched = payment_repo.get_by_filter({'id': created.id})
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.no_installment == created.no_installment


def test_payment_repository_update(payment_repo: PaymentRepositorySQL, payment: PaymentEntity):
    created = payment_repo.create(payment)
    created.status = PaymentStatus.PAID
    updated = payment_repo.update(created)
    assert updated.status == PaymentStatus.PAID


def test_payment_repository_delete_by_filter(payment_repo: PaymentRepositorySQL, payment: PaymentEntity):
    created = payment_repo.create(payment)
    cnt = payment_repo.count_by_filter(filter={'id': created.id})
    assert cnt == 1
    payment_repo.delete_by_filter({'id': created.id})
    cnt_after = payment_repo.count_by_filter(filter={'id': created.id})
    assert cnt_after == 0
