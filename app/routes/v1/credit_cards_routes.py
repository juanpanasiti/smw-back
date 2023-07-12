from typing import List

from fastapi import APIRouter, Depends, Query

from app.dependencies.auth_dependencies import has_permission
from app.controllers.credit_card_controller import CreditCardController
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.credit_card_schemas import NewCreditCardReq, CreditCardRes, CreditCardReq
from app.schemas.auth_schemas import DecodedJWT


router = APIRouter(prefix='/credit_cards')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
controller = CreditCardController()

@router.post(
    '/',
    status_code=201,
)
async def create(
    credit_card: NewCreditCardReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.create(token.user_id, credit_card)