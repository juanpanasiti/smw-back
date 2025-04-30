import logging
from typing import List

from app.schemas.expense_category_schemas_v2 import NewExpenseCategoryReq, UpdateExpenseCategoryReq, ExpenseCategoryRes
from app.repositories import ExpenseCategoryRepository


logger = logging.getLogger(__name__)


class ExpenseCategoryServiceV2:
    def __init__(self):
        self.__expense_category_repo = None


    @property
    def expense_category_repo(self):
        if self.__expense_category_repo is None:
            self.__expense_category_repo = ExpenseCategoryRepository()
        return self.__expense_category_repo
    


    def create(self, expense_category: NewExpenseCategoryReq) -> ExpenseCategoryRes:
        new_expense_category = self.expense_category_repo.create(expense_category.model_dump())
        return ExpenseCategoryRes(**new_expense_category)

    def get_list(self, user_id: int) -> List[ExpenseCategoryRes]:
        params_dict = {'user_id': user_id}
        expenses = self.expense_category_repo.get_many(**params_dict)
        return [ExpenseCategoryRes(**expense) for expense in expenses]

    def get_one(self, search_filter: dict) -> ExpenseCategoryRes | None:
        expense = self.expense_category_repo.get_one(search_filter)
        return ExpenseCategoryRes(**expense) if expense else None

    def update(self, expense_category: UpdateExpenseCategoryReq, search_filter: dict) -> ExpenseCategoryRes | None:
        new_data = expense_category.model_dump(exclude_none=True)
        updated_expense = self.expense_category_repo.update(new_data, search_filter)
        return ExpenseCategoryRes(**updated_expense)

    def delete(self, search_filter: dict) -> bool:
        # !DELETE PRINT
        print('\033[91m', 'delete', '\033[0m')
        return self.expense_category_repo.delete(search_filter)
