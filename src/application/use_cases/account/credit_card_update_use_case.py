from uuid import UUID

from src.domain.account import CreditCardFactory
from ...dtos import CreditCardResponseDTO, UpdateCreditCardDTO
from ...ports import CreditCardRepository

class CreditCardUpdateUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID, credit_card_data: UpdateCreditCardDTO) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        if credit_card is None:
            raise ValueError("Credit card not found")
        for field, value in credit_card_data.model_dump(exclude_unset=True).items():
            setattr(credit_card, field, value)
        updated_credit_card = self.credit_card_repository.update(credit_card)
        return CreditCardResponseDTO.model_validate(updated_credit_card)