import logging
from typing import List


from app.exceptions import client_exceptions as ce
from app.exceptions import handle_exceptions
from app.services import CreditCardService
from app.core.enums.role_enum import ADMIN_ROLES
from app.schemas.credit_card_schemas import NewCreditCardReq, UpdateCreditCardReq, CreditCardRes, CreditCardListParam
from app.schemas.auth_schemas import DecodedJWT

logger = logging.getLogger(__name__)


class CreditCardController():
    def __init__(self) -> None:
        self.__credit_card_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

    @handle_exceptions
    def create(self, token: DecodedJWT, new_credit_card: NewCreditCardReq) -> CreditCardRes:
        if new_credit_card.user_id is not None and new_credit_card.user_id != token.user_id and token.role not in ADMIN_ROLES:
            raise ce.Forbidden('You can only create credit cards for yourself', 'CREATE_CREDIT_CARD_FOR_OTHER_USER_ERROR')

        if new_credit_card.user_id is None:
            new_credit_card.user_id = token.user_id

        return self.credit_card_service.create(new_credit_card)

    @handle_exceptions
    def get_list(self, token: DecodedJWT, params: CreditCardListParam) -> List[CreditCardRes]:
        return self.credit_card_service.get_list(token.user_id, params)

    @handle_exceptions
    def get_by_id(self, token: DecodedJWT, cc_id: int) -> CreditCardRes:
        search_filter = {'id': cc_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        credit_card = self.credit_card_service.get_one(search_filter)
        if credit_card is None:
            raise ce.NotFound('Credit card not found', 'CREDIT_CARD_NOT_FOUND')
        return credit_card

    @handle_exceptions
    def update(self, token: DecodedJWT, cc_id: int, credit_card: UpdateCreditCardReq) -> CreditCardRes:
        if credit_card.user_id is not None and token.role not in ADMIN_ROLES and token.user_id != credit_card.user_id:
            raise ce.Forbidden('You can only update your own credit cards', 'UPDATE_CREDIT_CARD_FOR_OTHER_USER_ERROR')
        search_filter = {'id': cc_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id

        return self.credit_card_service.update(credit_card, search_filter)

    @handle_exceptions
    def delete_one(self, token: DecodedJWT, cc_id: int) -> None:
        search_filter = {'id': cc_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        was_deleted = self.credit_card_service.delete(search_filter)
        if not was_deleted:
            raise ce.NotFound('Credit card not found', 'CREDIT_CARD_NOT_FOUND')
