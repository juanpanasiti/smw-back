from uuid import uuid4

from src.domain.expense import PurchaseFactory, Purchase
from src.domain.shared import Amount
from ...dtos import CreatePurchaseDTO, ExpenseResponseDTO
from ...ports import ExpenseRepository
from .helpers import parse_expense


class PurchaseCreateUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Purchase]):
        self.expense_repository = expense_repository

    def execute(self, purchase_data: CreatePurchaseDTO) -> ExpenseResponseDTO:
        purchase = PurchaseFactory.create(
            id=uuid4(),
            account_id=purchase_data.account_id,
            title=purchase_data.title,
            cc_name=purchase_data.cc_name,
            acquired_at=purchase_data.acquired_at,
            amount=Amount(purchase_data.amount),
            installments=purchase_data.installments,
            first_payment_date=purchase_data.first_payment_date,
            category_id=purchase_data.category_id,
            payments=[],
        )
        self.expense_repository.create(purchase)
        return parse_expense(purchase)
