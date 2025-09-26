from uuid import UUID

from ...dtos import UpdateCreditCardDTO, ExpenseCategoryResponseDTO
from ...ports import ExpenseCategoryRepository


class ExpenseCategoryUpdateUseCase:
    def __init__(self, expense_category_repository: ExpenseCategoryRepository):
        self.expense_category_repository = expense_category_repository

    def execute(self, category_id: UUID, category_data: UpdateCreditCardDTO) -> ExpenseCategoryResponseDTO:
        expense_category = self.expense_category_repository.get_by_filter({'id': category_id})
        if expense_category is None:
            raise ValueError("Expense category not found")
        # Update only the fields that are provided in category_data
        for field, value in category_data.model_dump(exclude_unset=True).items():
            setattr(expense_category, field, value)
        updated_expense_category = self.expense_category_repository.update(expense_category)
        return ExpenseCategoryResponseDTO.model_validate(updated_expense_category)
