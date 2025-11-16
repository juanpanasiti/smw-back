from uuid import UUID

from src.domain.expense import Subscription
from ...ports import ExpenseRepository


class SubscriptionDeleteUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Subscription]):
        self.expense_repository = expense_repository

    def execute(self, subscription_id: UUID) -> None:
        self.expense_repository.delete_by_filter({'id': subscription_id})
