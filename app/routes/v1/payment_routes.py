from typing import List

from fastapi import APIRouter, Depends, Query, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.payment_controller_v1 import PaymentControllerV1
from app.core.enums.role_enum import ALL_ROLES, ADMIN_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.payment_schemas_v1 import PaymentReqV1, PaymentResV1, NewPaymentReqV1, UpdatePaymentReqV1, PaymentUpdateQueryParamsV1
from app.schemas.auth_schemas import DecodedJWT


router = APIRouter(prefix='/expenses/{expense_id}/payments')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
controller = PaymentControllerV1()


@router.post(
    '/',
    status_code=201,
)
async def create(
    payment: NewPaymentReqV1,
    expense_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentResV1:
    return controller.create_subscription_payment(expense_id, payment)


@router.get(
    '/',
)
async def get_all(
    expense_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> List[PaymentResV1]:
    return controller.get_all(expense_id)


@router.get(
    '/{payment_id}'
)
async def get_by_id(
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentResV1:
    return controller.get_by_id(expense_id, payment_id)


@router.put('/{payment_id}')
async def update(
    payment: UpdatePaymentReqV1,
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    params: PaymentUpdateQueryParamsV1 = Depends()
) -> PaymentResV1:
    return controller.update(expense_id, payment_id, payment, params)


@router.delete('/{payment_id}', status_code=204)
async def delete_one(
    expense_id: int = Path(ge=1),
    payment_id: int = Path(ge=1),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one(expense_id, payment_id)
