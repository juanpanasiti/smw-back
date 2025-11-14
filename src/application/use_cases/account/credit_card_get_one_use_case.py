from uuid import UUID

from ...dtos import CreditCardResponseDTO
from ...ports import CreditCardRepository
from src.common.exceptions import RepoNotFoundError
from .helpers import parse_credit_card


class CreditCardGetOneUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID) -> CreditCardResponseDTO:
        credit_card = self.credit_card_repository.get_by_filter({'id': credit_card_id})
        if credit_card is None:
            raise RepoNotFoundError(f'Credit card with id {credit_card_id} not found')
        return parse_credit_card(credit_card)
