from ...ports import ExpenseCategoryRepository
from ...dtos import ExpenseCategoryResponseDTO, PaginatedResponse, Pagination
from .helpers import parse_expense_category


class ExpenseCategoryGetPaginatedUseCase:
    def __init__(self, expense_category_repository: ExpenseCategoryRepository):
        self.expense_category_repository = expense_category_repository

    def execute(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[ExpenseCategoryResponseDTO]:
        categories = self.expense_category_repository.get_many_by_filter(
            filter, limit, offset)
        total = self.expense_category_repository.count_by_filter(filter)
        return PaginatedResponse[ExpenseCategoryResponseDTO](
            items=[parse_expense_category(cat) for cat in categories],
            pagination=Pagination(
                total_pages=(total // limit) + 1,
                total_items=total,
                per_page=limit,
                current_page=offset // limit + 1,
            )
        )
