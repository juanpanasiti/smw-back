import asyncio
from typing import Optional

from app.schemas.credit_card_schemas_v3 import CreditCardRes, NewCreditCardReq, UpdateCreditCardReq
from app.schemas.paginated_schemas import PaginatedResponse
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.credit_card_schemas_v3 import CreditCardListParam
from app.repositories.credit_card_repository_v3 import CreditCardRepository
from app.exceptions import app_exceptions as ae


class CreditCardServiceV3:
    def __init__(self, credit_card_repo: Optional[CreditCardRepository] = CreditCardRepository()):
        self.credit_card_repo = credit_card_repo

    async def count(self, user_id: int) -> int:
        return self.credit_card_repo.count({'user_id': user_id, 'main_credit_card_id': None})

    async def get_paginated(self, token: DecodedJWT, params: CreditCardListParam) -> PaginatedResponse[CreditCardRes]:
        user_id = token.user_id
        params_dict = params.model_dump()
        if params.order_by is not None:
            params_dict['order_by'] = params.order_by.value
        params_dict['main_credit_card_id'] = None

        credit_cards, total_count = await asyncio.gather(
            self.__get_credit_cards(user_id, params_dict),
            self.count(user_id)
        )
        current_page = params.offset // params.limit + 1
        total_pages = total_count // params.limit + 1
        if current_page > total_pages:
            raise ae.NotFoundError(f'Page not found for offset {params.offset} and limit {params.limit}')
        return PaginatedResponse[CreditCardRes](
            results=credit_cards,
            meta={
                'current_page': current_page,
                'total_pages': total_pages,
                'total_items': total_count,
                'per_page': params.limit,
            }
        )

    async def create(self, token: DecodedJWT, data: NewCreditCardReq) -> CreditCardRes:
        user_id = token.user_id
        data_dict = data.model_dump()
        data_dict['user_id'] = user_id
        data_dict['main_credit_card_id'] = None

        return self.credit_card_repo.create(data_dict)

    async def get_one(self, search_filter: dict = {}) -> CreditCardRes:
        credit_card = self.credit_card_repo.get_one(search_filter)
        if not credit_card:
            raise ae.NotFoundError(f'Credit card not found. criteria: {search_filter}')
        return CreditCardRes(**credit_card)

    async def delete(self, search_filter: dict) -> None:
        self.credit_card_repo.get_one(search_filter)
        # TODO: Uncomment when the delete methods are implemented
        # await asyncio.gather(
        # self.__delete_expenses_related(search_filter['id']),
        # self.__delete_extensions_related(search_filter['id']),
        # )
        deleted = self.credit_card_repo.delete(search_filter['id'])
        if not deleted:
            raise ae.NotFoundError(f'Credit card not found. criteria: {search_filter}')
        return None

    async def __delete_expenses_related(self, id):
        expenses = self.expense_repo.get_many(account_id=id)
        for expense in expenses:
            self.expense_service.delete({'id': expense['id']})

    async def __delete_extensions_related(self, id):
        extensions = self.credit_card_repo.get_many(main_credit_card_id=id)
        for extension in extensions:
            self.delete({'id': extension['id']})

    async def __get_credit_cards(self, user_id: int, params_dict: dict) -> list[dict]:
        return self.credit_card_repo.get_many(user_id=user_id, **params_dict)
