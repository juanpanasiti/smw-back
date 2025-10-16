from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import router_api

app = FastAPI(
    title='Save My Wallet API',
    description='API for Save My Wallet application',
    version='3.0.0 beta',
)

app.include_router(router_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
