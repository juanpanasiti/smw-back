from fastapi import APIRouter

from .credit_card_routes import router as credit_card_router
from .expense_routes import router as expense_router
from .purchase_routes import router as purchase_router

router_v2 = APIRouter(prefix='/v2')

router_v2.include_router(credit_card_router, tags=['Credit Cards'])
router_v2.include_router(expense_router, tags=['Expenses'])
router_v2.include_router(purchase_router, tags=['Purchases'])
