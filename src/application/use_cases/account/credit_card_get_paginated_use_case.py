from ...dtos import CreditCardResponseDTO, PaginatedResponse, Pagination
from ...ports import CreditCardRepository
from .helpers import parse_credit_card


class CreditCardGetPaginatedUseCase:
    def __init__(self, credit_card_repository: CreditCardRepository):
        self.credit_card_repository = credit_card_repository

    def execute(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[CreditCardResponseDTO]:
        credit_cards = self.credit_card_repository.get_many_by_filter(filter, limit, offset)
        total = self.credit_card_repository.count_by_filter(filter)
        credit_cards_dto = [parse_credit_card(credit_card) for credit_card in credit_cards]
        pagination = Pagination(
            current_page=offset // limit + 1,
            total_pages=(total // limit) + 1 if total % limit != 0 else total // limit,
            total_items=total,
            per_page=limit,
        )
        return PaginatedResponse[CreditCardResponseDTO](
            items=credit_cards_dto,
            pagination=pagination,
        )
