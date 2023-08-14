import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.credit_card_schemas import NewCreditCardReq, CreditCardReq, CreditCardRes
from app.schemas.credit_card_expense_schemas import NewCCPurchaseReq, CCPurchaseReq, CCPurchaseRes
from app.schemas.credit_card_expense_schemas import NewCCSubscriptionReq, CCSubscriptionReq, CCSubscriptionRes
from app.schemas.credit_card_statement_schemas import NewCCStatementReq, CCStatementReq, CCStatementRes
from app.schemas.statement_item_schemas import NewStatementItemReq, StatementItemReq, StatementItemRes
from app.services.credit_card_service import CreditCardService
from app.services.credit_card_expense_service import CreditCardExpenseService as CCExpenseService
from app.services.credit_card_statement_service import CreditCardStatementService as CCStatementService
from app.services.statement_item_service import StatementItemService as SItemService
from app.services.user_service import UserService
from app.core.enums.role_enum import RoleEnum as Role

logger = logging.getLogger(__name__)


class CreditCardController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__credit_card_service = None
        self.__cc_expense_service = None
        self.__cc_statement_service = None
        self.__statement_item_service = None

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
    def cc_expense_service(self) -> CCExpenseService:
        if self.__cc_expense_service is None:
            self.__cc_expense_service = CCExpenseService()
        return self.__cc_expense_service

    @property
    def cc_statement_service(self) -> CCStatementService:
        if self.__cc_statement_service is None:
            self.__cc_statement_service = CCStatementService()
        return self.__cc_statement_service

    @property
    def statement_item_service(self) -> SItemService:
        if self.__statement_item_service is None:
            self.__statement_item_service = SItemService()
        return self.__statement_item_service

    def create(self, user_id: int, new_credit_card: NewCreditCardReq) -> CreditCardRes:
        try:
            self.user_service.get_by_id(user_id)

            credit_card_data = CreditCardReq(
                user_id=user_id,
                **new_credit_card.model_dump(exclude_none=True),
            )

            return self.credit_card_service.create(credit_card_data)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_paginated(self, user_id: int, limit: int, offset: int) -> List[CreditCardRes]:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_many(limit, offset, search_filter)
        except BaseHTTPException as ex:
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
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    # !---------------------------------------------------! #
    # ! CREDIT CARD EXPENSES (Purchases and Subscriptions)! #
    # !---------------------------------------------------! #

    def create_new_purchase(self, user_id: int, cc_id: int, new_purchase_data: NewCCPurchaseReq):
        try:
            self.__check_permissions(user_id, cc_id)
            purchase_data = CCPurchaseReq(
                credit_card_id=cc_id,
                **new_purchase_data.model_dump(exclude_none=True),
            )
            # Create new purchase
            new_purchase_res = self.cc_expense_service.create_purchase(purchase_data)

            # If ok, create installments without statement related
            if new_purchase_res.id:
                remaining_amount = new_purchase_res.total_amount
                remaining_installments = new_purchase_res.total_installments

                for installment_no in range(1, new_purchase_res.total_installments + 1):
                    installment_amount = round(remaining_amount/remaining_installments, 2)
                    new_installment = StatementItemReq(
                        installment_no=installment_no,
                        cc_expense_id=new_purchase_res.id,
                        cc_statement_id=None,
                        amount=installment_amount,
                    )
                    self.statement_item_service.create(new_installment)
                    remaining_amount -= installment_amount
                    remaining_installments -= 1
            return new_purchase_res
        except BaseHTTPException as ex:
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

            return self.cc_expense_service.create_subscription(subscription_data)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_purchases_paginated(self, user_id: int, cc_id: int, limit: int, offset: int) -> List[CCPurchaseRes]:
        try:
            self.__check_permissions(user_id, cc_id)

            search_filter = {'credit_card_id': cc_id}
            return self.cc_expense_service.get_many_purchases(limit, offset, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_subscriptions_paginated(self, user_id: int, cc_id: int, limit: int, offset: int) -> List[CCSubscriptionRes]:
        try:
            self.__check_permissions(user_id, cc_id)

            search_filter = {'credit_card_id': cc_id}
            return self.cc_expense_service.get_many_subscriptions(limit, offset, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_purchase_by_id(self, user_id: int, cc_id: int, purchase_id: int) -> CCPurchaseRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}

            return self.cc_expense_service.get_purchase_by_id(purchase_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_subscription_by_id(self, user_id: int, cc_id: int, subscription_id: int) -> CCSubscriptionRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}

            return self.cc_expense_service.get_subscription_by_id(subscription_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_purchase(self, user_id: int, cc_id: int, purchase_id: int, purchase: CCPurchaseReq) -> CCPurchaseRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.cc_expense_service.update_purchase(purchase_id, purchase, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_subscription(self, user_id: int, cc_id: int, subscription_id: int, subscription: CCSubscriptionReq) -> CCSubscriptionRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.cc_expense_service.update_subscription(subscription_id, subscription, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_purchase(self, user_id: int, cc_id: int, purchase_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            self.cc_expense_service.delete_purchase(purchase_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_subscription(self, user_id: int, cc_id: int, subscription_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            self.cc_expense_service.delete_subscription(subscription_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    # !-----------------------------------------! #
    # ! CREDIT CARD Statements and Installments ! #
    # !-----------------------------------------! #

    def create_new_statement(self, user_id: int, cc_id: int, new_statement: NewCCStatementReq) -> CCStatementRes:
        try:
            self.__check_permissions(user_id, cc_id)
            response = self.cc_statement_service.create(
                CCStatementReq(
                    credit_card_id=cc_id,
                    **new_statement.model_dump(exclude_none=True),
                )
            )

            return response
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_statements_paginated(self, user_id: int, cc_id: int, limit: int, offset: int) -> List[CCStatementRes]:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.cc_statement_service.get_many(limit, offset, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_statement_by_id(self, user_id: int, cc_id: int, statement_id: int) -> CCStatementRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            return self.cc_statement_service.get_by_id(statement_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_statement(self, user_id: int, cc_id: int, statement_id: int, statement: CCStatementReq) -> CCStatementRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}

            response = self.cc_statement_service.update(statement_id, statement, search_filter)
            if statement.date_from is not None or statement.date_to is not None:
                # TODO: Check statement items (installments)
                pass

            return response
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_statement(self, user_id: int, cc_id: int, statement_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'credit_card_id': cc_id}
            self.cc_statement_service.delete(statement_id, search_filter)
            # TODO: Delete installments
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def create_new_installment(self, user_id: int, cc_id: int, statement_id: int, new_item: NewStatementItemReq) -> StatementItemRes:
        try:
            self.__check_permissions(user_id, cc_id)

            response = self.statement_item_service.create(StatementItemReq(
                cc_statement_id=statement_id,
                **new_item.model_dump(exclude_none=True),
            ))

            return response
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    # def get_installments_paginated(self, user_id: int, cc_id: int,statement_id: int, limit: int, offset: int) -> List[StatementItemRes]:
    #     try:
    #         self.__check_permissions(user_id, cc_id)
    #         search_filter = {'cc_statement_id': cc_id}
    #         return self.cc_statement_service.get_many(limit, offset, search_filter)
    #     except BaseHTTPException as ex:
    #         raise ex
    #     except Exception as ex:
    #         logger.error(type(ex))
    #         logger.critical(ex.args)
    #         raise se.InternalServerError(ex.args)

    def get_installment_by_id(self, user_id: int, cc_id: int, statement_id: int, item_id: int) -> StatementItemRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'cc_statement_id': statement_id}
            return self.statement_item_service.get_by_id(item_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update_installment(self, user_id: int, cc_id: int, statement_id: int, item_id: int, item: StatementItemReq) -> StatementItemRes:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'cc_statement_id': statement_id}

            response = self.statement_item_service.update(item_id, item, search_filter)
            return response
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one_installment(self, user_id: int, cc_id: int, statement_id: int, item_id: int) -> None:
        try:
            self.__check_permissions(user_id, cc_id)
            search_filter = {'cc_statement_id': statement_id}
            self.cc_statement_service.delete(item_id, search_filter)
        except BaseHTTPException as ex:
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
