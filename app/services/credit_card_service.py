import logging
from typing import List

from app.repositories import CreditCardRepository, ExpenseRepository
from app.exceptions import client_exceptions as ce
from app.schemas.credit_card_schemas import NewCreditCardReq, UpdateCreditCardReq, CreditCardRes, CreditCardListParam
from app.services import ExpenseService


logger = logging.getLogger(__name__)


class CreditCardService():
    def __init__(self) -> None:
        self.__credit_card_repo: CreditCardRepository = None
        self.__expense_repo: ExpenseService = None
        self.__expense_service: ExpenseRepository = None

    @property
    def credit_card_repo(self) -> CreditCardRepository:
        if self.__credit_card_repo is None:
            self.__credit_card_repo = CreditCardRepository()
        return self.__credit_card_repo

    @property
    def expense_service(self) -> ExpenseService:
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    @property
    def expense_repo(self) -> ExpenseRepository:
        if self.__expense_repo is None:
            self.__expense_repo = ExpenseRepository()
        return self.__expense_repo

    def create(self, new_credit_card: NewCreditCardReq) -> CreditCardRes:
        if new_credit_card.main_credit_card_id is not None:
            main_cc: CreditCardRes = self._check_main_credit_card(
                new_credit_card.main_credit_card_id, new_credit_card.user_id)
            new_credit_card.limit = main_cc.limit
            new_credit_card.next_closing_date = main_cc.next_closing_date
            new_credit_card.next_expiring_date = main_cc.next_expiring_date
        credit_card = self.credit_card_repo.create(new_credit_card.model_dump())
        return CreditCardRes(**credit_card)

    def get_list(self, user_id: int, params: CreditCardListParam) -> List[CreditCardRes]:
        params_dict = params.model_dump()
        if params.order_by is not None:
            params_dict['order_by'] = params.order_by.value
        credit_cards = self.credit_card_repo.get_many(user_id=user_id, **params_dict)
        return [CreditCardRes(**credit_card) for credit_card in credit_cards]

    def get_one(self, search_filter: dict = {}) -> CreditCardRes | None:
        credit_card = self.credit_card_repo.get_one(search_filter)
        if not credit_card:
            return None
        return CreditCardRes(**credit_card)

    def update(self, credit_card: UpdateCreditCardReq, search_filter: dict = {}) -> CreditCardRes:
        if credit_card.main_credit_card_id is not None:
            user_id = self._get_user_id(credit_card, search_filter)
            if user_id is None:
                return None
            self._check_main_credit_card(credit_card.main_credit_card_id, user_id)
        new_data = credit_card.model_dump(exclude_none=True)
        updated_cc = self.credit_card_repo.update(new_data, search_filter)
        return CreditCardRes(**updated_cc)

    def delete(self, search_filter: dict) -> bool:
        self.credit_card_repo.get_one(search_filter)
        self.__delete_expenses_related(search_filter['id'])
        self.__delete_extensions_related(search_filter['id'])
        return self.credit_card_repo.delete(search_filter['id'])

    def __delete_expenses_related(self, id):
        expenses = self.expense_repo.get_many(account_id=id)
        for expense in expenses:
            self.expense_service.delete({'id': expense['id']})

    def __delete_extensions_related(self, id):
        extensions = self.credit_card_repo.get_many(main_credit_card_id=id)
        for extension in extensions:
            self.delete({'id': extension['id']})

    def _check_main_credit_card(self, main_credit_card_id: int, user_id: int) -> CreditCardRes:
        main_cc = self.get_one({'id': main_credit_card_id, 'user_id': user_id})
        if main_cc is not None and main_cc.main_credit_card_id is not None:
            raise ce.BadRequest('You cannot assign a main credit card that is already an extension.')
        return main_cc

    def _get_user_id(self, credit_card: UpdateCreditCardReq, search_filter: dict) -> int | None:
        if credit_card.user_id is not None:
            return credit_card.user_id
        current_cc = self.get_one(search_filter)
        return current_cc.user_id if current_cc else None
    # def __filter_expenses_by_status(self, credit_card: CreditCardRes, expense_status: ExpenseStatusEnum) -> None:
    #     if not expense_status:
    #         return

    #     credit_card.expenses = [expense for expense in credit_card.expenses if expense.status == expense_status]
