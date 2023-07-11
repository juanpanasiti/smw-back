from fastapi import APIRouter

from .auth_routes import router as auth_router

# Router
router_v1 = APIRouter(prefix='/v1')

# Include Routers
router_v1.include_router(auth_router)
