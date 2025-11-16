from fastapi import APIRouter

from .v3 import router_v3


router_api = APIRouter(prefix='/api')

router_api.include_router(router_v3)
