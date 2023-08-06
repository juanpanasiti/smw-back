from typing import List

from fastapi import APIRouter, Depends, Query, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.credit_card_controller import CreditCardController
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.credit_card_schemas import NewCreditCardReq, CreditCardRes, CreditCardReq
from app.schemas.credit_card_expense_schemas import NewCCPurchaseReq, CCPurchaseReq, CCPurchaseRes
from app.schemas.credit_card_expense_schemas import NewCCSubscriptionReq, CCSubscriptionReq, CCSubscriptionRes
from app.schemas.credit_card_statement_schemas import NewCCStatementReq, CCStatementReq, CCStatementRes
from app.schemas.statement_item_schemas import NewStatementItemReq, StatementItemReq, StatementItemRes
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


@router.get(
    '/',
)
async def get_paginated(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0,),
) -> List[CreditCardRes]:
    return controller.get_paginated(token.user_id, limit, offset)


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
    purchase_data: NewCCPurchaseReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCPurchaseRes:
    return controller.create_new_purchase(token.user_id, cc_id, purchase_data)


@router.post(
    '/{cc_id}/subscriptions/',
    status_code=201,
    tags=['Expenses', 'Subscriptions'],
)
async def create_new_subscription(
    subscription_data: NewCCSubscriptionReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCSubscriptionRes:
    return controller.create_new_subscription(token.user_id, cc_id, subscription_data)


@router.get(
    '/{cc_id}/purchases/',
    tags=['Expenses', 'Purchases'],
)
async def get_purchases_paginated(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    cc_id: int = Path(ge=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0,),
) -> List[CCPurchaseRes]:
    return controller.get_purchases_paginated(token.user_id, cc_id, limit, offset)


@router.get(
    '/{cc_id}/subscriptions/',
    tags=['Expenses', 'Subscriptions'],
)
async def get_subscriptions_paginated(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    cc_id: int = Path(ge=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0,),
) -> List[CCSubscriptionRes]:
    return controller.get_subscriptions_paginated(token.user_id, cc_id, limit, offset)


@router.get(
    '/{cc_id}/purchases/{purchase_id}/',
    tags=['Expenses', 'Purchases'],
)
async def get_by_id(
    cc_id: int = Path(ge=1),
    purchase_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CCPurchaseRes:
    return controller.get_purchase_by_id(token.user_id, cc_id, purchase_id)


@router.get(
    '/{cc_id}/subscriptions/{subscription_id}/',
    tags=['Expenses', 'Subscriptions'],
)
async def get_by_id(
    cc_id: int = Path(ge=1),
    subscription_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CCSubscriptionRes:
    return controller.get_subscription_by_id(token.user_id, cc_id, subscription_id)


@router.put(
    '/{cc_id}/purchases/{purchase_id}/',
    tags=['Expenses', 'Purchases'],
)
async def update_purchase(
    purchase: CCPurchaseReq,
    cc_id: int = Path(ge=1),
    purchase_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCPurchaseRes:
    return controller.update_purchase(token.user_id, cc_id, purchase_id, purchase)


@router.put(
    '/{cc_id}/subscriptions/{subscription_id}/',
    tags=['Expenses', 'Subscriptions'],
)
async def update_subscription(
    subscription: CCSubscriptionReq,
    cc_id: int = Path(ge=1),
    subscription_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCSubscriptionRes:
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

    # !-----------------------------------------! #
    # ! CREDIT CARD Statements and Installments ! #
    # !-----------------------------------------! #


@router.post(
    '/{cc_id}/statements/',
    status_code=201,
    tags=['Statements'],
)
async def create_new_statement(
    statement_data: NewCCStatementReq,
    cc_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCStatementRes:
    return controller.create_new_statement(token.user_id, cc_id, statement_data)


@router.get(
    '/{cc_id}/statements/',
    tags=['Statements'],
)
async def get_statements_paginated(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    cc_id: int = Path(ge=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0,),
) -> List[CCStatementRes]:
    return controller.get_statements_paginated(token.user_id, cc_id, limit, offset)


@router.get(
    '/{cc_id}/statements/{statement_id}/',
    tags=['Statements'],
)
async def get_statement_by_id(
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> CCStatementRes:
    return controller.get_statement_by_id(token.user_id, cc_id, statement_id)


@router.put(
    '/{cc_id}/statements/{statement_id}/',
    tags=['Statements'],
)
async def update_statement(
    statement: CCStatementReq,
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> CCStatementRes:
    return controller.update_statement(token.user_id, cc_id, statement_id, statement)


@router.delete(
    '/{cc_id}/statements/{statement_id}/',
    status_code=204,
    tags=['Statements'],
)
async def delete_one_statement(
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one_statement(token.user_id, cc_id, statement_id)


@router.post(
    '/{cc_id}/statements/{statement_id}/items/',
    status_code=201,
    tags=['Statements', 'Installments'],
)
async def create_new_installment(
    item_data: NewStatementItemReq,
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> StatementItemRes:
    return controller.create_new_installment(token.user_id, cc_id, statement_id, item_data)


@router.get(
    '/{cc_id}/statements/{statement_id}/items/{item_id}',
    tags=['Statements', 'Installments'],
)
async def get_installment_by_id(
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    item_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> StatementItemRes:
    return controller.get_installment_by_id(token.user_id, cc_id, statement_id, item_id)


@router.put(
    '/{cc_id}/statements/{statement_id}/items/{item_id}',
    tags=['Statements', 'Installments'],
)
async def update_installment(
    item: StatementItemReq,
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    item_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> StatementItemRes:
    return controller.update_installment(token.user_id, cc_id, statement_id, item_id, item)


@router.delete(
    '/{cc_id}/statements/{statement_id}/items/{item_id}',
    status_code=204,
    tags=['Statements', 'Installments'],
)
async def delete_one_installment(
    cc_id: int = Path(ge=1),
    statement_id: int = Path(ge=1),
    item_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> None:
    return controller.delete_one_installment(token.user_id, cc_id, statement_id, item_id)
