import logging
from typing import List

from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums.role_enum import ADMIN_ROLES
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.expense_schemas import NewExpenseReq, UpdateExpenseReq, ExpenseRes, ExpenseListParam
from app.services.expense_service import ExpenseService


class ExpenseController:
    def __init__(self):
        self.__expense_service = None

    @property
    def expense_service(self):
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    @handle_exceptions
    def create(self, token: DecodedJWT, new_expense: NewExpenseReq) -> ExpenseRes:
        return self.expense_service.create(new_expense)

    @handle_exceptions
    def get_list(self, token: DecodedJWT, account_id: int | None, params: ExpenseListParam) -> List[ExpenseRes]:
        return self.expense_service.get_list(token.user_id, account_id, params)

    @handle_exceptions
    def get_by_id(self, token: DecodedJWT, expense_id: int) -> ExpenseRes:
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense = self.expense_service.get_one(search_filter, include_relationships=True)
        if expense is None:
            raise ce.NotFound('Expense not found')
        return expense
        
    @handle_exceptions
    def update(self, token: DecodedJWT, expense_id: int, expense: UpdateExpenseReq) -> ExpenseRes:
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense_res = self.expense_service.update(expense, search_filter)
        if expense_res is None:
            raise ce.NotFound('Expense not found')
        return expense_res

    @handle_exceptions
    def delete_one(self, token: DecodedJWT, expense_id: int):
        search_filter = {'id': expense_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        was_deleted = self.expense_service.delete(search_filter)
        if not was_deleted:
            raise ce.NotFound('Credit card not found')
