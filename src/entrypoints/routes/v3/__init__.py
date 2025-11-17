from fastapi import APIRouter
from .auth_routes import router as auth_router
from .account_routes import router as account_router
from .user_routes import router as user_router
from .expense_routes import (
    category_router,
    purchase_router,
    subscription_router,
    expense_router,
)
from .period_routes import router as period_router


router_v3 = APIRouter(prefix='/v3')

router_v3.include_router(auth_router, tags=['auth'])
router_v3.include_router(account_router, tags=['account'])
router_v3.include_router(user_router, tags=['users'])
router_v3.include_router(category_router, tags=['expense-categories'])
router_v3.include_router(purchase_router, tags=['purchases'])
router_v3.include_router(subscription_router, tags=['subscriptions'])
router_v3.include_router(expense_router, tags=['expenses'])
router_v3.include_router(period_router, tags=['periods'])
