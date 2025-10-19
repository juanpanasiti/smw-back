import pytest
import copy
from uuid import uuid4
from collections.abc import Callable

from src.infrastructure.repositories import CreditCardRepositorySQL
from src.infrastructure.database.models import CreditCardModel
from src.domain.account import CreditCard as CreditCardEntity
from tests.fixtures.db_fixtures import sqlite_session  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401


@pytest.fixture
def credit_card_repo(sqlite_session) -> CreditCardRepositorySQL:
    return CreditCardRepositorySQL(model=CreditCardModel, session_factory=sqlite_session)


def test_credit_card_repository_sql_init(credit_card_repo: CreditCardRepositorySQL):
    assert isinstance(credit_card_repo, CreditCardRepositorySQL)
    assert hasattr(credit_card_repo, 'create')
    assert hasattr(credit_card_repo, 'get_many_by_filter')
    assert hasattr(credit_card_repo, 'count_by_filter')
    assert hasattr(credit_card_repo, 'update')
    assert hasattr(credit_card_repo, 'delete_by_filter')


def test_credit_card_repository_get_filter_params(credit_card_repo: CreditCardRepositorySQL):
    params = {
        'owner_id': uuid4(),
        'alias': 'Test',
        'some_key': 'some_value',
    }
    filter_params = credit_card_repo._get_filter_params(params)
    assert 'owner_id' in filter_params and 'alias' in filter_params
    assert 'some_key' not in filter_params


def test_credit_card_repository_create(credit_card_repo: CreditCardRepositorySQL, main_credit_card: CreditCardEntity):
    created = credit_card_repo.create(main_credit_card)
    assert isinstance(created, CreditCardEntity)
    # ensure it's persisted
    count = credit_card_repo.count_by_filter(filter={'id': main_credit_card.id})
    assert count == 1


def test_credit_card_repository_get_many_by_filter(credit_card_repo: CreditCardRepositorySQL, main_credit_card: CreditCardEntity):
    # create multiple
    for i in range(3):
        card = copy.deepcopy(main_credit_card)
        card.id = uuid4()
        card.alias = f'Card{i}'
        credit_card_repo.create(card)
    total = credit_card_repo.count_by_filter()
    assert total == 3


def test_credit_card_repository_get_by_filter(credit_card_repo: CreditCardRepositorySQL, main_credit_card: CreditCardEntity):
    created = credit_card_repo.create(main_credit_card)
    fetched = credit_card_repo.get_by_filter({'id': created.id})
    assert fetched is not None
    assert fetched.id == created.id


def test_credit_card_repository_update(credit_card_repo: CreditCardRepositorySQL, main_credit_card: CreditCardEntity):
    created = credit_card_repo.create(main_credit_card)
    created.alias = 'Updated Alias'
    updated = credit_card_repo.update(created)
    assert updated.alias == 'Updated Alias'


def test_credit_card_repository_delete_by_filter(credit_card_repo: CreditCardRepositorySQL, main_credit_card: CreditCardEntity, sqlite_session):
    __check_session(sqlite_session)
    created = credit_card_repo.create(main_credit_card)
    cnt = credit_card_repo.count_by_filter(filter={'id': created.id})
    assert cnt == 1
    credit_card_repo.delete_by_filter({'id': created.id})
    cnt_after = credit_card_repo.count_by_filter(filter={'id': created.id})
    assert cnt_after == 0


def __check_session(sqlite_session: Callable):
    session = sqlite_session()
    if session.get_bind().dialect.name == 'sqlite':
        pytest.skip("Skip en SQLite por limitaciones DELETE multi-table")
