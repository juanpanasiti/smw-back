from typing import List

from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.credit_card_schemas import NewCreditCardReq, UpdateCreditCardReq, CreditCardRes, CreditCardListParam
from app.controllers import CreditCardController

router = APIRouter(prefix='/credit_cards')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
controller = CreditCardController()


@router.post(
    '',
    status_code=201,
)
async def create_new_credit_card(
    credit_card: NewCreditCardReq,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.create(token, credit_card)


@router.get('')
async def get_list(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    params: CreditCardListParam = Depends()
) -> List[CreditCardRes]:
    return controller.get_list(token, params)


@router.get(
    '/{cc_id}',
    responses={
        404: ce.NotFound.dict(),
    }
)
async def get_by_id(
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.get_by_id(token, cc_id)


@router.patch(
    '/{cc_id}',
    responses={
        404: ce.NotFound.dict(),
    }
)
async def update(
    credit_card: UpdateCreditCardReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CreditCardRes:
    return controller.update(token, cc_id, credit_card)


@router.delete(
    '/{cc_id}',
    status_code=204,
    responses={
        404: ce.NotFound.dict(),
    }
)
async def delete(
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> None:
    controller.delete_one(token, cc_id)
