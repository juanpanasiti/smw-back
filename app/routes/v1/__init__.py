from fastapi import APIRouter

from .auth_routes import router as auth_router
from .credit_cards_routes import router as credit_card_router

# Router
router_v1 = APIRouter(prefix='/v1')

# Include Routers
router_v1.include_router(auth_router)
router_v1.include_router(credit_card_router)
