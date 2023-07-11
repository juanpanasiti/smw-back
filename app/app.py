from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .api.middlewares.jwt_middlewares import JWTMiddlewares
# from .api.routes import api_router
from .database import db_conn
from app.core.api_doc import api_description
# from app.core.config import settings

app = FastAPI(**api_description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
# app.add_middleware(JWTMiddlewares)

# app.include_router(api_router)


@app.on_event('startup')
async def startup_event():
    db_conn.connect()


@app.on_event('shutdown')
async def shutdown_event():
    db_conn.disconnect()
