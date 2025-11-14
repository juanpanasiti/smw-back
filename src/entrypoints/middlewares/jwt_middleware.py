import json
import time
from datetime import timedelta

from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from src.config import settings
from src.application.helpers.security import decode_jwt, encode_jwt


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get('Authorization')
        response = await call_next(request)
        

        if token is None or not token.startswith('Bearer'):
            return response

        try:
            jwt = decode_jwt(token.split(' ')[1], settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            exp_timestamp = jwt["exp"]

            current_timestamp = int(time.time())
            time_left = (exp_timestamp - current_timestamp) // 60
            if time_left < (settings.JWT_EXPIRATION_TIME_MINUTES*0.5):
                del jwt['exp']
                expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
                new_token = encode_jwt(jwt, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, expires_delta)
                response.headers['renewed-token'] = new_token
        except HTTPException as ex:
            return Response(content=json.dumps({'error': ex.detail}), status_code=ex.status_code)
        except Exception:
            return Response(content=json.dumps({'error': 'Error al procesar el token'}), status_code=500)

        return response