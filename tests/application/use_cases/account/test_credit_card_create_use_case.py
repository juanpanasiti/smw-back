from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.account import CreditCardCreateUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import CreateCreditCardDTO, CreditCardResponseDTO


@pytest.fixture
def create_dto() -> CreateCreditCardDTO:
    return CreateCreditCardDTO(
        owner_id=uuid4(),
        alias='Personal Card',
        limit=2000000.0,
        financing_limit=2000000.0,
        main_credit_card_id=None,
        next_closing_date=date.today(),
        next_expiring_date=date.today(),
    )


@pytest.fixture
def repo(create_dto: CreateCreditCardDTO) -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.create.return_value = CreditCardResponseDTO(
        id=uuid4(),
        owner_id=create_dto.owner_id,
        alias=create_dto.alias,
        limit=create_dto.limit,
        is_enabled=True,
        main_credit_card_id=create_dto.main_credit_card_id,
        next_closing_date=create_dto.next_closing_date,
        next_expiring_date=create_dto.next_expiring_date,
        financing_limit=create_dto.financing_limit,
        total_expenses_count=0,
        total_purchases_count=0,
        total_subscriptions_count=0,
        used_limit=0.0,
        available_limit=create_dto.limit,
        used_financing_limit=0.0,
        available_financing_limit=create_dto.financing_limit,
    )
    return repo


@pytest.fixture
def repo_fail() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.create.side_effect = Exception('Database error')
    return repo


def test_credit_card_create_use_case_success(create_dto: CreateCreditCardDTO, repo: CreditCardRepository):
    use_case = CreditCardCreateUseCase(credit_card_repository=repo)
    result = use_case.execute(create_dto)
    assert isinstance(
        result, CreditCardResponseDTO), f'Expected CreditCardResponseDTO, got {type(result)}'
    assert result.id is not None, 'Expected non-null credit card ID'
    assert result.owner_id == create_dto.owner_id, f'Expected owner_id "{create_dto.owner_id}", got {result.owner_id}'
    assert result.alias == create_dto.alias, f'Expected alias "{create_dto.alias}", got {result.alias}'
    assert result.limit == create_dto.limit, f'Expected limit {create_dto.limit}, got {result.limit}'
    assert result.is_enabled is True, f'Expected is_enabled True, got {result.is_enabled}'
    assert result.main_credit_card_id == create_dto.main_credit_card_id, f'Expected main_credit_card_id "{create_dto.main_credit_card_id}", got {result.main_credit_card_id}'
    assert result.next_closing_date == create_dto.next_closing_date, f'Expected next_closing_date {create_dto.next_closing_date}, got {result.next_closing_date}'
    assert result.next_expiring_date == create_dto.next_expiring_date, f'Expected next_expiring_date {create_dto.next_expiring_date}, got {result.next_expiring_date}'
    assert result.financing_limit == create_dto.financing_limit, f'Expected financing_limit {create_dto.financing_limit}, got {result.financing_limit}'
    assert result.total_expenses_count == 0, f'Expected total_expenses_count 0, got {result.total_expenses_count}'
    assert result.total_purchases_count == 0, f'Expected total_purchases_count 0, got {result.total_purchases_count}'
    assert result.total_subscriptions_count == 0, f'Expected total_subscriptions_count 0, got {result.total_subscriptions_count}'
    assert result.used_limit == 0.0, f'Expected used_limit 0.0, got {result.used_limit}'
    assert result.available_limit == create_dto.limit, f'Expected available_limit {create_dto.limit}, got {result.available_limit}'
    assert result.used_financing_limit == 0.0, f'Expected used_financing_limit 0.0, got {result.used_financing_limit}'
    assert result.available_financing_limit == create_dto.financing_limit, f'Expected available_financing_limit {create_dto.financing_limit}, got {result.available_financing_limit}'

def test_credit_card_create_use_case_fail(create_dto: CreateCreditCardDTO, repo_fail: CreditCardRepository):
    use_case = CreditCardCreateUseCase(credit_card_repository=repo_fail)
    with pytest.raises(Exception):
        use_case.execute(create_dto)