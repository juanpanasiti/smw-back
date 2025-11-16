from uuid import uuid4

from src.domain.expense import SubscriptionFactory, Subscription
from src.domain.shared import Amount
from ...dtos import CreateSubscriptionDTO, ExpenseResponseDTO
from ...ports import ExpenseRepository
from .helpers import parse_expense


class SubscriptionCreateUseCase:
    def __init__(self, expense_repository: ExpenseRepository[Subscription]):
        self.expense_repository = expense_repository

    def execute(self, subscription_data: CreateSubscriptionDTO) -> ExpenseResponseDTO:
        subscription = SubscriptionFactory.create(
            id=uuid4(),
            account_id=subscription_data.account_id,
            title=subscription_data.title,
            cc_name=subscription_data.cc_name,
            acquired_at=subscription_data.acquired_at,
            amount=Amount(subscription_data.amount),
            first_payment_date=subscription_data.first_payment_date,
            category_id=subscription_data.category_id,
            payments=[],
        )
        self.expense_repository.create(subscription)
        return parse_expense(subscription)
