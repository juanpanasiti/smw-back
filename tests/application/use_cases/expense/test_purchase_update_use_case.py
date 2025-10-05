from unittest.mock import MagicMock

import pytest

from src.application.use_cases.expense import PurchaseUpdateUseCase
from src.application.ports import ExpenseRepository
from src.application.dtos import UpdatePurchaseDTO
from tests.fixtures.account_fixtures import main_credit_card  # noqa: F401
from tests.fixtures.auth_fixtures import user  # noqa: F401
from tests.fixtures.expense_fixtures import purchase  # noqa: F401
from src.domain.expense import Purchase
from src.domain.shared import Amount


def get_fake_purchase(filter: dict, purchase: Purchase) -> Purchase:
    purchase.id = filter.get('id', purchase.id)
    return purchase


@pytest.fixture
def repo(purchase: Purchase) -> ExpenseRepository:
    repo: ExpenseRepository = MagicMock(spec=ExpenseRepository)
    repo.get_by_filter.side_effect = lambda filter: get_fake_purchase(filter, purchase)
    repo.update.side_effect = lambda purchase: purchase
    return repo


def test_purchase_update_use_case_success(repo: ExpenseRepository, purchase: Purchase):
    use_case = PurchaseUpdateUseCase(repo)
    purchase_id = purchase.id
    update_data = UpdatePurchaseDTO(
        cc_name='updated*ccname',
        title='Updated Purchase Title',
    )
    updated_purchase = use_case.execute(purchase_id, update_data)
    assert updated_purchase.id == purchase_id
    assert updated_purchase.cc_name == update_data.cc_name
    assert updated_purchase.title == update_data.title
    assert updated_purchase.acquired_at == purchase.acquired_at
