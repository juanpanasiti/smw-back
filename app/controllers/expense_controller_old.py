import logging
from typing import List

from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import server_exceptions as se
from app.services.credit_card_service_old import CreditCardServiceOld
from app.services.expense_service_old import ExpenseServiceOld
from app.schemas.expense_schemas_old import NewExpenseReq, UpdateExpenseReq, ExpenseRes
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.payment_status_enum import PaymentStatusEnum
from app.exceptions import client_exceptions as ce
from app.schemas.payment_schemas_old import PaymentReq
from app.services.payment_service_old import PaymentServiceOld
from app.services.user_service_old import UserServiceOld
from app.core.enums.role_enum import RoleEnum as Role
from app.schemas.expense_schemas_old import ExpenseListParams

logger = logging.getLogger(__name__)


class ExpenseControllerOld():
    def __init__(self) -> None:
        self.__credit_card_service = None
        self.__expense_service = None
        self.__payment_service = None
        self.__user_service = None

    @property
    def credit_card_service(self) -> CreditCardServiceOld:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardServiceOld()
        return self.__credit_card_service

    @property
    def expense_service(self) -> ExpenseServiceOld:
        if self.__expense_service is None:
            self.__expense_service = ExpenseServiceOld()
        return self.__expense_service

    @property
    def payment_service(self) -> PaymentServiceOld:
        if self.__payment_service is None:
            self.__payment_service = PaymentServiceOld()
        return self.__payment_service

    @property
    def user_service(self) -> UserServiceOld:
        if self.__user_service is None:
            self.__user_service = UserServiceOld()
        return self.__user_service

    def get_all(self, user_id: int, params: ExpenseListParams) -> List[ExpenseRes]:
        try:
            response = []
            search_filter_cc = {'user_id': user_id}

            credit_cards = self.credit_card_service.get_many(
                search_filter=search_filter_cc
            )

            for credit_card in credit_cards:
                # TODO: refactor
                search_filter = {'account_id': credit_card.id}
                if params.type is not None:
                    search_filter.update(type=params.type)
                if params.status is not None:
                    search_filter.update(status=params.status)
                partial = self.expense_service.get_many(
                    search_filter=search_filter,
                    order_by=params.order_by,
                    order_asc=params.order_asc,
                )
                response.extend(partial)

            return response
        except BaseHTTPException as ex:
            logger.error(
                f'Error getting expenses for user {user_id}: {ex.description}'
            )
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'GET_EXPENSES_UNHANDLED_ERROR')

    def create(self, user_id: int, new_expense: NewExpenseReq) -> ExpenseRes:
        try:
            self.__check_permissions(user_id, new_expense.account_id)
            new_expense_res = self.expense_service.create(user_id, new_expense)
            if (new_expense.type == ExpenseTypeEnum.PURCHASE):
                self.__create_new_purchase_installments(new_expense_res)
            else:
                self.__create_new_subscription_installments(new_expense_res)
            return new_expense_res
        except BaseHTTPException as ex:
            logger.error(f'Error creating new purchase for credit card {
                         new_expense.account_id} for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args, 'CREATE_EXPENSE_UNHANDLED_ERROR')

    def get_by_id(self, expense_id: int) -> ExpenseRes:
        return self.expense_service.get_by_id(expense_id)

    def update(self, expense_id: int, expense: UpdateExpenseReq) -> ExpenseRes:
        return self.expense_service.update(expense_id, expense)

    def disable(self, expense_id: int):
        self.expense_service.set_enable(expense_id, False)

    def enable(self, expense_id: int):
        self.expense_service.set_enable(expense_id, True)

    def delete(self, expense_id: int):
        self.expense_service.delete(expense_id)

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
                self.payment_service.create(new_purchase.id, new_installment)
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
        self.payment_service.create(new_subscription.id, new_installment)

    def __check_permissions(self, user_id: int, cc_id: int) -> None:
        try:
            user = self.user_service.get_by_id(user_id)
            cc = self.credit_card_service.get_by_id(cc_id)

            if (cc.user_id != user.id and user.role != Role.ADMIN):
                raise ce.Forbidden(
                    message='You have no permissions to add a subscription to this credit_card',
                    exception_code='EXPENSE_FORBIDDEN_ERROR'
                )
        except BaseHTTPException as ex:
            raise ex
