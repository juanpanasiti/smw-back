from uuid import uuid4
from datetime import date

import pytest

from src.domain.account import CreditCardFactory, CreditCard
from src.domain.auth import User
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
