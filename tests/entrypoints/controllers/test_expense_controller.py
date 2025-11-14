import pytest
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import date

from src.entrypoints.controllers import ExpenseController
from src.application.dtos import (
    CreateExpenseCategoryDTO,
    UpdateExpenseCategoryDTO,
    ExpenseCategoryResponseDTO,
    CreatePurchaseDTO,
    UpdatePurchaseDTO,
    CreateSubscriptionDTO,
    UpdateSubscriptionDTO,
    ExpenseResponseDTO,
    PaginatedResponse,
    Pagination,
    CreatePaymentDTO,
    UpdatePaymentDTO,
    PaymentResponseDTO,
)
from src.application.ports import ExpenseCategoryRepository, ExpenseRepository, PaymentRepository
from src.entrypoints.exceptions.client_exceptions import BadRequest, NotFound
from src.entrypoints.exceptions.server_exceptions import InternalServerError
from src.domain.expense.enums import ExpenseType, ExpenseStatus


@pytest.fixture
def expense_category_repository_mock() -> MagicMock:
    return MagicMock(spec=ExpenseCategoryRepository)


@pytest.fixture
def expense_repository_mock() -> MagicMock:
    return MagicMock(spec=ExpenseRepository)


@pytest.fixture
def payment_repository_mock() -> MagicMock:
    return MagicMock(spec=PaymentRepository)


@pytest.fixture
def controller(
    expense_category_repository_mock: MagicMock,
    expense_repository_mock: MagicMock,
    payment_repository_mock: MagicMock,
) -> ExpenseController:
    return ExpenseController(
        expense_category_repository=expense_category_repository_mock,
        expense_repository=expense_repository_mock,
        payment_repository=payment_repository_mock,
    )


@pytest.fixture
def create_category_dto() -> CreateExpenseCategoryDTO:
    return CreateExpenseCategoryDTO(
        owner_id=uuid4(),
        name='Food',
        description='Food expenses',
        is_income=False,
    )


@pytest.fixture
def category_response_dto() -> ExpenseCategoryResponseDTO:
    return ExpenseCategoryResponseDTO(
        id=uuid4(),
        owner_id=uuid4(),
        name='Food',
        description='Food expenses',
        is_income=False,
    )


@pytest.fixture
def create_purchase_dto() -> CreatePurchaseDTO:
    return CreatePurchaseDTO(
        account_id=uuid4(),
        title='Laptop',
        cc_name='My Card',
        acquired_at=date(2025, 11, 1),
        amount=1000.0,
        installments=12,
        first_payment_date=date(2025, 12, 1),
        category_id=uuid4(),
    )


@pytest.fixture
def expense_response_dto() -> ExpenseResponseDTO:
    return ExpenseResponseDTO(
        id=uuid4(),
        account_id=uuid4(),
        title='Laptop',
        cc_name='My Card',
        acquired_at=date(2025, 11, 1),
        amount=1000.0,
        installments=12,
        first_payment_date=date(2025, 12, 1),
        category_id=uuid4(),
        expense_type=ExpenseType.PURCHASE,
        status=ExpenseStatus.PENDING,
        payments=[],
        is_one_time_payment=False,
        paid_amount=0.0,
        pending_installments=12,
        done_installments=0,
        pending_financing_amount=1000.0,
        pending_amount=1000.0,
    )


# Expense Category tests

@pytest.fixture
def create_category_use_case_ok(monkeypatch: pytest.MonkeyPatch, category_response_dto: ExpenseCategoryResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = category_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryCreateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def create_category_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid category data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryCreateUseCase', uc_class)
    return uc_instance


def test_create_expense_category_success(
    controller: ExpenseController,
    create_category_dto: CreateExpenseCategoryDTO,
    create_category_use_case_ok: MagicMock,
) -> None:
    result = controller.create_expense_category(create_category_dto)
    assert isinstance(result, ExpenseCategoryResponseDTO)
    assert result.name == 'Food'


def test_create_expense_category_bad_request(
    controller: ExpenseController,
    create_category_dto: CreateExpenseCategoryDTO,
    create_category_use_case_value_error: MagicMock,
) -> None:
    with pytest.raises(BadRequest) as exc:
        controller.create_expense_category(create_category_dto)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'CREATE_CATEGORY_BAD_REQUEST'


# Purchase tests

@pytest.fixture
def create_purchase_use_case_ok(monkeypatch: pytest.MonkeyPatch, expense_response_dto: ExpenseResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseCreateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def create_purchase_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid purchase data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseCreateUseCase', uc_class)
    return uc_instance


def test_create_purchase_success(
    controller: ExpenseController,
    create_purchase_dto: CreatePurchaseDTO,
    create_purchase_use_case_ok: MagicMock,
) -> None:
    result = controller.create_purchase(create_purchase_dto)
    assert isinstance(result, ExpenseResponseDTO)
    assert result.title == 'Laptop'


def test_create_purchase_bad_request(
    controller: ExpenseController,
    create_purchase_dto: CreatePurchaseDTO,
    create_purchase_use_case_value_error: MagicMock,
) -> None:
    with pytest.raises(BadRequest) as exc:
        controller.create_purchase(create_purchase_dto)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'CREATE_PURCHASE_BAD_REQUEST'


@pytest.fixture
def get_purchase_use_case_ok(monkeypatch: pytest.MonkeyPatch, expense_response_dto: ExpenseResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseGetOneUseCase', uc_class)
    return uc_instance


@pytest.fixture
def get_purchase_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Purchase not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseGetOneUseCase', uc_class)
    return uc_instance


def test_get_purchase_success(
    controller: ExpenseController,
    get_purchase_use_case_ok: MagicMock,
) -> None:
    purchase_id = uuid4()
    result = controller.get_purchase(purchase_id)
    assert isinstance(result, ExpenseResponseDTO)


def test_get_purchase_not_found(
    controller: ExpenseController,
    get_purchase_use_case_value_error: MagicMock,
) -> None:
    purchase_id = uuid4()
    with pytest.raises(NotFound) as exc:
        controller.get_purchase(purchase_id)
    assert exc.value.status_code == 404
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'PURCHASE_NOT_FOUND'


@pytest.fixture
def delete_purchase_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = None
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseDeleteUseCase', uc_class)
    return uc_instance


@pytest.fixture
def delete_purchase_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Purchase not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseDeleteUseCase', uc_class)
    return uc_instance


def test_delete_purchase_success(
    controller: ExpenseController,
    delete_purchase_use_case_ok: MagicMock,
) -> None:
    purchase_id = uuid4()
    controller.delete_purchase(purchase_id)
    delete_purchase_use_case_ok.execute.assert_called_once_with(purchase_id)


def test_delete_purchase_not_found(
    controller: ExpenseController,
    delete_purchase_use_case_value_error: MagicMock,
) -> None:
    purchase_id = uuid4()
    with pytest.raises(NotFound) as exc:
        controller.delete_purchase(purchase_id)
    assert exc.value.status_code == 404
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail['code'] == 'PURCHASE_NOT_FOUND'


# Subscription tests (similar to purchase)

@pytest.fixture
def create_subscription_dto() -> CreateSubscriptionDTO:
    return CreateSubscriptionDTO(
        account_id=uuid4(),
        title='Netflix',
        cc_name='My Card',
        acquired_at=date(2025, 11, 1),
        amount=15.99,
        installments=1,
        first_payment_date=date(2025, 12, 1),
        status=ExpenseStatus.ACTIVE,
        category_id=uuid4(),
    )


@pytest.fixture
def create_subscription_use_case_ok(monkeypatch: pytest.MonkeyPatch, expense_response_dto: ExpenseResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionCreateUseCase', uc_class)
    return uc_instance


def test_create_subscription_success(
    controller: ExpenseController,
    create_subscription_dto: CreateSubscriptionDTO,
    create_subscription_use_case_ok: MagicMock,
) -> None:
    result = controller.create_subscription(create_subscription_dto)
    assert isinstance(result, ExpenseResponseDTO)


# Paginated expenses test

@pytest.fixture
def get_paginated_expenses_use_case_ok(monkeypatch: pytest.MonkeyPatch, expense_response_dto: ExpenseResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = PaginatedResponse(
        items=[expense_response_dto],
        pagination=Pagination(current_page=1, total_pages=1, total_items=1, per_page=10),
    )
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseGetPaginatedUseCase', uc_class)
    return uc_instance


def test_get_paginated_expenses_success(
    controller: ExpenseController,
    get_paginated_expenses_use_case_ok: MagicMock,
) -> None:
    result = controller.get_paginated_expenses(filter={}, limit=10, offset=0)
    assert isinstance(result, PaginatedResponse)
    assert len(result.items) == 1


# Payment tests

@pytest.fixture
def create_payment_dto() -> CreatePaymentDTO:
    return CreatePaymentDTO(
        expense_id=uuid4(),
        amount=20.0,
        payment_date=date(2025, 2, 15),
    )


@pytest.fixture
def update_payment_dto() -> UpdatePaymentDTO:
    from src.domain.expense.enums import PaymentStatus
    return UpdatePaymentDTO(
        amount=30.0,
        status=PaymentStatus.CONFIRMED,
        payment_date=date(2025, 2, 20),
    )


@pytest.fixture
def payment_response_dto() -> PaymentResponseDTO:
    from src.domain.expense.enums import PaymentStatus
    return PaymentResponseDTO(
        id=uuid4(),
        expense_id=uuid4(),
        amount=20.0,
        no_installment=1,
        status=PaymentStatus.UNCONFIRMED,
        payment_date=date(2025, 2, 15),
        is_last_payment=False,
    )


@pytest.fixture
def create_payment_use_case_ok(monkeypatch: pytest.MonkeyPatch, payment_response_dto: PaymentResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = payment_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentCreateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def update_payment_use_case_ok(monkeypatch: pytest.MonkeyPatch, payment_response_dto: PaymentResponseDTO) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = payment_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentUpdateUseCase', uc_class)
    return uc_instance


@pytest.fixture
def delete_payment_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = None
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentDeleteUseCase', uc_class)
    return uc_instance


def test_create_payment_success(
    controller: ExpenseController,
    create_payment_dto: CreatePaymentDTO,
    create_payment_use_case_ok: MagicMock,
) -> None:
    result = controller.create_payment(create_payment_dto)
    assert isinstance(result, PaymentResponseDTO)
    create_payment_use_case_ok.execute.assert_called_once_with(create_payment_dto)


def test_create_payment_bad_request(
    controller: ExpenseController,
    create_payment_dto: CreatePaymentDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid payment data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentCreateUseCase', uc_class)
    
    with pytest.raises(BadRequest) as exc_info:
        controller.create_payment(create_payment_dto)
    
    assert 'Invalid payment data' in str(exc_info.value)


def test_create_payment_internal_error(
    controller: ExpenseController,
    create_payment_dto: CreatePaymentDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise generic exception
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = Exception('Database error')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentCreateUseCase', uc_class)
    
    with pytest.raises(InternalServerError):
        controller.create_payment(create_payment_dto)


def test_update_payment_success(
    controller: ExpenseController,
    update_payment_dto: UpdatePaymentDTO,
    update_payment_use_case_ok: MagicMock,
) -> None:
    payment_id = uuid4()
    result = controller.update_payment(payment_id, update_payment_dto)
    assert isinstance(result, PaymentResponseDTO)
    update_payment_use_case_ok.execute.assert_called_once_with(payment_id, update_payment_dto)


def test_update_payment_bad_request(
    controller: ExpenseController,
    update_payment_dto: UpdatePaymentDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Payment not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentUpdateUseCase', uc_class)
    
    payment_id = uuid4()
    with pytest.raises(BadRequest) as exc_info:
        controller.update_payment(payment_id, update_payment_dto)
    
    assert 'Payment not found' in str(exc_info.value)


def test_update_payment_internal_error(
    controller: ExpenseController,
    update_payment_dto: UpdatePaymentDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise generic exception
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = Exception('Database error')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentUpdateUseCase', uc_class)
    
    payment_id = uuid4()
    with pytest.raises(InternalServerError):
        controller.update_payment(payment_id, update_payment_dto)


def test_delete_payment_success(
    controller: ExpenseController,
    delete_payment_use_case_ok: MagicMock,
) -> None:
    payment_id = uuid4()
    result = controller.delete_payment(payment_id)
    assert result is None
    delete_payment_use_case_ok.execute.assert_called_once_with(payment_id)


def test_delete_payment_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Payment not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentDeleteUseCase', uc_class)
    
    payment_id = uuid4()
    with pytest.raises(NotFound) as exc_info:
        controller.delete_payment(payment_id)
    
    assert 'Payment not found' in str(exc_info.value)


def test_delete_payment_internal_error(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise generic exception
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = Exception('Database error')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PaymentDeleteUseCase', uc_class)
    
    payment_id = uuid4()
    with pytest.raises(InternalServerError):
        controller.delete_payment(payment_id)


# ExpenseCategory update tests

def test_update_expense_category_success(
    controller: ExpenseController,
    category_response_dto: ExpenseCategoryResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = category_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryUpdateUseCase', uc_class)
    
    update_dto = UpdateExpenseCategoryDTO(name='Updated Category')
    category_id = uuid4()
    result = controller.update_expense_category(category_id, update_dto)
    
    assert isinstance(result, ExpenseCategoryResponseDTO)
    uc_instance.execute.assert_called_once_with(category_id, update_dto)


def test_update_expense_category_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Category not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryUpdateUseCase', uc_class)
    
    update_dto = UpdateExpenseCategoryDTO(name='Test')
    category_id = uuid4()
    
    with pytest.raises(BadRequest) as exc_info:
        controller.update_expense_category(category_id, update_dto)
    
    assert 'Category not found' in str(exc_info.value)


# ExpenseCategory delete tests

def test_delete_expense_category_success(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = None
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryDeleteUseCase', uc_class)
    
    category_id = uuid4()
    result = controller.delete_expense_category(category_id)
    
    assert result is None
    uc_instance.execute.assert_called_once_with(category_id)


def test_delete_expense_category_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Category not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.ExpenseCategoryDeleteUseCase', uc_class)
    
    category_id = uuid4()
    
    with pytest.raises(NotFound) as exc_info:
        controller.delete_expense_category(category_id)
    
    assert 'Category not found' in str(exc_info.value)


# Purchase update tests

def test_update_purchase_success(
    controller: ExpenseController,
    expense_response_dto: ExpenseResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseUpdateUseCase', uc_class)
    
    update_dto = UpdatePurchaseDTO(title='Updated Purchase', amount=200.0)
    purchase_id = uuid4()
    result = controller.update_purchase(purchase_id, update_dto)
    
    assert isinstance(result, ExpenseResponseDTO)
    uc_instance.execute.assert_called_once_with(purchase_id, update_dto)


def test_update_purchase_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Purchase not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.PurchaseUpdateUseCase', uc_class)
    
    update_dto = UpdatePurchaseDTO(title='Test')
    purchase_id = uuid4()
    
    with pytest.raises(BadRequest) as exc_info:
        controller.update_purchase(purchase_id, update_dto)
    
    assert 'Purchase not found' in str(exc_info.value)


# Subscription get, update, and delete tests

def test_get_subscription_success(
    controller: ExpenseController,
    expense_response_dto: ExpenseResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionGetOneUseCase', uc_class)
    
    subscription_id = uuid4()
    result = controller.get_subscription(subscription_id)
    
    assert isinstance(result, ExpenseResponseDTO)
    uc_instance.execute.assert_called_once_with(subscription_id)


def test_get_subscription_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Subscription not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionGetOneUseCase', uc_class)
    
    subscription_id = uuid4()
    
    with pytest.raises(NotFound) as exc_info:
        controller.get_subscription(subscription_id)
    
    assert 'Subscription not found' in str(exc_info.value)


def test_update_subscription_success(
    controller: ExpenseController,
    expense_response_dto: ExpenseResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = expense_response_dto
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionUpdateUseCase', uc_class)
    
    update_dto = UpdateSubscriptionDTO(title='Updated Subscription', amount=20.0)
    subscription_id = uuid4()
    result = controller.update_subscription(subscription_id, update_dto)
    
    assert isinstance(result, ExpenseResponseDTO)
    uc_instance.execute.assert_called_once_with(subscription_id, update_dto)


def test_update_subscription_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Subscription not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionUpdateUseCase', uc_class)
    
    update_dto = UpdateSubscriptionDTO(title='Test')
    subscription_id = uuid4()
    
    with pytest.raises(BadRequest) as exc_info:
        controller.update_subscription(subscription_id, update_dto)
    
    assert 'Subscription not found' in str(exc_info.value)


def test_delete_subscription_success(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.return_value = None
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionDeleteUseCase', uc_class)
    
    subscription_id = uuid4()
    result = controller.delete_subscription(subscription_id)
    
    assert result is None
    uc_instance.execute.assert_called_once_with(subscription_id)


def test_delete_subscription_not_found(
    controller: ExpenseController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock use case to raise ValueError
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Subscription not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.expense_controller.SubscriptionDeleteUseCase', uc_class)
    
    subscription_id = uuid4()
    
    with pytest.raises(NotFound) as exc_info:
        controller.delete_subscription(subscription_id)
    
    assert 'Subscription not found' in str(exc_info.value)


