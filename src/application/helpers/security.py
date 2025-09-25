from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

from src.common.exceptions import JWTExpiredError, JWTInvalidError, JWTInvalidSignatureError
from src.config import settings
from src.domain.auth import User


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def encode_jwt(data: dict, secret: str, algorithm: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(token: str, secret: str, algorithm: str) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTExpiredError()
    except jwt.InvalidSignatureError:
        raise JWTInvalidSignatureError()
    except jwt.InvalidTokenError:
        raise JWTInvalidError()


def create_access_token(user: User) -> str:
    expires = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
    payload = {
        'sub': str(user.id),
        'role': user.role,
        'email': user.email,
    }
    token = encode_jwt(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, expires)
    return token
