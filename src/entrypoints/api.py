from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from .routes import router_api
from src.entrypoints.middlewares.jwt_middleware import JWTMiddleware

origins = [
    'https://smw.juanpanasiti.com.ar',
    'http://localhost:5173',
]

api_middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r'https://smw.*\.(netlify\.app|juanpanasiti\.com\.ar)',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['renewed-token'],
    ),
    Middleware(JWTMiddleware),
]

app = FastAPI(
    title='Save My Wallet API',
    description='API for Save My Wallet application',
    version='3.0.0 beta',
    middleware=api_middlewares,
    routes=router_api.routes,
)

