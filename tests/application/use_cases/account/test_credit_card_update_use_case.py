from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.account import CreditCardUpdateUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import CreditCardResponseDTO, UpdateCreditCardDTO
from src.common.exceptions import RepoNotFoundError
from .helpers import updata_credit_card_dto

@pytest.fixture
def credit_card() -> CreditCardResponseDTO:
    return CreditCardResponseDTO(
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

@pytest.fixture
def update_dto() -> UpdateCreditCardDTO:
    return UpdateCreditCardDTO(
        alias='Updated Card',
        limit=2500000.0,
        financing_limit=2500000.0,
    )


@pytest.fixture
def repo(credit_card: CreditCardResponseDTO, update_dto: UpdateCreditCardDTO) -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_by_filter.return_value = credit_card
    repo.update.return_value = updata_credit_card_dto(credit_card, update_dto)
    return repo
        

def test_credit_card_update_use_case_success(repo: CreditCardRepository, credit_card: CreditCardResponseDTO, update_dto: UpdateCreditCardDTO):
    use_case = CreditCardUpdateUseCase(repo)
    updated_card = use_case.execute(credit_card.id, update_dto)
    
    assert updated_card.alias == update_dto.alias,\
        f'Expected alias {update_dto.alias}, got {updated_card.alias}'
    assert updated_card.limit == update_dto.limit,\
        f'Expected limit {update_dto.limit}, got {updated_card.limit}'
    assert updated_card.financing_limit == update_dto.financing_limit,\
        f'Expected financing limit {update_dto.financing_limit}, got {updated_card.financing_limit}'