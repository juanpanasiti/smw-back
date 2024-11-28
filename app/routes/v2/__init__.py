from fastapi import APIRouter

from .credit_card_routes import router as credit_card_router

router_v2 = APIRouter(prefix='/v2')

router_v2.include_router(credit_card_router, tags=['Credit Cards'])
