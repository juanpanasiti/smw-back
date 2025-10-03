from uuid import UUID

from ...dtos import CreditCardResponseDTO, UpdateCreditCardDTO
from ...ports import CreditCardRepository
from src.domain.account import CreditCard


class CreditCardUpdateUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID, credit_card_data: UpdateCreditCardDTO) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        if credit_card is None:
            raise ValueError("Credit card not found")
        credit_card.update_from_dict(credit_card_data.model_dump(exclude_unset=True))
        updated_credit_card = self.credit_card_repository.update(credit_card)
        return CreditCardResponseDTO(
            id=updated_credit_card.id,
            owner_id=updated_credit_card.owner_id,
            alias=updated_credit_card.alias,
            limit=updated_credit_card.limit.value,
            is_enabled=updated_credit_card.is_enabled,
            main_credit_card_id=updated_credit_card.main_credit_card_id,
            next_closing_date=updated_credit_card.next_closing_date,
            next_expiring_date=updated_credit_card.next_expiring_date,
            financing_limit=updated_credit_card.financing_limit.value,
            total_expenses_count=updated_credit_card.total_expenses_count,
            total_purchases_count=updated_credit_card.total_purchases_count,
            total_subscriptions_count=updated_credit_card.total_subscriptions_count,
            used_limit=updated_credit_card.used_limit.value,
            available_limit=updated_credit_card.available_limit.value,
            used_financing_limit=updated_credit_card.used_financing_limit.value,
            available_financing_limit=updated_credit_card.available_financing_limit.value,
        )
