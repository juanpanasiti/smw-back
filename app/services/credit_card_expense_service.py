import logging
from typing import List

from app.repositories.credit_card_expense_repository import CreditCardExpenseRepository as CCExpenseRepo
from app.schemas.credit_card_expense_schemas import CCPurchaseReq, CCPurchaseRes
from app.schemas.credit_card_expense_schemas import CCSubscriptionReq, CCSubscriptionRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce

logger = logging.getLogger(__name__)


class CreditCardExpenseService():
    def __init__(self) -> None:
        self.__repo: CCExpenseRepo = None

    @property
    def repo(self) -> CCExpenseRepo:
        if self.__repo is None:
            self.__repo = CCExpenseRepo()
        return self.__repo

    def create_purchase(self, new_purchase: CCPurchaseReq) -> CCPurchaseRes:
        try:
            purchase_dict = new_purchase.model_dump()
            purchase_dict.update(is_subscription=False, is_active=True)
            purchase = self.repo.create(purchase_dict)
            return CCPurchaseRes.model_validate(purchase)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many_purchases(self, limit: int, offset: int, search_filter: dict = {}) -> List[CCPurchaseRes]:
        try:
            search_filter.update(is_subscription=False)
            purchases = self.repo.get_many(limit, offset, search_filter)
            return [CCPurchaseRes.model_validate(purchase) for purchase in purchases]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_purchase_by_id(self, purchase_id: int, search_filter: dict = {}) -> CCPurchaseRes:
        try:
            search_filter.update(is_subscription=False, id=purchase_id)
            credit_card = self.repo.get_one(search_filter)
            return CCPurchaseRes.model_validate(credit_card)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update_purchase(self, purchase_id: int, purchase: CCPurchaseReq, search_filter: dict = {}) -> CCPurchaseRes:
        try:
            search_filter.update(is_subscription=False, id=purchase_id)
            updated_purchase = self.repo.update(
                purchase.model_dump(exclude_none=True), search_filter)
            return CCPurchaseRes.model_validate(updated_purchase)
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

    def create_subscription(self, new_subscription: CCSubscriptionReq) -> CCSubscriptionRes:
        try:
            subscription_dict = new_subscription.model_dump()
            subscription_dict.update(is_subscription=True)
            subscription = self.repo.create(subscription_dict)
            return CCSubscriptionRes.model_validate(subscription)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many_subscriptions(self, limit: int, offset: int, search_filter: dict = {}) -> List[CCSubscriptionRes]:
        try:
            search_filter.update(is_subscription=True)
            subscriptions = self.repo.get_many(limit, offset, search_filter)
            return [CCSubscriptionRes.model_validate(subscription) for subscription in subscriptions]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_subscription_by_id(self, subscription_id: int, search_filter: dict = {}) -> CCSubscriptionRes:
        try:
            search_filter.update(is_subscription=True, id=subscription_id)
            credit_card = self.repo.get_one(search_filter)
            return CCSubscriptionRes.model_validate(credit_card)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update_subscription(self, subscription_id: int, subscription: CCSubscriptionReq, search_filter: dict = {}) -> CCSubscriptionRes:
        try:
            search_filter.update(is_subscription=True, id=subscription_id)
            updated_subscription = self.repo.update(
                subscription.model_dump(exclude_none=True), search_filter)
            return CCSubscriptionRes.model_validate(updated_subscription)
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
