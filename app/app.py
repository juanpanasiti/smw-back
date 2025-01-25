from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.jwt_middleware import JWTMiddleware
from app.routes import api_router
from .database import db_conn
from app.core.api_doc import api_description

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

app = FastAPI(**api_description, middleware=api_middlewares)

app.include_router(api_router)


@app.on_event('startup')
async def startup_event():
    db_conn.connect()


@app.on_event('shutdown')
async def shutdown_event():
    db_conn.disconnect()
