from ...ports import ExpenseCategoryRepository
from ...dtos import ExpenseCategoryResponseDTO


class ExpenseCategoryGetPaginatedUseCase:
    def __init__(self, expense_category_repository: ExpenseCategoryRepository):
        self.expense_category_repository = expense_category_repository

    def execute(self, filter: dict, limit: int, offset: int) -> list[ExpenseCategoryResponseDTO]:
        categories = self.expense_category_repository.get_many_by_filter(filter, limit, offset)
        return [ExpenseCategoryResponseDTO.model_validate(cat) for cat in categories]
