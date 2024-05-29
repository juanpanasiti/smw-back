import logging
from typing import List

from app.repositories.expense_repository import ExpenseRepository as ExpenseRepo
from app.schemas.expense_schemas import NewExpenseReq, ExpenseRes
from app.schemas.expense_schemas import PurchaseReq, UpdateExpenseReq, PurchaseRes
from app.schemas.expense_schemas import SubscriptionReq, SubscriptionRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.core.enums.expense_status_enum import ExpenseStatusEnum
from app.core.enums.expense_type_enum import ExpenseTypeEnum

logger = logging.getLogger(__name__)


class ExpenseService():
    def __init__(self) -> None:
        self.__repo: ExpenseRepo = None

    @property
    def repo(self) -> ExpenseRepo:
        if self.__repo is None:
            self.__repo = ExpenseRepo()
        return self.__repo

    def create(self, new_expense: NewExpenseReq) -> ExpenseRes:
        try:
            new_expense_res = self.repo.create(new_expense.model_dump())
            return ExpenseRes.model_validate(new_expense_res)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, search_filter: dict = {}) -> List[ExpenseRes]:
        try:
            expenses = self.repo.get_many(search_filter=search_filter)
            return [ExpenseRes.model_validate(expense) for expense in expenses]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, expense_id: int, search_filter: dict = {}) -> ExpenseRes:
        try:
            search_filter.update(id=expense_id)
            expense = self.repo.get_one(search_filter)
            return ExpenseRes.model_validate(expense)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_purchase_by_id(self, purchase_id: int, search_filter: dict = {}) -> PurchaseRes:
        try:
            search_filter.update(is_subscription=False, id=purchase_id)
            purchase = self.repo.get_one(search_filter)
            return PurchaseRes.model_validate(purchase)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, expense_id: int, expense: UpdateExpenseReq):
        try:
            self.repo.get_one({'id': expense_id})
            updated_expense = self.repo.update(
                expense.model_dump(exclude_none=True), {'id': expense_id})
            return ExpenseRes.model_validate(updated_expense)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def set_enable(self, expense_id: int, enabled: bool):
        try:
            expense = self.repo.get_one({'id': expense_id})
            self.__check_expense_type(ExpenseRes.model_validate(expense), ExpenseTypeEnum.SUBSCRIPTION)
            status = ExpenseStatusEnum.ACTIVE if enabled else ExpenseStatusEnum.FINISHED
            updated_expense = self.repo.update({'status': status}, {'id': expense_id})
            return ExpenseRes.model_validate(updated_expense)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def __check_expense_type(self, expense: ExpenseRes, expense_type: ExpenseTypeEnum):
        try:
            if expense.type != expense_type:
                raise ce.BadRequest(f'Expected type: {expense_type}')
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)