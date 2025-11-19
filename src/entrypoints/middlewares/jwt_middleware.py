import json
import time
from datetime import timedelta

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.config import settings
from src.application.helpers.security import decode_jwt, encode_jwt
from src.common.exceptions import JWTExpiredError, JWTInvalidSignatureError, JWTInvalidError


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get('Authorization')
        
        # If no token or not Bearer format, just continue
        if token is None or not token.startswith('Bearer'):
            response = await call_next(request)
            return response

        try:
            jwt_payload = decode_jwt(token.split(' ')[1], settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            exp_timestamp = jwt_payload["exp"]

            current_timestamp = int(time.time())
            time_left = (exp_timestamp - current_timestamp) // 60
            
            # Process the request first
            response = await call_next(request)
            
            # Check if token needs renewal (less than 50% of lifetime remaining)
            if time_left < (settings.JWT_EXPIRATION_TIME_MINUTES * 0.5):
                # Get current renewal count (default to 0 if not present)
                renewal_count = jwt_payload.get('renewal_count', 0)
                
                # Check if we've reached the max renewals limit
                if renewal_count >= settings.JWT_MAX_RENEWALS:
                    # Signal frontend that refresh token is required
                    response.headers['X-Require-Refresh'] = 'true'
                else:
                    # Renew the token and increment renewal count
                    del jwt_payload['exp']
                    jwt_payload['renewal_count'] = renewal_count + 1
                    
                    expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
                    new_token = encode_jwt(
                        jwt_payload, 
                        settings.JWT_SECRET_KEY, 
                        settings.JWT_ALGORITHM, 
                        expires_delta
                    )
                    response.headers['renewed-token'] = new_token
            
            return response
                    
        except (JWTExpiredError, JWTInvalidSignatureError, JWTInvalidError) as ex:
            # Return consistent error format with code
            return Response(
                content=json.dumps({
                    'detail': {
                        'description': str(ex),
                        'code': ex.code
                    }
                }),
                status_code=401,
                media_type='application/json'
            )
        except Exception as ex:
            # For unexpected errors, return consistent format
            return Response(
                content=json.dumps({
                    'detail': {
                        'description': 'Error processing token',
                        'code': 'TOKEN_PROCESSING_ERROR'
                    }
                }),
                status_code=500,
                media_type='application/json'
            )