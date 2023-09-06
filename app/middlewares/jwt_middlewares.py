import json
import time

from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from app.core import settings
from app.core.jwt import JWTManager


class JWTMiddlewares(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.jwt_manager = JWTManager()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get('Authorization')
        response = await call_next(request)

        if token is None or not token.startswith('Bearer'):
            return response

        try:
            jwt = self.jwt_manager.decode(token.split(' ')[1])
            exp_timestamp = jwt["exp"]

            current_timestamp = int(time.time())
            time_left = (exp_timestamp - current_timestamp) // 60
            if time_left < (settings.JWT_EXPIRATION_TIME_MINUTES*0.5):
                del jwt['exp']
                new_token = self.jwt_manager.encode(jwt)
                response.headers['renewed-token'] = new_token
        except HTTPException as ex:
            return Response(content=json.dumps({'error': ex.detail}), status_code=ex.status_code)
        except Exception:
            return Response(content=json.dumps({'error': 'Error al procesar el token'}), status_code=500)

        return response
