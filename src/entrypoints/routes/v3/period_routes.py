from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Path

from src.application.dtos import (
    PeriodResponseDTO,
    PeriodSummaryDTO,
    DecodedJWT,
)
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import PeriodController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import CreditCardRepositorySQL
from src.infrastructure.database.models import CreditCardModel
from src.infrastructure.database import db_conn


router = APIRouter(prefix='/periods', tags=['periods'])

controller = PeriodController(
    credit_card_repository=CreditCardRepositorySQL(
        model=CreditCardModel,
        session_factory=db_conn.SessionLocal,
    ),
)


@router.get('/current', response_model=PeriodResponseDTO)
def get_current_period(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PeriodResponseDTO:
    """
    Get the current period (current month).
    
    Returns:
        PeriodResponseDTO with all payments for the current month
    """
    today = date.today()
    return controller.get_period(token.user_id, today.month, today.year)


@router.get('/projection', response_model=list[PeriodResponseDTO])
def get_periods_projection(
    months_ahead: int = Query(12, ge=1, le=24, description="Months to project ahead"),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> list[PeriodResponseDTO]:
    """
    Get future period projection with complete payments for charts.
    
    Useful for:
    - Visualizing future expense evolution
    - Financial planning
    - Bar/line charts
    - Detailed analysis of future payments
    
    Args:
        months_ahead: Number of months ahead (1-24, default: 12)
        
    Returns:
        List of PeriodResponseDTO with enriched payments for each period
    """
    return controller.get_periods_projection(token.user_id, months_ahead)


@router.get('/{month}/{year}', response_model=PeriodResponseDTO)
def get_period(
    month: int = Path(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Path(..., ge=2020, description="Year"),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PeriodResponseDTO:
    """
    Get a specific period with all enriched payments.
    
    Includes:
    - Payment data (amount, status, date)
    - Expense data (title, type, total installments)
    - Account data (card alias, type)
    - Category data (if exists)
    
    Enriched payments allow frontend filtering by:
    - Credit card
    - Payment status
    - Category
    - Expense type
    
    Args:
        month: Period month (1-12)
        year: Period year (>= 2020)
        
    Returns:
        PeriodResponseDTO with enriched payments and calculated amounts
    """
    return controller.get_period(token.user_id, month, year)
