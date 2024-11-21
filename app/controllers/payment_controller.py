import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.payment_schemas import PaymentReq, PaymentRes, NewPaymentReq, PaymentUpdateQueryParams
from app.services.payment_service import PaymentService
from app.services.expense_service import ExpenseService
from app.core.enums.payment_status_enum import PaymentStatusEnum as Status

logger = logging.getLogger(__name__)


class PaymentController():
    def __init__(self) -> None:
        self.__payment_service = None
        self.__expense_service = None

    @property
    def payment_service(self) -> PaymentService:
        if self.__payment_service is None:
            self.__payment_service = PaymentService()
        return self.__payment_service

    @property
    def expense_service(self) -> ExpenseService:
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    def create_subscription_payment(self, expense_id: int, payment: NewPaymentReq) -> PaymentRes:
        try:
            return self.payment_service.create_subscription_payment(expense_id, payment)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new payment: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_all(self, expense_id: int) -> List[PaymentRes]:
        try:
            self.expense_service.get_by_id(expense_id)
            search_filter = {'expense_id': expense_id}
            return self.payment_service.get_many(search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting paginated payments for expense {
                         expense_id}: {ex.description}')
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
            logger.error(f'Error getting payment {payment_id} for expense {
                         expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update(self, expense_id: int, payment_id: int, payment: PaymentReq, params: PaymentUpdateQueryParams) -> PaymentRes:
        try:
            search_filter = {'expense_id': expense_id}
            response = self.payment_service.update(payment_id, payment, search_filter)
            if payment.amount is not None and params.recalculate_amounts:
                self.__recalculate_payments_amount(expense_id, payment_id)
            self.expense_service.update_expense_status(expense_id)
            return response
        except BaseHTTPException as ex:
            logger.error(f'Error updating payment {payment_id} for expense {
                         expense_id}: {ex.description}')
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
            logger.error(f'Error deleting payment {payment_id} for expense {
                         expense_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def __recalculate_payments_amount(self, expense_id: int, payment_id: int) -> None:
        try:
            # TODO: Refactor
            # TODO: Only Purchases can recalculate payments
            total_amount = self.expense_service.get_by_id(expense_id).amount
            payments = self.get_all(expense_id)
            payments_ok = [payment for payment in payments if payment.status not in [
                Status.UNCONFIRMED] or payment.id == payment_id]
            payments_fix = [payment for payment in payments if payment.status in [
                Status.UNCONFIRMED] and payment.id != payment_id]
            payments_fix = sorted(
                payments_fix, key=lambda payment: payment.no_installment)
            remaining_amount = total_amount - \
                sum([payment.amount for payment in payments_ok])
            remaining_installments = len(payments_fix)
            for payment in payments_fix:
                payment.amount = remaining_amount / remaining_installments
                remaining_amount -= payment.amount
                remaining_installments -= 1
                self.payment_service.update(payment.id, payment)
        except ce.NotFound:
            logger.warn(f'Expense {expense_id} is not a purchase expense.')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
