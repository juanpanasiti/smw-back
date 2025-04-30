import logging
from typing import List

from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums.role_enum import ADMIN_ROLES
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.expense_schemas_v2 import NewExpenseReqV2, UpdateExpenseReqV2, ExpenseResV2, ExpenseListParamV2
from app.services import ExpenseServiceV2


class ExpenseControllerV2:
    def __init__(self):
        self.__expense_service = None

    @property
    def expense_service(self):
        if self.__expense_service is None:
            self.__expense_service = ExpenseServiceV2()
        return self.__expense_service

    @handle_exceptions
    def create(self, token: DecodedJWT, new_expense: NewExpenseReqV2) -> ExpenseResV2:
        return self.expense_service.create(new_expense)

    @handle_exceptions
    def get_list(self, token: DecodedJWT, account_id: int | None, params: ExpenseListParamV2) -> List[ExpenseResV2]:
        return self.expense_service.get_list(token.user_id, account_id, params)

    @handle_exceptions
    def get_by_id(self, token: DecodedJWT, expense_id: int) -> ExpenseResV2:
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense = self.expense_service.get_one(search_filter, include_relationships=True)
        if expense is None:
            raise ce.NotFound('Expense not found', 'EXPENSE_NOT_FOUND')
        return expense
        
    @handle_exceptions
    def update(self, token: DecodedJWT, expense_id: int, expense: UpdateExpenseReqV2) -> ExpenseResV2:
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense_res = self.expense_service.update(expense, search_filter)
        if expense_res is None:
            raise ce.NotFound('Expense not found', 'EXPENSE_NOT_FOUND')
        return expense_res

    @handle_exceptions
    def delete_one(self, token: DecodedJWT, expense_id: int):
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        was_deleted = self.expense_service.delete(search_filter)
        if not was_deleted:
            raise ce.NotFound('Expense not found', 'EXPENSE_NOT_FOUND')
