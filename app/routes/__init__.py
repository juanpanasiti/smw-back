from fastapi import APIRouter

from .v1 import router_v1
from .v2 import router_v2
from .v3 import router_v3
from .root_routes import router as root_router

api_router = APIRouter()
api_router.include_router(root_router, include_in_schema=False)
api_router.include_router(router_v3, prefix='/api', tags=['V3'])
api_router.include_router(router_v2, prefix='/api', tags=['V2'])
api_router.include_router(router_v1, prefix='/api', tags=['V1'])
