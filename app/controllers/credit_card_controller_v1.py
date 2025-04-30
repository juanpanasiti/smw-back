import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.credit_card_schemas_v1 import CreditCardReqV1, CreditCardResV1, CreditCardListParamsV1
from app.services.credit_card_service_v1 import CreditCardServiceV1
from app.services.expense_service_v1 import ExpenseServiceV1
from app.services.payment_service_v1 import PaymentServiceV1
from app.services.user_service_v1 import UserServiceV1
from app.core.enums.role_enum import RoleEnum as Role

logger = logging.getLogger(__name__)


class CreditCardControllerV1():
    def __init__(self) -> None:
        self.__user_service = None
        self.__credit_card_service = None
        self.__expense_service = None
        self.__payment_service = None

    @property
    def credit_card_service(self) -> CreditCardServiceV1:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardServiceV1()
        return self.__credit_card_service

    @property
    def user_service(self) -> UserServiceV1:
        if self.__user_service is None:
            self.__user_service = UserServiceV1()
        return self.__user_service

    @property
    def expense_service(self) -> ExpenseServiceV1:
        if self.__expense_service is None:
            self.__expense_service = ExpenseServiceV1()
        return self.__expense_service

    @property
    def payment_service(self) -> PaymentServiceV1:
        if self.__payment_service is None:
            self.__payment_service = PaymentServiceV1()
        return self.__payment_service

    def create(self, user_id: int, new_credit_card: CreditCardReqV1) -> CreditCardResV1:
        try:
            self.user_service.get_by_id(user_id)
            new_credit_card.user_id = user_id

            return self.credit_card_service.create(new_credit_card)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new credit card for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'CREATE_CREDIT_CARD_UNHANDLED_ERROR')

    def get_all(self, user_id: int, params: CreditCardListParamsV1) -> List[CreditCardResV1]:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_many(
                search_filter=search_filter,
                order_by=params.order_by,
                order_asc=params.order_asc,
                expense_status=params.expense_status
            )
        except BaseHTTPException as ex:
            logger.error(f'Error getting paginated credit cards for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'GET_ALL_CREDIT_CARDS_UNHANDLED_ERROR')

    def get_by_id(self, user_id: int, cc_id: int) -> CreditCardResV1:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_by_id(cc_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'GET_CREDIT_CARD_BY_ID_UNHANDLED_ERROR')

    def update(self, user_id: int, cc_id: int, credit_card: CreditCardReqV1) -> CreditCardResV1:
        try:
            search_filter = {'user_id': user_id}
            credit_card.user_id = user_id
            return self.credit_card_service.update(cc_id, credit_card, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'UPDATE_CREDIT_CARD_UNHANDLED_ERROR')

    def delete_one(self, user_id: int, cc_id: int) -> None:
        try:
            search_filter = {'user_id': user_id}
            self.credit_card_service.delete(cc_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error deleting credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'DELETE_CREDIT_CARD_UNHANDLED_ERROR')

    # # ! Private methods

    # def __check_permissions(self, user_id: int, cc_id: int) -> None:
    #     try:
    #         user = self.user_service.get_by_id(user_id)
    #         cc = self.credit_card_service.get_by_id(cc_id)

    #         if (cc.user_id != user.id and user.role != Role.ADMIN):
    #             raise ce.Forbidden(
    #                 'You have no permissions to add a subscription to this credit_card'
    #             )
    #     except BaseHTTPException as ex:
    #         raise ex
