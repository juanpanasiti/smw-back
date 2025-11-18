from uuid import UUID
from fastapi import APIRouter, Depends, Query

from src.application.dtos import (
    CreateCreditCardDTO,
    UpdateCreditCardDTO,
    CreditCardResponseDTO,
    DecodedJWT,
    PaginatedResponse,
)
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import AccountController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import CreditCardRepositorySQL
from src.infrastructure.database.models import CreditCardModel
from src.infrastructure.database import db_conn

router = APIRouter(prefix='/credit-cards')
controller = AccountController(
    credit_card_repository=CreditCardRepositorySQL(
        model=CreditCardModel,
        session_factory=db_conn.SessionLocal,
    )
)


@router.post('', response_model=CreditCardResponseDTO, status_code=201)
def create_credit_card(
    data: CreateCreditCardDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CreditCardResponseDTO:
    """Create a new credit card."""
    return controller.create_credit_card(data)


@router.get('/{credit_card_id}', response_model=CreditCardResponseDTO)
def get_credit_card(
    credit_card_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CreditCardResponseDTO:
    """Get a credit card by ID."""
    return controller.get_credit_card(credit_card_id)


@router.put('/{credit_card_id}', response_model=CreditCardResponseDTO)
def update_credit_card(
    credit_card_id: UUID,
    data: UpdateCreditCardDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CreditCardResponseDTO:
    """Update a credit card."""
    return controller.update_credit_card(credit_card_id, data)


@router.delete('/{credit_card_id}', status_code=204)
def delete_credit_card(
    credit_card_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a credit card."""
    controller.delete_credit_card(credit_card_id)


@router.get('', response_model=PaginatedResponse[CreditCardResponseDTO])
def get_paginated_credit_cards(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaginatedResponse[CreditCardResponseDTO]:
    """Get a paginated list of credit cards."""
    filter_dict = {'owner_id': token.user_id}
    return controller.get_paginated_credit_cards(filter_dict, limit, offset)
