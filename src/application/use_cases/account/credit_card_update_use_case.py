from uuid import UUID

from ...dtos import CreditCardResponseDTO, UpdateCreditCardDTO
from ...ports import CreditCardRepository
from src.domain.account import CreditCard
from .helpers import parse_credit_card


class CreditCardUpdateUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID, credit_card_data: UpdateCreditCardDTO) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        if credit_card is None:
            raise ValueError('Credit card not found')
        credit_card.update_from_dict(credit_card_data.model_dump(exclude_unset=True))
        updated_credit_card = self.credit_card_repository.update(credit_card)
        return parse_credit_card(updated_credit_card)
