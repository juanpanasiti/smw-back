from uuid import UUID

from src.domain.expense import Purchase
from ...ports import ExpenseRepository


class PurchaseDeleteUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Purchase]):
        self.expense_repository = expense_repository

    def execute(self, purchase_id: UUID) -> None:
        self.expense_repository.delete_by_filter({'id': purchase_id})
