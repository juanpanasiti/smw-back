from uuid import uuid4
from datetime import date

import pytest

from src.domain.account import CreditCardFactory, CreditCard
from src.domain.shared import Amount
from src.application.dtos import CreateCreditCardDTO
from .auth_fixtures import user


@pytest.fixture
def main_credit_card_dto() -> CreateCreditCardDTO:
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
def main_credit_card() -> CreditCard:
    return CreditCardFactory.create(
        id=uuid4(),
        owner_id=uuid4(),
        alias='Personal Card',
        limit=Amount(2000000.0),
        is_enabled=True,
        main_credit_card_id=None,
        next_closing_date=date.today(),
        next_expiring_date=date.today(),
        financing_limit=Amount(2000000.0),
        expenses=[],
    )
