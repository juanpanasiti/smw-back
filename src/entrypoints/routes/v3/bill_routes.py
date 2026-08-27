from uuid import UUID
from fastapi import APIRouter, Depends, Query

from src.application.dtos import (
    CreateBillDTO,
    UpdateBillDTO,
    UpdateBillNextDateDTO,
    BillResponseDTO,
    UpcomingBillDTO,
    DecodedJWT,
    PaginatedResponse,
)
from src.domain.auth.enums.role import ALL_ROLES
from src.domain.expense.enums import BillFrequency
from src.entrypoints.controllers import BillController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import BillRepositorySQL, BillGroupRepositorySQL
from src.infrastructure.database.models import ExpenseModel, BillGroupModel
from src.infrastructure.database import db_conn

router = APIRouter(prefix='/bills')


def get_controller() -> BillController:
    """Get controller instance with dependencies."""
    return BillController(
        bill_repository=BillRepositorySQL(
            model=ExpenseModel,
            session_factory=db_conn.SessionLocal,
        ),
        bill_group_repository=BillGroupRepositorySQL(
            model=BillGroupModel,
            session_factory=db_conn.SessionLocal,
        )
    )


@router.post('', response_model=BillResponseDTO, status_code=201)
def create_bill(
    data: CreateBillDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillResponseDTO:
    """Create a new bill."""
    controller = get_controller()
    return controller.create_bill(data)


@router.get('/upcoming', response_model=list[UpcomingBillDTO])
def get_upcoming_bills(
    year: int | None = Query(None, ge=2000, le=2100),
    month: int | None = Query(None, ge=1, le=12),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> list[UpcomingBillDTO]:
    """Get upcoming bills for the authenticated user for a specific period."""
    controller = get_controller()
    return controller.get_upcoming_bills(token.user_id, year, month)


@router.get('', response_model=PaginatedResponse[BillResponseDTO])
def get_paginated_bills(
    account_id: UUID | None = Query(None, description="Filter by BillGroup ID"),
    frequency: BillFrequency | None = Query(None, description="Filter by frequency"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaginatedResponse[BillResponseDTO]:
    """Get a paginated list of bills for the authenticated user."""
    filter_dict: dict = {'owner_id': token.user_id}
    if account_id:
        filter_dict['account_id'] = account_id
    if frequency:
        filter_dict['frequency'] = frequency.value
    
    controller = get_controller()
    return controller.get_paginated_bills(filter_dict, limit, offset)


@router.get('/{bill_id}', response_model=BillResponseDTO)
def get_bill(
    bill_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillResponseDTO:
    """Get a bill by ID."""
    controller = get_controller()
    return controller.get_bill(bill_id)


@router.put('/{bill_id}', response_model=BillResponseDTO)
def update_bill(
    bill_id: UUID,
    data: UpdateBillDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillResponseDTO:
    """Update a bill."""
    controller = get_controller()
    return controller.update_bill(bill_id, data)


@router.patch('/{bill_id}/next-date', response_model=BillResponseDTO)
def update_bill_next_date(
    bill_id: UUID,
    data: UpdateBillNextDateDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillResponseDTO:
    """Update only the next bill date for a bill."""
    controller = get_controller()
    return controller.update_bill_next_date(bill_id, data)


@router.delete('/{bill_id}', status_code=204)
def delete_bill(
    bill_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a bill."""
    controller = get_controller()
    controller.delete_bill(bill_id)
