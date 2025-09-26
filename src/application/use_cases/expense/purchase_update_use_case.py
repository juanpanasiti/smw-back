from uuid import UUID

from src.domain.expense import Purchase
from ...dtos import UpdatePurchaseDTO, ExpenseResponseDTO
from ...ports import ExpenseRepository


class PurchaseUpdateUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Purchase]):
        self.expense_repository = expense_repository

    def execute(self, purchase_id: UUID, purchase_data: UpdatePurchaseDTO) -> ExpenseResponseDTO:
        purchase = self.expense_repository.get_by_filter({'id': purchase_id})
        if not purchase:
            raise ValueError("Purchase not found")
        for field, value in purchase_data.model_dump(exclude_unset=True).items():
            setattr(purchase, field, value)
        updated_purchase = self.expense_repository.update(purchase)
        return ExpenseResponseDTO.model_validate(updated_purchase)
