import logging
from typing import List

from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums.role_enum import ADMIN_ROLES
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.expense_category_schemas import NewExpenseCategoryReq, UpdateExpenseCategoryReq, ExpenseCategoryRes
from app.services import ExpenseCategoryService, ExpenseService


class ExpenseCategoryController:
    def __init__(self):
        self.__expense_category_service = None
        self.__expense_service = None

    @property
    def expense_category_service(self):
        if self.__expense_category_service is None:
            self.__expense_category_service = ExpenseCategoryService()
        return self.__expense_category_service

    @property
    def expense_service(self):
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service

    @handle_exceptions
    def create(self, token: DecodedJWT, expense_category: NewExpenseCategoryReq) -> ExpenseCategoryRes:
        if token.role not in ADMIN_ROLES:
            expense_category.user_id = token.user_id
        return self.expense_category_service.create(expense_category)

    @handle_exceptions
    def get_list(self, token: DecodedJWT) -> List[ExpenseCategoryRes]:
        return self.expense_category_service.get_list(token.user_id)

    @handle_exceptions
    def get_by_id(self, token: DecodedJWT, expense_category_id: int) -> ExpenseCategoryRes:
        search_filter = {'id': expense_category_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense_category = self.expense_category_service.get_one(search_filter)
        if not expense_category:
            raise ce.NotFound('Expense category not found')
        return expense_category

    @handle_exceptions
    def update(self, token: DecodedJWT, expense_category_id: int, expense_category: UpdateExpenseCategoryReq) -> ExpenseCategoryRes:
        search_filter = {'id': expense_category_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expense_category = self.expense_category_service.update(expense_category, search_filter)
        if not expense_category:
            raise ce.NotFound('Expense category not found')
        return expense_category

    @handle_exceptions
    def delete_one(self, token: DecodedJWT, expense_category_id: int):
        search_filter = {'id': expense_category_id}
        if token.role not in ADMIN_ROLES:
            search_filter['user_id'] = token.user_id
        expenses_count = self.expense_service.count({'category_id': expense_category_id})
        if expenses_count > 0:
            logging.warning(f'Cannot delete expense category with expenses associated: {expenses_count}')
            raise ce.BadRequest('Cannot delete expense category with expenses associated',
                                exception_code='EXCEPTION_CATEGORY_NOT_EMPTY')
        was_deleted = self.expense_category_service.delete(search_filter)
        if not was_deleted:
            logging.warning(f'Expense category not found: {expense_category_id}')
            raise ce.NotFound('Expense category not found')
        
