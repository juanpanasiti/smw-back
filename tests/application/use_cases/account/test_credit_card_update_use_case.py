from unittest.mock import MagicMock

import pytest

from src.application.use_cases.account import CreditCardUpdateUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import CreditCardResponseDTO, UpdateCreditCardDTO
from src.domain.account import CreditCard
from tests.fixtures.account_fixtures import main_credit_card, updated_credit_card_dto  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401


def fake_update(credit_card: CreditCard) -> CreditCard:
    return credit_card



@pytest.fixture
def repo(main_credit_card: CreditCardResponseDTO) -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_by_filter.return_value = main_credit_card
    repo.update.side_effect = fake_update
    return repo


def test_credit_card_update_use_case_success(repo: CreditCardRepository, main_credit_card: CreditCard, updated_credit_card_dto: UpdateCreditCardDTO):
    use_case = CreditCardUpdateUseCase(repo)
    updated_card = use_case.execute(main_credit_card.id, updated_credit_card_dto)

    assert updated_card.alias == updated_credit_card_dto.alias, \
        f'Expected alias {updated_credit_card_dto.alias}, got {updated_card.alias}'
    assert updated_card.limit == updated_credit_card_dto.limit, \
        f'Expected limit {updated_credit_card_dto.limit}, got {updated_card.limit}'
    assert updated_card.financing_limit == updated_credit_card_dto.financing_limit, \
        f'Expected financing limit {updated_credit_card_dto.financing_limit}, got {updated_card.financing_limit}'
