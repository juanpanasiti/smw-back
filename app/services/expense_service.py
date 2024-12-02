import logging
from typing import List

from app.schemas.expense_schemas import NewExpenseReq, UpdateExpenseReq, ExpenseRes, ExpenseListParam
from app.schemas.payment_schemas import NewPaymentReq, UpdatePaymentReq
from app.core.enums import ExpenseTypeEnum
from app.core.enums import PaymentStatusEnum as PaymentStatus, FINISHED_PAYMENT_STATUSES
from app.repositories import ExpenseRepository
from .payment_service import PaymentService


logger = logging.getLogger(__name__)


class ExpenseService:
    def __init__(self):
        self.__expense_repo = None
        self.__payment_service = None

    @property
    def expense_repo(self):
        if self.__expense_repo is None:
            self.__expense_repo = ExpenseRepository()
        return self.__expense_repo

    @property
    def payment_service(self):
        if self.__payment_service is None:
            self.__payment_service = PaymentService()
        return self.__payment_service

    def create(self, new_expense: NewExpenseReq) -> ExpenseRes:
        if new_expense.type == ExpenseTypeEnum.SUBSCRIPTION:
            new_expense.installments = 1

        new_expense_dict = new_expense.model_dump()
        expense_dict = self.expense_repo.create(new_expense_dict)
        expense_res = ExpenseRes(**expense_dict)
        self.__create_installments(expense_res)
        return expense_res

    def get_list(self, user_id: int | None, account_id: int | None, params: ExpenseListParam) -> List[ExpenseRes]:
        params_dict = params.model_dump(exclude_none=True)
        if params.order_by is not None:
            params_dict['order_by'] = params.order_by.value
        if user_id is not None:
            params_dict['user_id'] = user_id
        if account_id is not None:
            params_dict['account_id'] = account_id
        expenses = self.expense_repo.get_many(**params_dict)
        return [ExpenseRes(**expense) for expense in expenses]

    def get_one(self, search_filter: dict, include_relationships: bool) -> ExpenseRes | None:
        expense = self.expense_repo.get_one(search_filter, include_relationships)
        return ExpenseRes(**expense) if expense else None

    def update(self, expense: UpdateExpenseReq, search_filter: dict) -> ExpenseRes | None:
        new_data = expense.model_dump(exclude_none=True)
        updated_expense = self.expense_repo.update(new_data, search_filter)
        expense_res = ExpenseRes(**updated_expense)
        if expense.amount is not None and expense.amount != expense_res.amount:
            self.__update_installments_amount(expense_res)
        return expense_res

    def delete(self, search_filter: dict) -> bool:
        self.payment_service.delete({'expense_id': search_filter['id']})
        return self.expense_repo.delete(search_filter)

    def __create_installments(self, expense: ExpenseRes):
        remaining_amount = expense.amount
        remaining_installments = expense.installments
        month = expense.first_payment_date.month
        year = expense.first_payment_date.year
        for no_installment in range(1, expense.installments + 1):
            installment_amount = round(remaining_amount / remaining_installments, 2)
            new_payment = NewPaymentReq(
                amount=installment_amount,
                no_installment=no_installment,
                month=month,
                year=year,
                expense_id=expense.id,
            )
            payment = self.payment_service.create(new_payment, PaymentStatus.UNCONFIRMED)
            expense.payments.append(payment)
            remaining_amount -= installment_amount
            remaining_installments -= 1
            month, year = self.__calc_next_period(month, year)
    
    def __update_installments_amount(self, expense: ExpenseRes):
        remaining_amount = expense.amount
        remaining_installments = expense.installments
        for payment in expense.payments:
            if payment.status not in FINISHED_PAYMENT_STATUSES:
                new_payment_amount = round(remaining_amount / remaining_installments, 2)
                payment.amount = new_payment_amount
                self.payment_service.update(UpdatePaymentReq(amount=new_payment_amount), {'id': payment.id})
            remaining_amount -= payment.amount
            remaining_installments -= 1

    def __calc_next_period(self, month: int, year: int) -> tuple[int, int]:
        year = year + 1 if month == 12 else year
        month = 1 if month == 12 else month + 1
        return month, year
