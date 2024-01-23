from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas import ExepenseListResponse
from app.schemas.auth_schemas import DecodedJWT
from app.controllers.expense_controller import ExpenseController

router = APIRouter(prefix='/expenses')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}

controller = ExpenseController()

@router.get(
    '/',
)
async def get_all(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExepenseListResponse:
    return controller.get_all(token.user_id)
