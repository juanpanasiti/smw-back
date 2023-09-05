import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.payment_schemas import PaymentReq, PaymentRes
# from app.schemas.expense_schemas import NewPurchaseReq, PurchaseReq, PurchaseRes
# from app.schemas.expense_schemas import NewCCSubscriptionReq, CCSubscriptionReq, CCSubscriptionRes
# from app.schemas.payment_schemas import PaymentReq, PaymentRes
from app.services.payment_service import PaymentService
# from app.services.expense_service import ExpenseService
# from app.services.payment_service import PaymentService
# from app.services.user_service import UserService
from app.core.enums.status_enum import StatusEnum as Status

logger = logging.getLogger(__name__)


class PaymentController():
    def __init__(self) -> None:
        self.__payment_service = None

    @property
    def payment_service(self) -> PaymentService:
        if self.__payment_service is None:
            self.__payment_service = PaymentService()
        return self.__payment_service

    def create(self, payment: PaymentReq) -> PaymentRes:
        try:
            payment_data = PaymentReq(
                **payment.model_dump(exclude_none=True),
            )

            return self.payment_service.create(payment_data)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new payment: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_paginated(self, expense_id: int, limit: int, offset: int) -> List[PaymentRes]:
        try:
            search_filter = {'expense_id': expense_id}
            return self.payment_service.get_many(limit, offset, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting paginated payments for expense {expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_by_id(self, expense_id: int, payment_id: int) -> PaymentRes:
        try:
            search_filter = {'expense_id': expense_id}
            return self.payment_service.get_by_id(payment_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting payment {payment_id} for expense {expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update(self, expense_id: int, payment_id: int, payment: PaymentReq) -> PaymentRes:
        try:
            search_filter = {'expense_id': expense_id}
            return self.payment_service.update(payment_id, payment, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating payment {payment_id} for expense {expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one(self, expense_id: int, payment_id: int) -> None:
        try:
            search_filter = {'expense_id': expense_id}
            self.payment_service.delete(payment_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error deleting payment {payment_id} for expense {expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)
