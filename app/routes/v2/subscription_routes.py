from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas_v2 import PaymentResV2
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.payment_schemas_v2 import NewSubscriptionPaymentReqV2, UpdateSubscriptionPaymentReqV2, PaymentResV2
from app.controllers import SubscriptionControllerV2

router = APIRouter(prefix='/subscriptions/{subscription_id}')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
subscription_controller = SubscriptionControllerV2()


@router.post(
    '/payments',
    status_code=201,
)
async def add_new_payment_to_subscription(
    payment: NewSubscriptionPaymentReqV2,
    subscription_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentResV2:
    return subscription_controller.create(token, subscription_id, payment)


@router.patch(
    '/payments/{payment_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def update(
    payment: UpdateSubscriptionPaymentReqV2,
    subscription_id: int = Path(),
    payment_id: int = Path(),
    _: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PaymentResV2:
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
