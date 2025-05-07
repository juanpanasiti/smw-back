from typing import Optional

from app.schemas.credit_card_schemas_v3 import CreditCardRes, NewCreditCardReq, UpdateCreditCardReq
from app.schemas.paginated_schemas import PaginatedResponse
from app.exceptions import server_exceptions as se, client_exceptions as ce, app_exceptions as ae
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.credit_card_schemas_v3 import CreditCardListParam
from app.services.credit_card_service_v3 import CreditCardServiceV3


class CreditCardControllerV3:
    def __init__(self, credit_card_service: Optional[CreditCardServiceV3] = CreditCardServiceV3()):
        self.credit_card_service = credit_card_service

    async def get_paginated(self, token: DecodedJWT, params: CreditCardListParam) -> PaginatedResponse[CreditCardRes]:
        try:
            return await self.credit_card_service.get_paginated(token, params)
        except ae.NotFoundError as e:
            raise ce.NotFound(e.message, 'CREDIT_CARDS_PAGE_NOT_FOUND')
        except Exception as e:
            raise se.InternalServerError('An error occurred while fetching credit cards', 'CREDIT_CARDS_UNHANDLED_ERROR')

    async def create(self, token: DecodedJWT, data: NewCreditCardReq) -> CreditCardRes:
        try:
            return await self.credit_card_service.create(token, data)
        except Exception as e:
            raise se.InternalServerError('An error occurred while creating the credit card', 'CREDIT_CARD_UNHANDLED_ERROR')

    async def get_by_id(self, token: DecodedJWT, credit_card_id: int) -> CreditCardRes:
        try:
            return await self.credit_card_service.get_one({'id': credit_card_id, 'user_id': token.user_id})
        except ae.NotFoundError as e:
            raise ce.NotFound(e.message, 'CREDIT_CARD_NOT_FOUND')
        except Exception as e:
            raise se.InternalServerError('An error occurred while fetching the credit card', 'CREDIT_CARD_UNHANDLED_ERROR')

    async def delete(self, token: DecodedJWT, credit_card_id: int) -> None:
        try:
            await self.credit_card_service.delete({'id': credit_card_id, 'user_id': token.user_id})
        except ae.NotFoundError as e:
            raise ce.NotFound(e.message, 'CREDIT_CARD_NOT_FOUND')
        except Exception as e:

            # !DELETE PRINT
            print('\033[91m', str(e), '\033[0m')
            raise se.InternalServerError('An error occurred while deleting the credit card', 'CREDIT_CARD_UNHANDLED_ERROR')
