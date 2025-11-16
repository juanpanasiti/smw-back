from uuid import UUID

from ...ports import CreditCardRepository


class CreditCardDeleteUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, credit_card_id: UUID) -> None:
        self.credit_card_repository.delete_by_filter({'id': credit_card_id})
