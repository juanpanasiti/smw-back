from uuid import UUID

from src.domain.expense import Purchase
from ...dtos import ExpenseResponseDTO
from ...ports import ExpenseRepository
from .helpers import parse_expense


class PurchaseGetOneUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Purchase]):
        self.expense_repository = expense_repository

    def execute(self, purchase_id: UUID) -> ExpenseResponseDTO:
        purchase = self.expense_repository.get_by_filter({'id': purchase_id})
        if not purchase:
            raise ValueError("Purchase not found")
        return parse_expense(purchase)
