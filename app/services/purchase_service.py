import logging

from app.schemas.expense_schemas import ExpenseRes
from app.schemas.payment_schemas import UpdatePurchasePaymentReq
from app.core.enums import ExpenseStatusEnum as ExpenseStatus
from app.core.enums import FINISHED_PAYMENT_STATUSES
from app.repositories import ExpenseRepository, PaymentRepository
from .expense_service import ExpenseService


logger = logging.getLogger(__name__)


class PurchaseService:
    def __init__(self):
        self.__expense_repo = None
        self.__payment_repo = None
        self.__expense_service = None

    @property
    def expense_repo(self):
        if self.__expense_repo is None:
            self.__expense_repo = ExpenseRepository()
        return self.__expense_repo

    @property
    def payment_repo(self):
        if self.__payment_repo is None:
            self.__payment_repo = PaymentRepository()
        return self.__payment_repo

    @property
    def expense_service(self):
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    def update(self, payment: UpdatePurchasePaymentReq, payment_id: int, purchase_search_filter: dict) -> ExpenseRes:
        purchase = self.expense_service.get_one(purchase_search_filter, True)
        if purchase is None:
            return
        # TODO 1: Si cambia month o year, solo sea actualiza el payment
        new_month = payment.month
        new_year = payment.year
        # TODO 2: Si cambia status y es a un estado final, verificar que el purhcase quede con estado 'finished', si no lo está, que quede con estado 'active'
        new_status = payment.status
        # TODO 3: Si cambia el monto, se deben cambiar los montos de todos los payments que no estén en estado final, si no hay ninguno, se debe actualizar el monto del purchase
        new_amount = payment.amount

        update_payment_data = {}
        update_purchase_data = {}

        if new_month is not None:
            update_payment_data['month'] = new_month
        if new_year is not None:
            update_payment_data['year'] = new_year
        if new_status is not None:
            update_payment_data['status'] = new_status
        if new_amount is not None:
            update_payment_data['amount'] = new_amount
        updated_payment = self.payment_repo.update(update_payment_data, {'id': payment_id, 'expense_id': purchase.id})

        if updated_payment is None:
            return

        if new_status is not None:
            self.__check_installments_status(purchase, new_status, update_purchase_data, payment_id)

        if new_amount is not None:
            self.__check_installments_amount(purchase, new_amount, update_purchase_data, payment_id)

        if update_purchase_data != {}:
            updated_purchase = self.expense_repo.update(update_purchase_data, purchase_search_filter)
            return ExpenseRes(**updated_purchase)
        return self.expense_service.get_one(purchase_search_filter, True)

    def __check_installments_status(self, purchase: ExpenseRes, new_status: str, purchase_data: dict, payment_id: int):
        purchase_must_finish = False
        for payment in purchase.payments:
            if payment.id == payment_id:
                status = new_status
            else:
                status = payment.status.value

            if status not in FINISHED_PAYMENT_STATUSES:
                break
        else:
            purchase_must_finish = True

        if (
            (purchase_must_finish and purchase.status != ExpenseStatus.FINISHED) or
            (not purchase_must_finish and purchase.status == ExpenseStatus.FINISHED)
        ):
            purchase_data['status'] = ExpenseStatus.FINISHED if purchase_must_finish else ExpenseStatus.ACTIVE

    def __check_installments_amount(self, purchase: ExpenseRes, new_amount: float, purchase_data: dict, payment_id: int):
        other_payments = tuple(payment for payment in purchase.payments if payment.id != payment_id)
        if all(payment.status.value in FINISHED_PAYMENT_STATUSES for payment in other_payments):
            purchase_data['amount'] = sum(
                payment.amount for payment in purchase.payments if payment.id != payment_id) + new_amount
            return
        remaining_amount = purchase.amount - new_amount
        remaining_installments = purchase.installments - 1

        for payment in other_payments:
            if payment.status.value in FINISHED_PAYMENT_STATUSES:
                remaining_amount -= payment.amount
                remaining_installments -= 1
                continue
            amount = round(remaining_amount / remaining_installments, 2)
            self.payment_repo.update({'amount': amount}, {'id': payment.id})
            remaining_amount -= amount
            remaining_installments -= 1
