import pytest
from uuid import uuid4, UUID
from unittest.mock import MagicMock
from datetime import date

from src.entrypoints.controllers import AccountController
from src.application.dtos import (
    CreateCreditCardDTO,
    UpdateCreditCardDTO,
    CreditCardResponseDTO,
    PaginatedResponse,
    Pagination,
)
from src.application.ports import CreditCardRepository
from src.entrypoints.exceptions.client_exceptions import BadRequest, NotFound
from src.entrypoints.exceptions.server_exceptions import InternalServerError
from src.common.exceptions import RepoNotFoundError


@pytest.fixture
def credit_card_repository_mock() -> MagicMock:
    return MagicMock(spec=CreditCardRepository)


@pytest.fixture
def controller(credit_card_repository_mock: MagicMock) -> AccountController:
    return AccountController(credit_card_repository=credit_card_repository_mock)


@pytest.fixture
def create_credit_card_dto() -> CreateCreditCardDTO:
    return CreateCreditCardDTO(
        owner_id=uuid4(),
        alias='My Credit Card',
        limit=5000.0,
        main_credit_card_id=None,
        next_closing_date=date(2025, 12, 15),
        next_expiring_date=date(2026, 1, 10),
        financing_limit=1000.0,
    )


@pytest.fixture
def update_credit_card_dto() -> UpdateCreditCardDTO:
    return UpdateCreditCardDTO(
        alias='Updated Card',
        limit=6000.0,
        is_enabled=True,
        next_closing_date=date(2025, 12, 20),
        next_expiring_date=date(2026, 1, 15),
        financing_limit=1500.0,
    )


@pytest.fixture
def credit_card_response_dto() -> CreditCardResponseDTO:
    return CreditCardResponseDTO(
        id=uuid4(),
        owner_id=uuid4(),
        alias='Test Card',
        limit=5000.0,
        is_enabled=True,
        main_credit_card_id=None,
        next_closing_date=date(2025, 12, 15),
        next_expiring_date=date(2026, 1, 10),
        financing_limit=1000.0,
        total_expenses_count=0,
        total_purchases_count=0,
        total_subscriptions_count=0,
        used_limit=0.0,
        available_limit=5000.0,
        used_financing_limit=0.0,
        available_financing_limit=1000.0,
    )


# Create Credit Card tests

@pytest.fixture
def create_credit_card_use_case_ok(monkeypatch: pytest.MonkeyPatch, credit_card_response_dto: CreditCardResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = credit_card_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardCreateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def create_credit_card_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid credit card data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardCreateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def create_credit_card_use_case_exception(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = Exception('Unexpected error')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardCreateUseCase', uc_class)
    return uc_instance


def test_create_credit_card_success(
    controller: AccountController,
    create_credit_card_dto: CreateCreditCardDTO,
    create_credit_card_use_case_ok: MagicMock,
) -> None:
    result = controller.create_credit_card(create_credit_card_dto)
    assert isinstance(result, CreditCardResponseDTO)
    assert result.alias == 'Test Card'


def test_create_credit_card_bad_request(
    controller: AccountController,
    create_credit_card_dto: CreateCreditCardDTO,
    create_credit_card_use_case_value_error: MagicMock,
) -> None:
    with pytest.raises(BadRequest) as exc:
        controller.create_credit_card(create_credit_card_dto)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'CREATE_CREDIT_CARD_BAD_REQUEST'


def test_create_credit_card_unexpected_error(
    controller: AccountController,
    create_credit_card_dto: CreateCreditCardDTO,
    create_credit_card_use_case_exception: MagicMock,
) -> None:
    with pytest.raises(InternalServerError) as exc:
        controller.create_credit_card(create_credit_card_dto)
    assert exc.value.status_code == 500


# Get Credit Card tests

@pytest.fixture
def get_credit_card_use_case_ok(monkeypatch: pytest.MonkeyPatch, credit_card_response_dto: CreditCardResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = credit_card_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardGetOneUseCase', uc_class)
    return uc_instance


@pytest.fixture
def get_credit_card_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = RepoNotFoundError('Credit card not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardGetOneUseCase', uc_class)
    return uc_instance


def test_get_credit_card_success(
    controller: AccountController,
    get_credit_card_use_case_ok: MagicMock,
) -> None:
    credit_card_id = uuid4()
    result = controller.get_credit_card(credit_card_id)
    assert isinstance(result, CreditCardResponseDTO)


def test_get_credit_card_not_found(
    controller: AccountController,
    get_credit_card_use_case_value_error: MagicMock,
) -> None:
    credit_card_id = uuid4()
    with pytest.raises(NotFound) as exc:
        controller.get_credit_card(credit_card_id)
    assert exc.value.status_code == 404
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'CREDIT_CARD_NOT_FOUND'


# Update Credit Card tests

@pytest.fixture
def update_credit_card_use_case_ok(monkeypatch: pytest.MonkeyPatch, credit_card_response_dto: CreditCardResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = credit_card_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardUpdateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def update_credit_card_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid update data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardUpdateUseCase', uc_class)
    return uc_instance


def test_update_credit_card_success(
    controller: AccountController,
    update_credit_card_dto: UpdateCreditCardDTO,
    update_credit_card_use_case_ok: MagicMock,
) -> None:
    credit_card_id = uuid4()
    result = controller.update_credit_card(credit_card_id, update_credit_card_dto)
    assert isinstance(result, CreditCardResponseDTO)


def test_update_credit_card_bad_request(
    controller: AccountController,
    update_credit_card_dto: UpdateCreditCardDTO,
    update_credit_card_use_case_value_error: MagicMock,
) -> None:
    credit_card_id = uuid4()
    with pytest.raises(BadRequest) as exc:
        controller.update_credit_card(credit_card_id, update_credit_card_dto)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'UPDATE_CREDIT_CARD_BAD_REQUEST'


# Delete Credit Card tests

@pytest.fixture
def delete_credit_card_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = None
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardDeleteUseCase', uc_class)
    return uc_instance


@pytest.fixture
def delete_credit_card_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Credit card not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardDeleteUseCase', uc_class)
    return uc_instance


def test_delete_credit_card_success(
    controller: AccountController,
    delete_credit_card_use_case_ok: MagicMock,
) -> None:
    credit_card_id = uuid4()
    controller.delete_credit_card(credit_card_id)
    delete_credit_card_use_case_ok.execute.assert_called_once_with(credit_card_id)


def test_delete_credit_card_not_found(
    controller: AccountController,
    delete_credit_card_use_case_value_error: MagicMock,
) -> None:
    credit_card_id = uuid4()
    with pytest.raises(NotFound) as exc:
        controller.delete_credit_card(credit_card_id)
    assert exc.value.status_code == 404
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'CREDIT_CARD_NOT_FOUND'


# Get Paginated Credit Cards tests

@pytest.fixture
def get_paginated_credit_cards_use_case_ok(monkeypatch: pytest.MonkeyPatch, credit_card_response_dto: CreditCardResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = PaginatedResponse(
        items=[credit_card_response_dto],
        pagination=Pagination(current_page=1, total_pages=1, total_items=1, per_page=10),
    )
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardGetPaginatedUseCase', uc_class)
    return uc_instance


@pytest.fixture
def get_paginated_credit_cards_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid pagination parameters')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.account_controller.CreditCardGetPaginatedUseCase', uc_class)
    return uc_instance


def test_get_paginated_credit_cards_success(
    controller: AccountController,
    get_paginated_credit_cards_use_case_ok: MagicMock,
) -> None:
    result = controller.get_paginated_credit_cards(filter={}, limit=10, offset=0)
    assert isinstance(result, PaginatedResponse)
    assert len(result.items) == 1


def test_get_paginated_credit_cards_bad_request(
    controller: AccountController,
    get_paginated_credit_cards_use_case_value_error: MagicMock,
) -> None:
    with pytest.raises(BadRequest) as exc:
        controller.get_paginated_credit_cards(filter={}, limit=10, offset=0)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'PAGINATION_BAD_REQUEST'
