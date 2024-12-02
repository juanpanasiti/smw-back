from fastapi import APIRouter, Depends, Path
from typing import List

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas import PaymentRes
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.payment_schemas import NewSubscriptionPaymentReq, UpdateSubscriptionPaymentReq, PaymentRes
from app.controllers import SubscriptionController

router = APIRouter(prefix='/subscriptions/{subscription_id}')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
subscription_controller = SubscriptionController()


@router.post(
    '/payments',
    status_code=201,
)
async def add_new_payment_to_subscription(
    payment: NewSubscriptionPaymentReq,
    subscription_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentRes:
    return subscription_controller.create(token, subscription_id, payment)


@router.patch(
    '/payments/{payment_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def update(
    payment: UpdateSubscriptionPaymentReq,
    subscription_id: int = Path(),
    payment_id: int = Path(),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentRes:
    return subscription_controller.update(subscription_id, payment_id, payment)


@router.delete(
    '/payments/{payment_id}',
    status_code=204,
    responses={
        404: ce.NotFound.dict()
    }
)
async def delete(
    subscription_id: int = Path(),
    payment_id: int = Path(),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> None:
    subscription_controller.delete(subscription_id, payment_id)
