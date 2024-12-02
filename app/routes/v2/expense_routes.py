from fastapi import APIRouter, Depends, Path
from typing import List

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas import NewExpenseReq, UpdateExpenseReq, ExpenseRes, ExpenseListParam
from app.schemas.auth_schemas import DecodedJWT
from app.controllers import ExpenseController

router = APIRouter(prefix='/expenses')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
expense_controller = ExpenseController()


@router.post(
    '',
    status_code=201,
)
async def create_new_expense(
    expense: NewExpenseReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseRes:
    return expense_controller.create(token, expense)


@router.get(
    ''
)
async def get_list(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    account_id: int | None = None,
    params: ExpenseListParam = Depends(),
) -> List[ExpenseRes]:
    return expense_controller.get_list(token, account_id, params)


@router.get(
    '/{expense_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def get_by_id(
    expense_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseRes:
    return expense_controller.get_by_id(token, expense_id)


@router.patch(
    '/{expense_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def update(
    expense: UpdateExpenseReq,
    expense_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseRes:
    return expense_controller.update(token, expense_id, expense)


@router.delete(
    '/{expense_id}',
    status_code=204,
    responses={
        404: ce.NotFound.dict()
    }
)
async def delete(
    expense_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> None:
    expense_controller.delete_one(token, expense_id)
