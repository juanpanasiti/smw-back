from uuid import UUID

from ...dtos import CreditCardResponseDTO
from ...ports import CreditCardRepository
from src.common.exceptions import RepoNotFoundError


class CreditCardGetOneUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        if credit_card is None:
            raise RepoNotFoundError(f'Credit card with id {credit_card_id} not found')
        return CreditCardResponseDTO(
            id=credit_card.id,
            owner_id=credit_card.owner_id,
            alias=credit_card.alias,
            limit=credit_card.limit.value,
            is_enabled=credit_card.is_enabled,
            main_credit_card_id=credit_card.main_credit_card_id,
            next_closing_date=credit_card.next_closing_date,
            next_expiring_date=credit_card.next_expiring_date,
            financing_limit=credit_card.financing_limit.value,
            total_expenses_count=credit_card.total_expenses_count,
            total_purchases_count=credit_card.total_purchases_count,
            total_subscriptions_count=credit_card.total_subscriptions_count,
            used_limit=credit_card.used_limit.value,
            available_limit=credit_card.available_limit.value,
            used_financing_limit=credit_card.used_financing_limit.value,
            available_financing_limit=credit_card.available_financing_limit.value,
        )
