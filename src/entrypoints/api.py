from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .routes import router_api
from src.entrypoints.middlewares.jwt_middleware import JWTMiddleware
from src.entrypoints.exceptions import BaseHTTPException

origins = [
    'https://smw.juanpanasiti.com.ar',
    'http://localhost:5173',
    'http://localhost:3000',  # Next.js default port
    'http://localhost:3001',  # Alternative port
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


# Exception handlers
@app.exception_handler(BaseHTTPException)
async def base_http_exception_handler(request: Request, exc: BaseHTTPException):
    """Handle custom HTTP exceptions with consistent format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle standard HTTP exceptions with error code"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": {
                "description": exc.detail,
                "code": f"HTTP_{exc.status_code}"
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with error code"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "description": "Validation error",
                "code": "VALIDATION_ERROR",
                "errors": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with error code"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": {
                "description": "Internal server error",
                "code": "INTERNAL_SERVER_ERROR"
            }
        }
    )

