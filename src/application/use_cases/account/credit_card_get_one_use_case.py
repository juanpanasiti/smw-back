from uuid import UUID

from ...dtos import CreditCardResponseDTO
from ...ports import CreditCardRepository


class CreditCardGetOneUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        return CreditCardResponseDTO.model_validate(credit_card)
