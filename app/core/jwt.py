from datetime import datetime, timedelta
from typing import Optional

import jwt

from . import settings
from app.exceptions.client_exceptions import Unauthorized


class JWTManager():
    def __init__(self) -> None:
        self.secret_key: str = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)

    def encode(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.expires_delta

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Unauthorized(message='Token has expired')
        except jwt.InvalidSignatureError:
            raise Unauthorized(message='Token signature is invalid')
        except jwt.InvalidTokenError:
            raise Unauthorized(message='Token is invalid')

jwt_manager = JWTManager()