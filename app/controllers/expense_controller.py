import logging
from typing import List

from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import server_exceptions as se
from app.services.credit_card_service import CreditCardService
from app.services.expense_service import ExpenseService
from app.schemas.expense_schemas import NewExpenseReq, ExpenseRes
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.payment_status_enum import PaymentStatusEnum
from app.exceptions import client_exceptions as ce
from app.schemas.payment_schemas import PaymentReq
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
from app.core.enums.role_enum import RoleEnum as Role
from app.schemas.query_params_schemas import ExpenseListParams

logger = logging.getLogger(__name__)


class ExpenseController():
    def __init__(self) -> None:
        self.__credit_card_service = None
        self.__expense_service = None
        self.__payment_service = None
        self.__user_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

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

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    def get_all(self, user_id: int, params: ExpenseListParams) -> List[ExpenseRes]:
        try:
            response = []
            search_filter_cc = {'user_id': user_id}

            credit_cards = self.credit_card_service.get_many(
                search_filter=search_filter_cc)

            for credit_card in credit_cards:
                search_filter = {'credit_card_id': credit_card.id}
                if params.type is not None:
                    search_filter.update(type=params.type)
                partial = self.expense_service.get_many(
                    search_filter=search_filter)
                response.extend(partial)

            return response
        except BaseHTTPException as ex:
            logger.error(f'Error getting expenses for user {
                         user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def create(self, user_id: int, new_expense: NewExpenseReq) -> ExpenseRes:
        try:
            self.__check_permissions(user_id, new_expense.credit_card_id)
            new_expense.user_id = user_id
            new_expense_res = self.expense_service.create(new_expense)
            if (new_expense.type == ExpenseTypeEnum.PURCHASE):
                self.__create_new_purchase_installments(new_expense_res)
            else:
                self.__create_new_subscription_installments(new_expense_res)
            return new_expense_res
        except BaseHTTPException as ex:
            logger.error(f'Error creating new purchase for credit card {
                         new_expense.credit_card_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_by_id(self, expense_id: int) -> ExpenseRes:
        return self.expense_service.get_by_id(expense_id)

    def __create_new_purchase_installments(self, new_purchase: ExpenseRes):
        if new_purchase.id:
            remaining_amount = new_purchase.amount
            remaining_installments = new_purchase.installments
            month = new_purchase.first_payment_date.month
            year = new_purchase.first_payment_date.year
            for no_installment in range(1, new_purchase.installments + 1):
                installment_amount = round(
                    remaining_amount/remaining_installments, 2)
                new_installment = PaymentReq(
                    amount=installment_amount,
                    expense_id=new_purchase.id,
                    month=month,
                    year=year,
                    no_installment=no_installment,
                    status=PaymentStatusEnum.UNCONFIRMED
                )
                self.payment_service.create(new_installment)
                remaining_amount -= installment_amount
                remaining_installments -= 1
                year = (year + 1) if month == 12 else year
                month = 1 if month == 12 else (month + 1)

    def __create_new_subscription_installments(self, new_subscription: ExpenseRes):
        new_installment = PaymentReq(
            amount=new_subscription.amount,
            expense_id=new_subscription.id,
            month=new_subscription.first_payment_date.month,
            year=new_subscription.first_payment_date.year,
            status=PaymentStatusEnum.UNCONFIRMED,
            no_installment=1
        )
        self.payment_service.create(new_installment)

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
