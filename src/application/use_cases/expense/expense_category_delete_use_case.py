from uuid import UUID

from ...ports import ExpenseCategoryRepository


class ExpenseCategoryDeleteUseCase:
    def __init__(self, expense_category_repository: ExpenseCategoryRepository):
        self.expense_category_repository = expense_category_repository

    def execute(self, category_id: UUID):
        self.expense_category_repository.delete_by_filter({'id': category_id})
