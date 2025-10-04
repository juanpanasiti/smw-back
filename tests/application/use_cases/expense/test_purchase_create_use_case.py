from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date

import pytest

from src.application.use_cases.expense import PurchaseCreateUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import ExpenseResponseDTO, CreatePurchaseDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from src.domain.account import CreditCard


@pytest.fixture
def repo() -> ExpenseRepository:
    repo = MagicMock(spec=ExpenseRepository)
    repo.create.side_effect = lambda expense: expense
    return repo


def test_purchase_create_use_case_success(repo: ExpenseRepository, main_credit_card: CreditCard):
    use_case = PurchaseCreateUseCase(repo)
    purchase_data = CreatePurchaseDTO(
        account_id=main_credit_card.id,
        title='Some Purchase',
        cc_name='merpago*someplace',
        acquired_at=date.today(),
        amount=150.75,
        installments=1,
        first_payment_date=date.today(),
        category_id=uuid4(),
    )

    expense_response = use_case.execute(purchase_data)

    assert isinstance(expense_response, ExpenseResponseDTO), \
        f'Expected instance of ExpenseResponseDTO, got {type(expense_response)}'
    assert expense_response.title == purchase_data.title, \
        f'Expected title {purchase_data.title}, got {expense_response.title}'
    assert expense_response.amount == purchase_data.amount, \
        f'Expected amount {purchase_data.amount}, got {expense_response.amount}'
    assert expense_response.account_id == purchase_data.account_id, \
        f'Expected account_id {purchase_data.account_id}, got {expense_response.account_id}'
