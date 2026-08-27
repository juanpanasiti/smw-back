from uuid import UUID
from fastapi import APIRouter, Depends, Query

from src.application.dtos import (
    CreateBillGroupDTO,
    UpdateBillGroupDTO,
    BillGroupResponseDTO,
    BillGroupSummaryDTO,
    DecodedJWT,
    PaginatedResponse,
)
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import BillGroupController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import BillGroupRepositorySQL
from src.infrastructure.database.models import BillGroupModel
from src.infrastructure.database import db_conn

router = APIRouter(prefix='/bill-groups')
controller = BillGroupController(
    bill_group_repository=BillGroupRepositorySQL(
        model=BillGroupModel,
        session_factory=db_conn.SessionLocal,
    )
)


@router.post('', response_model=BillGroupResponseDTO, status_code=201)
def create_bill_group(
    data: CreateBillGroupDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillGroupResponseDTO:
    """Create a new bill group."""
    # Override owner_id with authenticated user
    data.owner_id = token.user_id
    return controller.create_bill_group(data)


@router.get('', response_model=PaginatedResponse[BillGroupResponseDTO])
def get_paginated_bill_groups(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PaginatedResponse[BillGroupResponseDTO]:
    """Get a paginated list of bill groups for the authenticated user."""
    filter_dict = {'owner_id': token.user_id}
    return controller.get_paginated_bill_groups(filter_dict, limit, offset)


@router.get('/{bill_group_id}', response_model=BillGroupResponseDTO)
def get_bill_group(
    bill_group_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillGroupResponseDTO:
    """Get a bill group by ID."""
    return controller.get_bill_group(bill_group_id)


@router.get('/{bill_group_id}/summary', response_model=BillGroupSummaryDTO)
def get_bill_group_summary(
    bill_group_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillGroupSummaryDTO:
    """Get a summary of a bill group with bills grouped by frequency."""
    return controller.get_bill_group_summary(bill_group_id)


@router.put('/{bill_group_id}', response_model=BillGroupResponseDTO)
def update_bill_group(
    bill_group_id: UUID,
    data: UpdateBillGroupDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> BillGroupResponseDTO:
    """Update a bill group."""
    return controller.update_bill_group(bill_group_id, data)


@router.delete('/{bill_group_id}', status_code=204)
def delete_bill_group(
    bill_group_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    """Delete a bill group."""
    controller.delete_bill_group(bill_group_id)
