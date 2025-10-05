from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.expense import SubscriptionCreateUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import ExpenseResponseDTO, CreateSubscriptionDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from src.domain.account import CreditCard
from src.domain.expense import ExpenseStatus


@pytest.fixture
def repo() -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.create.side_effect = lambda expense: expense
    return repo


def test_subscription_create_use_case_success(repo: ExpenseRepository, main_credit_card: CreditCard):
    use_case = SubscriptionCreateUseCase(repo)
    subscription_data = CreateSubscriptionDTO(
        account_id=main_credit_card.id,
        title='Some Subscription',
        cc_name='merpago*someplace',
        acquired_at=date.today(),
        amount=150.75,
        installments=1,
        first_payment_date=date.today(),
        category_id=uuid4(),
        status=ExpenseStatus.ACTIVE,
    )

    expense_response = use_case.execute(subscription_data)

    assert isinstance(expense_response, ExpenseResponseDTO), \
        f'Expected instance of ExpenseResponseDTO, got {type(expense_response)}'
    assert expense_response.title == subscription_data.title, \
        f'Expected title {subscription_data.title}, got {expense_response.title}'
    assert expense_response.amount == subscription_data.amount, \
        f'Expected amount {subscription_data.amount}, got {expense_response.amount}'
    assert expense_response.account_id == subscription_data.account_id, \
        f'Expected account_id {subscription_data.account_id}, got {expense_response.account_id}'
