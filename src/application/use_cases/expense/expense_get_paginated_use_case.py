from src.domain.expense import Expense
from ...dtos import ExpenseResponseDTO, PaginatedResponse, Pagination
from ...ports import ExpenseRepository
from .helpers import parse_expense


class ExpenseGetPaginatedUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Expense]):
        self.expense_repository = expense_repository

    def execute(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[ExpenseResponseDTO]:
        total_items = self.expense_repository.count_by_filter(filter)
        items = self.expense_repository.get_many_by_filter(filter, limit, offset)
        return PaginatedResponse[ExpenseResponseDTO](
            items=[parse_expense(expense) for expense in items],
            pagination=Pagination(
                current_page=offset // limit + 1,
                total_pages=(total_items // limit) + (1 if total_items % limit > 0 else 0),
                total_items=total_items,
                per_page=limit,
            )
        )
