import logging

from app.repositories.credit_card_repository_old import CreditCardRepositoryOld
from app.services.expense_service_old import ExpenseServiceOld
from app.schemas.credit_card_schemas_old import CreditCardReq, CreditCardRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.core.enums.expense_status_enum import ExpenseStatusEnum


logger = logging.getLogger(__name__)


class CreditCardServiceOld():
    def __init__(self) -> None:
        self.__repo: CreditCardRepositoryOld = None
        self.__expense_service: ExpenseServiceOld = None

    @property
    def repo(self) -> CreditCardRepositoryOld:
        if self.__repo is None:
            self.__repo = CreditCardRepositoryOld()
        return self.__repo

    @property
    def expense_service(self) -> ExpenseServiceOld:
        if self.__expense_service is None:
            self.__expense_service = ExpenseServiceOld()
        return self.__expense_service

    def create(self, new_credit_card: CreditCardReq) -> CreditCardRes:
        try:
            self._check_main_credit_card(new_credit_card)
            credit_card = self.repo.create(new_credit_card.model_dump())
            return CreditCardRes.model_validate(credit_card)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(
        self,
            order_by: str = 'id',
            order_asc: bool = False,
            limit: int | None = None,
            offset: int | None = None,
            search_filter: dict = {},
            expense_status: ExpenseStatusEnum = None
    ):
        try:
            credit_cards = self.repo.get_many(
                limit,
                offset,
                search_filter,
                order_by=order_by,
                order_asc=order_asc,
            )
            credit_cards_res = [CreditCardRes.model_validate(cc) for cc in credit_cards]
            for credit_card in credit_cards_res:
                self.__filter_expenses_by_status(credit_card, expense_status)
            return credit_cards_res
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, cc_id: int, search_filter: dict = {}) -> CreditCardRes:
        try:
            search_filter.update(id=cc_id)
            credit_card = self.repo.get_one(search_filter)
            return CreditCardRes.model_validate(credit_card)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message, 'CREDIT_CARD_NOT_FOUND')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, cc_id: int, credit_card: CreditCardReq, search_filter: dict = {}) -> CreditCardRes:
        try:
            search_filter.update(id=cc_id)
            self._check_main_credit_card(credit_card)
            updated_cc = self.repo.update(
                credit_card.model_dump(exclude_none=True), search_filter)
            return CreditCardRes.model_validate(updated_cc)
        except re.NotFoundError as err:
            ce.NotFound(err.message, 'CREDIT_CARD_NOT_FOUND')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, cc_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(id=cc_id)
            self.repo.get_one(search_filter)
            self.__delete_expenses_related(cc_id)
            self.__delete_extensions_related(cc_id)
            self.repo.delete(cc_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message, 'CREDIT_CARD_NOT_FOUND')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def __delete_expenses_related(self, id):
        expenses = self.expense_service.get_many(
            search_filter={'account_id': id}
        )
        for expense in expenses:
            self.expense_service.delete(expense.id)

    def __delete_extensions_related(self, id):
        extensions = self.repo.get_many(
            search_filter={'main_credit_card_id': id}
        )
        for extension in extensions:
            self.delete(extension.id)

    def _check_main_credit_card(self, credit_card: CreditCardReq):
        if credit_card.main_credit_card_id is not None:
            # HINT: This credit card is an extension
            main_cc = self.get_by_id(credit_card.main_credit_card_id)
            if main_cc.main_credit_card_id is not None:
                raise ce.BadRequest(
                    message='You cannot assign a main credit card that is already an extension.',
                    exception_code='CREDIT_CARD_EXTENSION_CANT_BE_MAIN'
                )
            credit_card.limit = main_cc.limit
            credit_card.next_closing_date = main_cc.next_closing_date
            credit_card.next_expiring_date = main_cc.next_expiring_date

    def __filter_expenses_by_status(self, credit_card: CreditCardRes, expense_status: ExpenseStatusEnum) -> None:
        if not expense_status:
            return

        credit_card.expenses = [expense for expense in credit_card.expenses if expense.status == expense_status]
