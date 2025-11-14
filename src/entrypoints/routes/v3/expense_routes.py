from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query

from src.application.dtos import (
    CreateExpenseCategoryDTO,
    UpdateExpenseCategoryDTO,
    ExpenseCategoryResponseDTO,
    CreatePurchaseDTO,
    UpdatePurchaseDTO,
    CreateSubscriptionDTO,
    UpdateSubscriptionDTO,
    ExpenseResponseDTO,
    DecodedJWT,
    PaginatedResponse,
    CreatePaymentDTO,
    UpdatePaymentDTO,
    PaymentResponseDTO,
)
from src.domain.auth.enums.role import ALL_ROLES
from src.domain.expense.enums import ExpenseType
from src.entrypoints.controllers import ExpenseController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import (
    ExpenseCategoryRepositorySQL,
    ExpenseRepositorySQL,
    PaymentRepositorySQL,
)
from src.infrastructure.database.models import (
    ExpenseCategoryModel,
    ExpenseModel,
    PaymentModel,
)
from src.infrastructure.database import db_conn

# Expense Category Router
category_router = APIRouter(prefix='/expense-categories')
category_controller = ExpenseController(
    expense_category_repository=ExpenseCategoryRepositorySQL(ExpenseCategoryModel),
    expense_repository=ExpenseRepositorySQL(ExpenseModel),
    payment_repository=PaymentRepositorySQL(PaymentModel),
)


@category_router.post('', response_model=ExpenseCategoryResponseDTO, status_code=201)
def create_expense_category(
    data: CreateExpenseCategoryDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseCategoryResponseDTO:
    """Create a new expense category."""
    return category_controller.create_expense_category(data)


@category_router.put('/{category_id}', response_model=ExpenseCategoryResponseDTO)
def update_expense_category(
    category_id: UUID,
    data: UpdateExpenseCategoryDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseCategoryResponseDTO:
    """Update an expense category."""
    return category_controller.update_expense_category(category_id, data)


@category_router.delete('/{category_id}', status_code=204)
def delete_expense_category(
    category_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete an expense category."""
    category_controller.delete_expense_category(category_id)


@category_router.get('', response_model=PaginatedResponse[ExpenseCategoryResponseDTO])
def get_paginated_expense_categories(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaginatedResponse[ExpenseCategoryResponseDTO]:
    """Get a paginated list of expense categories."""
    filter_dict = {'owner_id': token.user_id}
    return category_controller.get_paginated_expense_categories(filter_dict, limit, offset)


# Purchase Router
purchase_router = APIRouter(prefix='/purchases')
purchase_controller = ExpenseController(
    expense_category_repository=ExpenseCategoryRepositorySQL(
        model=ExpenseCategoryModel,
        session_factory=db_conn.SessionLocal,
    ),
    expense_repository=ExpenseRepositorySQL(
        model=ExpenseModel,
        session_factory=db_conn.SessionLocal,
    ),
    payment_repository=PaymentRepositorySQL(
        model=PaymentModel,
        session_factory=db_conn.SessionLocal,
    ),
)


@purchase_router.post('', response_model=ExpenseResponseDTO, status_code=201)
def create_purchase(
    data: CreatePurchaseDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Create a new purchase."""
    return purchase_controller.create_purchase(data)


@purchase_router.get('/{purchase_id}', response_model=ExpenseResponseDTO)
def get_purchase(
    purchase_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Get a purchase by ID."""
    return purchase_controller.get_purchase(purchase_id)


@purchase_router.put('/{purchase_id}', response_model=ExpenseResponseDTO)
def update_purchase(
    purchase_id: UUID,
    data: UpdatePurchaseDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Update a purchase."""
    return purchase_controller.update_purchase(purchase_id, data)


@purchase_router.delete('/{purchase_id}', status_code=204)
def delete_purchase(
    purchase_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a purchase."""
    purchase_controller.delete_purchase(purchase_id)


# Subscription Router
subscription_router = APIRouter(prefix='/subscriptions')
subscription_controller = ExpenseController(
    expense_category_repository=ExpenseCategoryRepositorySQL(
        model=ExpenseCategoryModel,
        session_factory=db_conn.SessionLocal,
    ),
    expense_repository=ExpenseRepositorySQL(
        model=ExpenseModel,
        session_factory=db_conn.SessionLocal,
    ),
    payment_repository=PaymentRepositorySQL(
        model=PaymentModel,
        session_factory=db_conn.SessionLocal,
    ),
)


@subscription_router.post('', response_model=ExpenseResponseDTO, status_code=201)
def create_subscription(
    data: CreateSubscriptionDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Create a new subscription."""
    return subscription_controller.create_subscription(data)


@subscription_router.get('/{subscription_id}', response_model=ExpenseResponseDTO)
def get_subscription(
    subscription_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Get a subscription by ID."""
    return subscription_controller.get_subscription(subscription_id)


@subscription_router.put('/{subscription_id}', response_model=ExpenseResponseDTO)
def update_subscription(
    subscription_id: UUID,
    data: UpdateSubscriptionDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseResponseDTO:
    """Update a subscription."""
    return subscription_controller.update_subscription(subscription_id, data)


@subscription_router.delete('/{subscription_id}', status_code=204)
def delete_subscription(
    subscription_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a subscription."""
    subscription_controller.delete_subscription(subscription_id)


# General Expenses Router
expense_router = APIRouter(prefix='/expenses')
expense_controller = ExpenseController(
    expense_category_repository=ExpenseCategoryRepositorySQL(
        model=ExpenseCategoryModel,
        session_factory=db_conn.SessionLocal,
    ),
    expense_repository=ExpenseRepositorySQL(
        model=ExpenseModel,
        session_factory=db_conn.SessionLocal,
    ),
    payment_repository=PaymentRepositorySQL(
        model=PaymentModel,
        session_factory=db_conn.SessionLocal,
    ),
)


@expense_router.get('', response_model=PaginatedResponse[ExpenseResponseDTO])
def get_paginated_expenses(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    type: Optional[ExpenseType] = Query(None, description="Filter by expense type: 'purchase' or 'subscription'"),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaginatedResponse[ExpenseResponseDTO]:
    """Get a paginated list of expenses (purchases and subscriptions)."""
    filter_dict = {'owner_id': token.user_id}
    if type:
        filter_dict['expense_type'] = type.value
    return expense_controller.get_paginated_expenses(filter_dict, limit, offset)


# Payment endpoints for subscriptions
@subscription_router.post('/{subscription_id}/payments', response_model=PaymentResponseDTO, status_code=201)
def create_payment_for_subscription(
    subscription_id: UUID,
    data: CreatePaymentDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaymentResponseDTO:
    """Create a new payment for a subscription."""
    # Verificar que el expense_id del payment coincida con el subscription_id
    if data.expense_id != subscription_id:
        from src.entrypoints.exceptions.client_exceptions import BadRequest
        raise BadRequest('expense_id in payment data must match subscription_id', 'EXPENSE_ID_MISMATCH')
    return subscription_controller.create_payment(data)


@subscription_router.delete('/{subscription_id}/payments/{payment_id}', status_code=204)
def delete_payment_from_subscription(
    subscription_id: UUID,
    payment_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a payment from a subscription."""
    subscription_controller.delete_payment(payment_id)


# Payment endpoint for general expenses (both purchases and subscriptions)
@expense_router.put('/payments/{payment_id}', response_model=PaymentResponseDTO)
def update_payment(
    payment_id: UUID,
    data: UpdatePaymentDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaymentResponseDTO:
    """Update a payment (for both purchases and subscriptions)."""
    return expense_controller.update_payment(payment_id, data)
