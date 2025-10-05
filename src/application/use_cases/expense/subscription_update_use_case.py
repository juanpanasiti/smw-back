from uuid import UUID

from src.domain.expense import Subscription
from ...dtos import UpdateSubscriptionDTO, ExpenseResponseDTO
from ...ports import ExpenseRepository
from .helpers import parse_expense


class SubscriptionUpdateUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Subscription]):
        self.expense_repository = expense_repository

    def execute(self, subscription_id: UUID, subscription_data: UpdateSubscriptionDTO) -> ExpenseResponseDTO:
        subscription = self.expense_repository.get_by_filter({'id': subscription_id})
        if not subscription:
            raise ValueError("Subscription not found")
        for field, value in subscription_data.model_dump(exclude_unset=True).items():
            setattr(subscription, field, value)
        updated_subscription = self.expense_repository.update(subscription)
        return parse_expense(updated_subscription)
