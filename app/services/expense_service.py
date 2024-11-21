import logging
from typing import List

from app.repositories.expense_repository import ExpenseRepository as ExpenseRepo
from app.repositories.payment_repository import PaymentRepository as PaymentRepo
from app.schemas.expense_schemas import NewExpenseReq, ExpenseRes
from app.schemas.expense_schemas import UpdateExpenseReq
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.core.enums.expense_status_enum import ExpenseStatusEnum
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.payment_status_enum import PaymentStatusEnum, FINISHED_PAYMENT_STATUSES

logger = logging.getLogger(__name__)


class ExpenseService():
    def __init__(self) -> None:
        self.__repo: ExpenseRepo = None
        self.__payment_repo: PaymentRepo = None

    @property
    def repo(self) -> ExpenseRepo:
        if self.__repo is None:
            self.__repo = ExpenseRepo()
        return self.__repo

    @property
    def payment_repo(self) -> PaymentRepo:
        if self.__payment_repo is None:
            self.__payment_repo = PaymentRepo()
        return self.__payment_repo

    def create(self, user_id: int, new_expense: NewExpenseReq) -> ExpenseRes:
        try:
            new_expense_dict = new_expense.model_dump()
            new_expense_dict.update({'user_id': user_id})
            new_expense_res = self.repo.create(new_expense_dict)
            return self.get_by_id(new_expense_res.id)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, order_by: str = 'id', order_asc: bool = False, search_filter: dict = {}) -> List[ExpenseRes]:
        try:
            expenses = self.repo.get_many(
                search_filter=search_filter,
                order_by=order_by,
                order_asc=order_asc,
            )
            expense_list = [ExpenseRes.model_validate(expense) for expense in expenses]
            [self.update_expense_status(expense.id) for expense in expense_list]  # TODO: Delete in next release
            return expense_list

        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, expense_id: int, search_filter: dict = {}) -> ExpenseRes:
        try:
            search_filter.update(id=expense_id)
            expense = self.repo.get_one(search_filter)
            response = ExpenseRes.model_validate(expense)
            # return self.__update_expense_status(response)
            return response
        except re.NotFoundError as err:
            raise ce.NotFound(
                f'No expense was found with this creiteria: {search_filter}')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, expense_id: int, expense: UpdateExpenseReq):
        try:
            current = self.repo.get_one({'id': expense_id})
            recalc_installments = current.type == ExpenseTypeEnum.PURCHASE and current.amount != expense.amount
            updated_expense = self.repo.update(
                expense.model_dump(exclude_none=True), {'id': expense_id})

            response = ExpenseRes.model_validate(updated_expense)
            if recalc_installments:
                self.__update_payments_amount(response)
            return response
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def set_enable(self, expense_id: int, enabled: bool, from_endpoint: bool = True):
        try:
            expense = self.repo.get_one({'id': expense_id})
            if from_endpoint:
                self.__check_expense_type(ExpenseRes.model_validate(expense), ExpenseTypeEnum.SUBSCRIPTION)
            status = ExpenseStatusEnum.ACTIVE if enabled else ExpenseStatusEnum.FINISHED
            updated_expense = self.repo.update(
                {'status': status}, {'id': expense_id})
            return ExpenseRes.model_validate(updated_expense)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, expense_id: int):
        try:
            print('delete payments')
            self.repo.get_one({'id': expense_id})
            self.__delete_payments(expense_id)
            self.repo.delete(expense_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def __delete_payments(self, expense_id: int):
        payments = self.payment_repo.get_many(
            search_filter={'expense_id': expense_id})
        for payment in payments:
            self.payment_repo.delete(payment.id)

    def __check_expense_type(self, expense: ExpenseRes, expense_type: ExpenseTypeEnum):
        try:
            if expense.type != expense_type:
                raise ce.BadRequest(f'Expected type: {expense_type}')
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)

    def __update_payments_amount(self, updated_expense: ExpenseRes):
        remaining_amount = updated_expense.amount
        remaining_installments = updated_expense.installments
        for payment in updated_expense.payments:
            if payment.status != PaymentStatusEnum.UNCONFIRMED:
                remaining_amount -= payment.amount
                remaining_installments -= 1
                continue
            amount = round(remaining_amount/remaining_installments, 2)
            self.payment_repo.update({'amount': amount}, {'id': payment.id})
            remaining_amount -= amount
            remaining_installments -= 1

    def update_expense_status(self, expense_id: int) -> None:
        expense: ExpenseRes = self.get_by_id(expense_id)
        if expense.type != ExpenseTypeEnum.PURCHASE:
            return
        expense_status_must_be_active = True
        for payment in expense.payments:
            if payment.status not in FINISHED_PAYMENT_STATUSES:
                break
        else:
            expense_status_must_be_active = False
        if (
            (expense_status_must_be_active and expense.status != ExpenseStatusEnum.ACTIVE) or
            (not expense_status_must_be_active and expense.status == ExpenseStatusEnum.ACTIVE)
        ):
            expense = self.set_enable(expense.id, expense_status_must_be_active, False)
