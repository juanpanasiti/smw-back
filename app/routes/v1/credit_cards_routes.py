from typing import List

from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.credit_card_controller import CreditCardController
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.credit_card_schemas import CreditCardRes, CreditCardReq
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
    credit_card: CreditCardReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.create(token.user_id, credit_card)


@router.get(
    '/',
)
async def get_all(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> List[CreditCardRes]:
    return controller.get_all(token.user_id)


@router.get(
    '/{cc_id}'
)
async def get_by_id(
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.get_by_id(token.user_id, cc_id)


@router.put('/{cc_id}')
async def update(
    credit_card: CreditCardReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CreditCardRes:
    return controller.update(token.user_id, cc_id, credit_card)


@router.delete('/{cc_id}', status_code=204)
async def delete_one(
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one(token.user_id, cc_id)