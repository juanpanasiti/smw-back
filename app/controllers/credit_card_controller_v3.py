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
