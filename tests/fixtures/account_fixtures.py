from uuid import uuid4
from datetime import date

import pytest

from src.domain.account import CreditCardFactory, CreditCard
from src.domain.auth import User
from src.domain.shared import Amount
from src.application.dtos import CreateCreditCardDTO, UpdateCreditCardDTO
from .auth_fixtures import user


@pytest.fixture
def main_credit_card(user: User) -> CreditCard:
    return CreditCardFactory.create(
        id=uuid4(),
        owner_id=user.id,
        alias='Personal Card',
        limit=Amount(2000000.0),
        is_enabled=True,
        main_credit_card_id=None,
        next_closing_date=date.today(),
        next_expiring_date=date.today(),
        financing_limit=Amount(2000000.0),
        expenses=[],
    )


@pytest.fixture
def main_credit_card_dto(main_credit_card: CreditCard) -> CreateCreditCardDTO:
    return CreateCreditCardDTO(
        owner_id=main_credit_card.owner_id,
        alias=main_credit_card.alias,
        limit=main_credit_card.limit.value,
        financing_limit=main_credit_card.financing_limit.value,
        main_credit_card_id=main_credit_card.main_credit_card_id,
        next_closing_date=main_credit_card.next_closing_date,
        next_expiring_date=main_credit_card.next_expiring_date,
    )


@pytest.fixture
def updated_credit_card_dto() -> UpdateCreditCardDTO:
    return UpdateCreditCardDTO(
        alias='Updated Card',
        limit=2500000.0,
        financing_limit=2500000.0,
    )
