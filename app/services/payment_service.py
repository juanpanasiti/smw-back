import logging
from typing import List

from app.repositories.payment_repository import PaymentRepository as PaymentRepo
from app.repositories.expense_repository import ExpenseRepository as ExpenseRepo
from app.schemas.payment_schemas import PaymentReq, PaymentRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.core.enums.expense_type_enum import ExpenseTypeEnum

logger = logging.getLogger(__name__)


class PaymentService():
    def __init__(self) -> None:
        self.__repo: PaymentRepo = None
        self.__expense_repo: PaymentRepo = None

    @property
    def repo(self) -> PaymentRepo:
        if self.__repo is None:
            self.__repo = PaymentRepo()
        return self.__repo

    @property
    def expense_repo(self) -> ExpenseRepo:
        if self.__expense_repo is None:
            self.__expense_repo = ExpenseRepo()
        return self.__expense_repo

    def create(self, expense_id: int, new_payment: PaymentReq) -> PaymentRes:
        try:
            self.__check_expense_type(expense_id, ExpenseTypeEnum.SUBSCRIPTION)
            payment_dict = new_payment.model_dump()
            no_installment = self.__get_no_installment(expense_id)
            payment_dict.update(
                expense_id=expense_id,
                no_installment=no_installment
            )
            payment = self.repo.create(payment_dict)
            return PaymentRes.model_validate(payment)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, search_filter: dict = {}) -> List[PaymentRes]:
        try:
            payments = self.repo.get_many(search_filter=search_filter)
            return [PaymentRes.model_validate(payment) for payment in payments]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, payment_id: int, search_filter: dict = {}) -> PaymentRes:
        try:
            search_filter.update(id=payment_id)
            payment = self.repo.get_one(search_filter)
            return PaymentRes.model_validate(payment)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, payment_id: int, payment: PaymentReq, search_filter: dict = {}) -> PaymentRes:
        try:
            search_filter.update(id=payment_id)
            updated_payment = self.repo.update(
                payment.model_dump(exclude_none=True), search_filter
            )
            return PaymentRes.model_validate(updated_payment)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, payment_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(id=payment_id)
            self.repo.get_one(search_filter)
            self.repo.delete(payment_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def __check_expense_type(self, expense_id: int, expense_type: ExpenseTypeEnum):
        try:
            expense = self.expense_repo.get_by_id(expense_id)
            if expense.type != expense_type:
                raise ce.BadRequest(f'Expected type: {expense_type}')

        except re.NotFoundError as err:
            raise ce.NotFound(err.message)

    def __get_no_installment(self, expense_id: int) -> int:
        payments = self.repo.get_many(search_filter={'expense_id': expense_id})
        return len(payments) + 1
