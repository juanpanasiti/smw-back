import logging
from typing import List

from app.repositories.expense_repository import ExpenseRepository as ExpenseRepo
from app.schemas.expense_schemas import ExpenseReq, ExpenseRes
from app.schemas.expense_schemas import PurchaseReq, PurchaseRes
from app.schemas.expense_schemas import SubscriptionReq, SubscriptionRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce

logger = logging.getLogger(__name__)


class ExpenseService():
    def __init__(self) -> None:
        self.__repo: ExpenseRepo = None

    @property
    def repo(self) -> ExpenseRepo:
        if self.__repo is None:
            self.__repo = ExpenseRepo()
        return self.__repo

    def create(self, new_expense: ExpenseReq) -> ExpenseRes:
        try:
            new_expense_res = self.repo.create(new_expense.model_dump())
            return ExpenseRes.model_validate(new_expense_res)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many_purchases(self, search_filter: dict = {}) -> List[PurchaseRes]:
        try:
            search_filter.update(is_subscription=False)
            purchases = self.repo.get_many(search_filter=search_filter)
            return [PurchaseRes.model_validate(purchase) for purchase in purchases]
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

    def update_purchase(self, purchase_id: int, purchase: PurchaseReq, search_filter: dict = {}) -> PurchaseRes:
        try:
            search_filter.update(is_subscription=False, id=purchase_id)
            updated_purchase = self.repo.update(
                purchase.model_dump(exclude_none=True), search_filter)
            return PurchaseRes.model_validate(updated_purchase)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete_purchase(self, purchase_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(is_subscription=False, id=purchase_id)
            self.repo.get_one(search_filter)
            self.repo.delete(purchase_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many_subscriptions(self, search_filter: dict = {}) -> List[SubscriptionRes]:
        try:
            search_filter.update(is_subscription=True)
            subscriptions = self.repo.get_many(search_filter=search_filter)
            return [SubscriptionRes.model_validate(subscription) for subscription in subscriptions]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_subscription_by_id(self, subscription_id: int, search_filter: dict = {}) -> SubscriptionRes:
        try:
            search_filter.update(is_subscription=True, id=subscription_id)
            credit_card = self.repo.get_one(search_filter)
            return SubscriptionRes.model_validate(credit_card)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update_subscription(self, subscription_id: int, subscription: SubscriptionReq, search_filter: dict = {}) -> SubscriptionRes:
        try:
            search_filter.update(is_subscription=True, id=subscription_id)
            updated_subscription = self.repo.update(
                subscription.model_dump(exclude_none=True), search_filter)
            return SubscriptionRes.model_validate(updated_subscription)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete_subscription(self, subscription_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(is_subscription=True, id=subscription_id)
            self.repo.get_one(search_filter)
            self.repo.delete(subscription_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
