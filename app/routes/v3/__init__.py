from fastapi import APIRouter

from .credit_card_routes import router as credit_card_router

router_v3 = APIRouter(prefix='/v3')

router_v3.include_router(credit_card_router, tags=['Credit Cards'])

