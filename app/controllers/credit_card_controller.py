import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.credit_card_schemas import CreditCardReq, CreditCardRes, CreditCardListParams
from app.services.credit_card_service import CreditCardService
from app.services.expense_service import ExpenseService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
from app.core.enums.role_enum import RoleEnum as Role

logger = logging.getLogger(__name__)


class CreditCardController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__credit_card_service = None
        self.__expense_service = None
        self.__payment_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def expense_service(self) -> ExpenseService:
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    @property
    def payment_service(self) -> PaymentService:
        if self.__payment_service is None:
            self.__payment_service = PaymentService()
        return self.__payment_service

    def create(self, user_id: int, new_credit_card: CreditCardReq) -> CreditCardRes:
        try:
            self.user_service.get_by_id(user_id)
            new_credit_card.user_id = user_id

            return self.credit_card_service.create(new_credit_card)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new credit card for user {
                         user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_all(self, user_id: int, params: CreditCardListParams) -> List[CreditCardRes]:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_many(
                search_filter=search_filter,
                order_by=params.order_by,
                order_asc=params.order_asc,
            )
        except BaseHTTPException as ex:
            logger.error(f'Error getting paginated credit cards for user {
                         user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_by_id(self, user_id: int, cc_id: int) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_by_id(cc_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting credit card {
                         cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update(self, user_id: int, cc_id: int, credit_card: CreditCardReq) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            credit_card.user_id = user_id
            return self.credit_card_service.update(cc_id, credit_card, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating credit card {
                         cc_id} for user {user_id}: {ex.description}'
                         )
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one(self, user_id: int, cc_id: int) -> None:
        try:
            search_filter = {'user_id': user_id}
            self.credit_card_service.delete(cc_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error deleting credit card {
                         cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    # ! Private methods

    def __check_permissions(self, user_id: int, cc_id: int) -> None:
        try:
            user = self.user_service.get_by_id(user_id)
            cc = self.credit_card_service.get_by_id(cc_id)

            if (cc.user_id != user.id and user.role != Role.ADMIN):
                raise ce.Forbidden(
                    'You have no permissions to add a subscription to this credit_card'
                )
        except BaseHTTPException as ex:
            raise ex
