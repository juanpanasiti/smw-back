from fastapi import APIRouter, Depends, Path
from typing import List

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas_old import NewExpenseReq, UpdateExpenseReq, ExpenseRes, ExpenseListParams
from app.schemas.auth_schemas import DecodedJWT
from app.controllers.expense_controller_old import ExpenseControllerOld

router = APIRouter(prefix='/expenses')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}

controller = ExpenseControllerOld()


@router.get(
    '/',
)
async def get_all(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    params: ExpenseListParams = Depends()
) -> List[ExpenseRes]:
    return controller.get_all(token.user_id, params)


@router.post(
    '/',
    status_code=201,
)
async def create_new_expense(
    new_expense: NewExpenseReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> ExpenseRes:
    return controller.create(token.user_id, new_expense)


@router.get(
    '/{id}',
)
async def get_by_id(
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    id: int = Path(ge=1),
) -> ExpenseRes:
    return controller.get_by_id(id)

@router.put(
    '/{id}',
)
async def update(
    expense: UpdateExpenseReq,
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    id: int = Path(ge=1),
) -> ExpenseRes:
    return controller.update(id, expense)

@router.patch(
    '/{id}/disable',
    status_code=204,
)
async def disable(
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    id: int = Path(ge=1),
) -> None:
    return controller.disable(id)

@router.patch(
    '/{id}/enable',
    status_code=204,
)
async def enable(
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    id: int = Path(ge=1),
) -> None:
    return controller.enable(id)

@router.delete(
    '/{id}',
    status_code=204,
)
async def delete(
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    id: int = Path(ge=1),
) -> None:
    return controller.delete(id)
