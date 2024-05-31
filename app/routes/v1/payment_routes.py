from typing import List

from fastapi import APIRouter, Depends, Query, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.payment_controller import PaymentController
from app.core.enums.role_enum import ALL_ROLES, ADMIN_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.payment_schemas import PaymentReq, PaymentRes, NewPaymentReq, UpdatePaymentReq, PaymentUpdateQueryParams
from app.schemas.auth_schemas import DecodedJWT


router = APIRouter(prefix='/expenses/{expense_id}/payments')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
controller = PaymentController()


@router.post(
    '/',
    status_code=201,
)
async def create(
    payment: NewPaymentReq,
    expense_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentRes:
    return controller.create_subscription_payment(expense_id, payment)


@router.get(
    '/',
)
async def get_all(
    expense_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> List[PaymentRes]:
    return controller.get_all(expense_id)


@router.get(
    '/{payment_id}'
)
async def get_by_id(
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentRes:
    return controller.get_by_id(expense_id, payment_id)


@router.put('/{payment_id}')
async def update(
    payment: UpdatePaymentReq,
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    params: PaymentUpdateQueryParams = Depends()
) -> PaymentRes:
    return controller.update(expense_id, payment_id, payment, params)


@router.delete('/{payment_id}', status_code=204)
async def delete_one(
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one(expense_id, payment_id)
