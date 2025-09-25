from ...dtos import CreateCreditCardDTO, CreditCardResponseDTO
from ...ports import CreditCardRepository
from src.domain.account import CreditCardFactory


class CreditCardCreateUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_data: CreateCreditCardDTO) -> CreditCardResponseDTO:
        credit_card = CreditCardFactory.create(**credit_card_data.model_dump())
        new_credit_card = self.credit_card_repository.create(credit_card)
        return CreditCardResponseDTO.model_validate(new_credit_card)
