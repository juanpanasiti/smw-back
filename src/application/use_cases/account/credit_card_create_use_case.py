from uuid import uuid4

from ...dtos import CreateCreditCardDTO, CreditCardResponseDTO
from ...ports import CreditCardRepository
from src.domain.account import CreditCardFactory
from src.domain.shared import Amount


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
        return CreditCardResponseDTO(
            id=new_credit_card.id,
            owner_id=new_credit_card.owner_id,
            alias=new_credit_card.alias,
            limit=new_credit_card.limit.value,
            is_enabled=new_credit_card.is_enabled,
            main_credit_card_id=new_credit_card.main_credit_card_id,
            next_closing_date=new_credit_card.next_closing_date,
            next_expiring_date=new_credit_card.next_expiring_date,
            financing_limit=new_credit_card.financing_limit.value,
            total_expenses_count=new_credit_card.total_expenses_count,
            total_purchases_count=new_credit_card.total_purchases_count,
            total_subscriptions_count=new_credit_card.total_subscriptions_count,
            used_limit=new_credit_card.used_limit.value,
            available_limit=new_credit_card.available_limit.value,
            used_financing_limit=new_credit_card.used_financing_limit.value,
            available_financing_limit=new_credit_card.available_financing_limit.value,
        )
