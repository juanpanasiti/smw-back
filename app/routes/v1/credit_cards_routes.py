from typing import List

from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.credit_card_controller import CreditCardController
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.credit_card_schemas import CreditCardRes, CreditCardReq
from app.schemas.expense_schemas import NewPurchaseReq, PurchaseReq, PurchaseRes
from app.schemas.expense_schemas import NewSubscriptionReq, SubscriptionReq, SubscriptionRes
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

# !---------------------------------------------------! #
# ! CREDIT CARD EXPENSES (Purchases and Subscriptions)! #
# !---------------------------------------------------! #


@router.post(
    '/{cc_id}/purchases/',
    status_code=201,
    tags=['Expenses', 'Purchases'],
)
async def create_new_purchase(
    purchase_data: NewPurchaseReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PurchaseRes:
    return controller.create_new_purchase(token.user_id, cc_id, purchase_data)


@router.post(
    '/{cc_id}/subscriptions/',
    status_code=201,
    tags=['Expenses', 'Subscriptions'],
)
async def create_new_subscription(
    subscription_data: NewSubscriptionReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> SubscriptionRes:
    return controller.create_new_subscription(token.user_id, cc_id, subscription_data)


@router.get(
    '/{cc_id}/purchases/',
    tags=['Expenses', 'Purchases'],
)
async def get_all_purchases(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    cc_id: int = Path(ge=1),
) -> List[PurchaseRes]:
    return controller.get_all_purchases(token.user_id, cc_id)


@router.get(
    '/{cc_id}/subscriptions/',
    tags=['Expenses', 'Subscriptions'],
)
async def get_all_subscriptions(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    cc_id: int = Path(ge=1),
) -> List[SubscriptionRes]:
    return controller.get_all_subscriptions(token.user_id, cc_id)


@router.get(
    '/{cc_id}/purchases/{purchase_id}/',
    tags=['Expenses', 'Purchases'],
)
async def get_purchase_by_id(
    cc_id: int = Path(ge=1),
    purchase_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> PurchaseRes:
    return controller.get_purchase_by_id(token.user_id, cc_id, purchase_id)


@router.get(
    '/{cc_id}/subscriptions/{subscription_id}/',
    tags=['Expenses', 'Subscriptions'],
)
async def get_subscription_by_id(
    cc_id: int = Path(ge=1),
    subscription_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> SubscriptionRes:
    return controller.get_subscription_by_id(token.user_id, cc_id, subscription_id)


@router.put(
    '/{cc_id}/purchases/{purchase_id}/',
    tags=['Expenses', 'Purchases'],
)
async def update_purchase(
    purchase: PurchaseReq,
    cc_id: int = Path(ge=1),
    purchase_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> PurchaseRes:
    return controller.update_purchase(token.user_id, cc_id, purchase_id, purchase)


@router.put(
    '/{cc_id}/subscriptions/{subscription_id}/',
    tags=['Expenses', 'Subscriptions'],
)
async def update_subscription(
    subscription: SubscriptionReq,
    cc_id: int = Path(ge=1),
    subscription_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> SubscriptionRes:
    return controller.update_subscription(token.user_id, cc_id, subscription_id, subscription)


@router.delete(
    '/{cc_id}/purchases/{purchase_id}/',
    status_code=204,
    tags=['Expenses', 'Purchases'],
)
async def delete_one_purchase(
    cc_id: int = Path(ge=1),
    purchase_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one_purchase(token.user_id, cc_id, purchase_id)


@router.delete(
    '/{cc_id}/subscriptions/{subscription_id}/',
    status_code=204,
    tags=['Expenses', 'Subscriptions'],
)
async def delete_one_subscription(
    cc_id: int = Path(ge=1),
    subscription_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one_subscription(token.user_id, cc_id, subscription_id)
