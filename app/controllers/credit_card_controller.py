import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.credit_card_schemas import NewCreditCardReq, CreditCardReq, CreditCardRes
from app.schemas.expense_schemas import NewPurchaseReq, PurchaseReq, PurchaseRes
from app.schemas.expense_schemas import NewCCSubscriptionReq, CCSubscriptionReq, CCSubscriptionRes
from app.schemas.payment_schemas import PaymentReq, PaymentRes
from app.services.credit_card_service import CreditCardService
from app.services.expense_service import ExpenseService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
from app.core.enums.role_enum import RoleEnum as Role

logger = logging.getLogger(__name__)


class CreditCardController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__credit_card_service = None
        self.__expense_service = None
        self.__payment_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def expense_service(self) -> ExpenseService:
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service
    @property
    def payment_service(self) -> PaymentService:
        if self.__payment_service is None:
            self.__payment_service = PaymentService()
        return self.__payment_service

    def create(self, user_id: int, new_credit_card: NewCreditCardReq) -> CreditCardRes:
        try:
            self.user_service.get_by_id(user_id)

            credit_card_data = CreditCardReq(
                user_id=user_id,
                **new_credit_card.model_dump(exclude_none=True),
            )

            return self.credit_card_service.create(credit_card_data)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new credit card for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_all(self, user_id: int) -> List[CreditCardRes]:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_many(search_filter=search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting paginated credit cards for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_by_id(self, user_id: int, cc_id: int) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_by_id(cc_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update(self, user_id: int, cc_id: int, credit_card: CreditCardReq) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.update(cc_id, credit_card, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

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
            raise se.InternalServerError(ex.args)

    # !---------------------------------------------------! #
    # ! CREDIT CARD EXPENSES (Purchases and Subscriptions)! #
    # !---------------------------------------------------! #

    def create_new_purchase(self, user_id: int, cc_id: int, new_purchase_data: NewPurchaseReq):
        try:
            self.__check_permissions(user_id, cc_id)
            purchase_data = PurchaseReq(
                credit_card_id=cc_id,
                **new_purchase_data.model_dump(exclude_none=True),
            )
            # Create new purchase
            new_purchase_res = self.expense_service.create_purchase(purchase_data)

            # If ok, create installments without statement related
            if new_purchase_res.id:
                remaining_amount = new_purchase_res.total_amount
                remaining_installments = new_purchase_res.total_installments
                month = new_purchase_data.first_installment.month
                year = new_purchase_data.first_installment.year

                for installment_no in range(1, new_purchase_res.total_installments + 1):
                    installment_amount = round(remaining_amount/remaining_installments, 2)
                    new_installment = PaymentReq(
                        amount=installment_amount,
                        expense_id=new_purchase_res.id,
                        month=month,
                        year=year,
                        number=installment_no
                    )
                    self.payment_service.create(new_installment)

                    remaining_amount -= installment_amount
                    remaining_installments -= 1
                    year = (year + 1) if month == 12 else year
                    month = 1 if month == 12 else (month + 1)
            return new_purchase_res
        except BaseHTTPException as ex:
            logger.error(f'Error creating new purchase for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def create_new_subscription(self, user_id: int, cc_id: int, new_subscription_data: NewCCSubscriptionReq) -> CCSubscriptionRes:
        try:
            self.__check_permissions(user_id, cc_id)

            subscription_data = CCSubscriptionReq(
                credit_card_id=cc_id,
                **new_subscription_data.model_dump(exclude_none=True),
            )

            return self.expense_service.create_subscription(subscription_data)
        except BaseHTTPException as ex:
            logger.error(f'Error creating new subscription for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_all_purchases(self, user_id: int, cc_id: int) -> List[PurchaseRes]:
        try:
            self.__check_permissions(user_id, cc_id)

            search_filter = {'credit_card_id': cc_id}
            return self.expense_service.get_many_purchases(search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting purchases for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_all_subscriptions(self, user_id: int, cc_id: int) -> List[CCSubscriptionRes]:
        try:
            self.__check_permissions(user_id, cc_id)

            search_filter = {'credit_card_id': cc_id}
            return self.expense_service.get_many_subscriptions(search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting subscriptions for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_purchase_by_id(self, user_id: int, cc_id: int, purchase_id: int) -> PurchaseRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}

            return self.expense_service.get_purchase_by_id(purchase_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting purchase {purchase_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_subscription_by_id(self, user_id: int, cc_id: int, subscription_id: int) -> CCSubscriptionRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}

            return self.expense_service.get_subscription_by_id(subscription_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error getting subscription {subscription_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_purchase(self, user_id: int, cc_id: int, purchase_id: int, purchase: PurchaseReq) -> PurchaseRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.expense_service.update_purchase(purchase_id, purchase, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating purchase {purchase_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_subscription(self, user_id: int, cc_id: int, subscription_id: int, subscription: CCSubscriptionReq) -> CCSubscriptionRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.expense_service.update_subscription(subscription_id, subscription, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error updating subscription {subscription_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_purchase(self, user_id: int, cc_id: int, purchase_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            self.expense_service.delete_purchase(purchase_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error deleting purchase {purchase_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_subscription(self, user_id: int, cc_id: int, subscription_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            self.expense_service.delete_subscription(subscription_id, search_filter)
        except BaseHTTPException as ex:
            logger.error(f'Error deleting subscription {subscription_id} for credit card {cc_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    # ! Private methods

    def __check_permissions(self, user_id: int, cc_id: int) -> None:
        try:
            user = self.user_service.get_by_id(user_id)
            cc = self.credit_card_service.get_by_id(cc_id)

            if (cc.user_id != user.id and user.role != Role.ADMIN):
                raise ce.Forbidden(
                    'You have no permissions to add a subscription to this credit_card'
                )
        except BaseHTTPException as ex:
            raise ex
