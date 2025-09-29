from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.account import CreditCardDeleteUseCase
from src.application.ports import CreditCardRepository


@pytest.fixture
def repo() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.delete_by_filter.return_value = None
    return repo


@pytest.fixture
def repo_fail() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.delete_by_filter.side_effect = Exception('Database error')
    return repo


def test_credit_card_delete_use_case_success(repo: CreditCardRepository):
    credit_card_id = uuid4()
    use_case = CreditCardDeleteUseCase(credit_card_repository=repo)
    none_response = use_case.execute(credit_card_id)
    assert none_response is None, f'Expected None, got {type(none_response)}'


def test_credit_card_delete_use_case_fail(repo_fail: CreditCardRepository):
    credit_card_id = uuid4()
    use_case = CreditCardDeleteUseCase(credit_card_repository=repo_fail)
    with pytest.raises(Exception):
        use_case.execute(credit_card_id)
