from uuid import UUID

from src.domain.expense import Subscription
from ...dtos import ExpenseResponseDTO
from ...ports import ExpenseRepository
from .helpers import parse_expense


class SubscriptionGetOneUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Subscription]):
        self.expense_repository = expense_repository

    def execute(self, subscription_id: UUID) -> ExpenseResponseDTO:
        subscription = self.expense_repository.get_by_filter({'id': subscription_id})
        if not subscription:
            raise ValueError('Subscription not found')
        return parse_expense(subscription)
