from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas_v2 import ExpenseResV2
from app.schemas.payment_schemas_v2 import UpdatePurchasePaymentReqV2
from app.schemas.auth_schemas import DecodedJWT
from app.controllers import PurchaseControllerV2

router = APIRouter(prefix='/purchases/{purchase_id}/payments')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
purchase_controller = PurchaseControllerV2()


@router.patch(
    '/{payment_id}',
    responses={
        404: ce.NotFound.dict()
    }
)
async def update(
    payment: UpdatePurchasePaymentReqV2,
    purchase_id: int = Path(),
    payment_id: int = Path(),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> ExpenseResV2:
    return purchase_controller.update(token, purchase_id, payment_id, payment)
