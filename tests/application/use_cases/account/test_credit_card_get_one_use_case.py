from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.account import CreditCardGetOneUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import CreditCardResponseDTO
from src.common.exceptions import RepoNotFoundError


@pytest.fixture
def repo() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_by_filter.return_value = CreditCardResponseDTO(
        id=uuid4(),
        owner_id=uuid4(),
        alias='Personal Card',
        limit=2000000.0,
        is_enabled=True,
        main_credit_card_id=None,
        next_closing_date=date.today(),
        next_expiring_date=date.today(),
        financing_limit=2000000.0,
        total_expenses_count=0,
        total_purchases_count=0,
        total_subscriptions_count=0,
        used_limit=0.0,
        available_limit=2000000.0,
        used_financing_limit=0.0,
        available_financing_limit=2000000.0,
    )
    return repo


@pytest.fixture
def repo_fail() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_by_filter.side_effect = Exception('Database error')
    return repo


@pytest.fixture
def repo_none() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_by_filter.return_value = None
    return repo


def test_credit_card_get_one_use_case_success(repo: CreditCardRepository):
    use_case = CreditCardGetOneUseCase(credit_card_repository=repo)
    result = use_case.execute(credit_card_id=uuid4())
    assert isinstance(
        result, CreditCardResponseDTO), f'Expected CreditCardResponseDTO, got {type(result)}'


def test_credit_card_get_one_use_case_not_found(repo_none: CreditCardRepository):
    use_case = CreditCardGetOneUseCase(credit_card_repository=repo_none)
    with pytest.raises(RepoNotFoundError):
        use_case.execute(credit_card_id=uuid4())


def test_credit_card_get_one_use_case_fail(repo_fail: CreditCardRepository):
    use_case = CreditCardGetOneUseCase(credit_card_repository=repo_fail)
    with pytest.raises(Exception):
        use_case.execute(credit_card_id=uuid4())
