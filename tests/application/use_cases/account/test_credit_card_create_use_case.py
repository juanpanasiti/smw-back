from unittest.mock import MagicMock

import pytest

from src.application.use_cases.account import CreditCardCreateUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import CreateCreditCardDTO, CreditCardResponseDTO
from src.domain.account import CreditCard
from tests.fixtures.account_fixtures import main_credit_card_dto, main_credit_card, user  # noqa: F401


def create_fake_credit_card(credit_card_data: CreditCard) -> CreditCard:
    return credit_card_data


@pytest.fixture
def repo() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.create.side_effect = create_fake_credit_card
    return repo


@pytest.fixture
def repo_fail() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.create.side_effect = Exception('Database error')
    return repo


def test_credit_card_create_use_case_success(main_credit_card_dto: CreateCreditCardDTO, repo: CreditCardRepository):
    use_case = CreditCardCreateUseCase(credit_card_repository=repo)
    result = use_case.execute(main_credit_card_dto)
    assert isinstance(
        result, CreditCardResponseDTO), f'Expected CreditCardResponseDTO, got {type(result)}'
    assert result.id is not None, 'Expected non-null credit card ID'
    assert result.owner_id == main_credit_card_dto.owner_id, f'Expected owner_id "{main_credit_card_dto.owner_id}", got {result.owner_id}'
    assert result.alias == main_credit_card_dto.alias, f'Expected alias "{main_credit_card_dto.alias}", got {result.alias}'
    assert result.limit == main_credit_card_dto.limit, f'Expected limit {main_credit_card_dto.limit}, got {result.limit}'
    assert result.is_enabled is True, f'Expected is_enabled True, got {result.is_enabled}'
    assert result.main_credit_card_id == main_credit_card_dto.main_credit_card_id, f'Expected main_credit_card_id "{main_credit_card_dto.main_credit_card_id}", got {result.main_credit_card_id}'
    assert result.next_closing_date == main_credit_card_dto.next_closing_date, f'Expected next_closing_date {main_credit_card_dto.next_closing_date}, got {result.next_closing_date}'
    assert result.next_expiring_date == main_credit_card_dto.next_expiring_date, f'Expected next_expiring_date {main_credit_card_dto.next_expiring_date}, got {result.next_expiring_date}'
    assert result.financing_limit == main_credit_card_dto.financing_limit, f'Expected financing_limit {main_credit_card_dto.financing_limit}, got {result.financing_limit}'
    assert result.total_expenses_count == 0, f'Expected total_expenses_count 0, got {result.total_expenses_count}'
    assert result.total_purchases_count == 0, f'Expected total_purchases_count 0, got {result.total_purchases_count}'
    assert result.total_subscriptions_count == 0, f'Expected total_subscriptions_count 0, got {result.total_subscriptions_count}'
    assert result.used_limit == 0.0, f'Expected used_limit 0.0, got {result.used_limit}'
    assert result.available_limit == main_credit_card_dto.limit, f'Expected available_limit {main_credit_card_dto.limit}, got {result.available_limit}'
    assert result.used_financing_limit == 0.0, f'Expected used_financing_limit 0.0, got {result.used_financing_limit}'
    assert result.available_financing_limit == main_credit_card_dto.financing_limit, f'Expected available_financing_limit {main_credit_card_dto.financing_limit}, got {result.available_financing_limit}'

def test_credit_card_create_use_case_fail(main_credit_card_dto: CreateCreditCardDTO, repo_fail: CreditCardRepository):
    use_case = CreditCardCreateUseCase(credit_card_repository=repo_fail)
    with pytest.raises(Exception):
        use_case.execute(main_credit_card_dto)