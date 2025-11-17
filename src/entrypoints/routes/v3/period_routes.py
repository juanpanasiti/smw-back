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
    Obtiene el período actual (mes corriente).
    
    Returns:
        PeriodResponseDTO con todos los payments del mes actual
    """
    today = date.today()
    return controller.get_period(token.user_id, today.month, today.year)


@router.get('/projection', response_model=list[PeriodResponseDTO])
def get_periods_projection(
    months_ahead: int = Query(12, ge=1, le=24, description="Months to project ahead"),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> list[PeriodResponseDTO]:
    """
    Obtiene proyección de períodos futuros con payments completos para gráficos.
    
    Útil para:
    - Visualizar evolución futura de gastos
    - Planificación financiera
    - Gráficos de barras/líneas
    - Análisis detallado de pagos futuros
    
    Args:
        months_ahead: Cantidad de meses hacia adelante (1-24, default: 12)
        
    Returns:
        Lista de PeriodResponseDTO con payments enriquecidos de cada período
    """
    return controller.get_periods_projection(token.user_id, months_ahead)


@router.get('/{month}/{year}', response_model=PeriodResponseDTO)
def get_period(
    month: int = Path(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Path(..., ge=2020, description="Year"),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PeriodResponseDTO:
    """
    Obtiene un período específico con todos sus payments enriquecidos.
    
    Incluye:
    - Datos del payment (monto, status, fecha)
    - Datos del expense (título, tipo, cuotas totales)
    - Datos de la account (alias de la tarjeta, tipo)
    - Datos de la categoría (si existe)
    
    Los payments enriquecidos permiten filtrar en el frontend por:
    - Tarjeta de crédito
    - Estado del pago
    - Categoría
    - Tipo de gasto
    
    Args:
        month: Mes del período (1-12)
        year: Año del período (>= 2020)
        
    Returns:
        PeriodResponseDTO con payments enriquecidos y montos calculados
    """
    return controller.get_period(token.user_id, month, year)
