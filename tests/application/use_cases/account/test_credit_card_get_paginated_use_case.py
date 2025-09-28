from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.account import CreditCardGetPaginatedUseCase
from src.application.ports import CreditCardRepository
from src.application.dtos import PaginatedResponse


@pytest.fixture
def repo() -> CreditCardRepository:
    repo: CreditCardRepository = MagicMock(spec=CreditCardRepository)
    repo.get_many_by_filter.return_value = []
    return repo


def test_credit_card_get_paginated_use_case_success(repo: CreditCardRepository):
    use_case = CreditCardGetPaginatedUseCase(credit_card_repository=repo)
    result = use_case.execute(filter={'owner_id': uuid4()}, limit=10, offset=0)
    assert isinstance(
        result, PaginatedResponse), f'Expected PaginatedResponse, got {type(result)}'
