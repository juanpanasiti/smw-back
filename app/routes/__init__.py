from fastapi import APIRouter

from .v1 import router_v1
from .root_routes import router as root_router

api_router = APIRouter()
api_router.include_router(root_router, include_in_schema=False)
api_router.include_router(router_v1, prefix='/api')
