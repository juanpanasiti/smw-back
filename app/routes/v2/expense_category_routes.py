from typing import List

from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_category_schemas import NewExpenseCategoryReq, UpdateExpenseCategoryReq, ExpenseCategoryRes
from app.schemas.auth_schemas import DecodedJWT
from app.controllers import ExpenseCategoryController


router = APIRouter(prefix='/expenses/categories')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
expense_category_controller = ExpenseCategoryController()


@router.post(
    '',
    status_code=201,
)
async def create_new_expense_category(
    expense_category: NewExpenseCategoryReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseCategoryRes:
    return expense_category_controller.create(token, expense_category)


@router.get(
    ''
)
async def get_list(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> List[ExpenseCategoryRes]:
    return expense_category_controller.get_list(token)


@router.get(
    '/{expense_category_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def get_by_id(
    expense_category_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseCategoryRes:
    return expense_category_controller.get_by_id(token, expense_category_id)


# update expense category
@router.patch(
    '/{expense_category_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def update(
    expense_category: UpdateExpenseCategoryReq,
    expense_category_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseCategoryRes:
    return expense_category_controller.update(token, expense_category_id, expense_category)

# delete
@router.delete(
    '/{expense_category_id}',
    status_code=204,
    responses={
        404: ce.NotFound.dict()
    }
)
async def delete(
    expense_category_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> None:
    expense_category_controller.delete_one(token, expense_category_id)