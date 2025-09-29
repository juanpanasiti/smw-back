from uuid import uuid4

from src.domain.expense import ExpenseCategoryFactory
from ...dtos import CreateExpenseCategoryDTO, ExpenseCategoryResponseDTO
from ...ports import ExpenseCategoryRepository


class ExpenseCategoryCreateUseCase:
    def __init__(self, expense_category_repository: ExpenseCategoryRepository):
        self.expense_category_repository = expense_category_repository

    def execute(self, expense_category_data: CreateExpenseCategoryDTO) -> ExpenseCategoryResponseDTO:
        expense_category = ExpenseCategoryFactory.create(
            id=uuid4(),
            owner_id=expense_category_data.owner_id,
            name=expense_category_data.name,
            description=expense_category_data.description,
            is_income=expense_category_data.is_income,
        )
        new_expense_category = self.expense_category_repository.create(expense_category)
        return ExpenseCategoryResponseDTO(
            id=new_expense_category.id,
            owner_id=new_expense_category.owner_id,
            name=new_expense_category.name,
            description=new_expense_category.description,
            is_income=new_expense_category.is_income,
        )
