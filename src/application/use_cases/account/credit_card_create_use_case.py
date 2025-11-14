from uuid import uuid4

from ...dtos import CreateCreditCardDTO, CreditCardResponseDTO
from ...ports import CreditCardRepository
from src.domain.account import CreditCardFactory
from src.domain.shared import Amount
from .helpers import parse_credit_card


class CreditCardCreateUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_data: CreateCreditCardDTO) -> CreditCardResponseDTO:
        credit_card = CreditCardFactory.create(
            id=uuid4(),
            owner_id=credit_card_data.owner_id,
            alias=credit_card_data.alias,
            limit=Amount(credit_card_data.limit),
            is_enabled=True,
            main_credit_card_id=credit_card_data.main_credit_card_id,
            next_closing_date=credit_card_data.next_closing_date,
            next_expiring_date=credit_card_data.next_expiring_date,
            financing_limit=Amount(credit_card_data.financing_limit),
            expenses=[],
        )
        new_credit_card = self.credit_card_repository.create(credit_card)
        return parse_credit_card(new_credit_card)
