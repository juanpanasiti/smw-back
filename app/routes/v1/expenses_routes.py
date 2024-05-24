from fastapi import APIRouter, Depends

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas import ExepenseListResponse, ExpenseReq, ExpenseRes
from app.schemas.query_params_schemas import PaginateParams
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
    pagination: PaginateParams = Depends(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExepenseListResponse:
    return controller.get_all(token.user_id)

@router.post(
    '/',
    status_code=201,
)
async def create_new_expense(
    new_expense: ExpenseReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseRes:
    return controller.create(token.user_id, new_expense)