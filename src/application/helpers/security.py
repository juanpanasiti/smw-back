from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

from src.common.exceptions import JWTExpiredError, JWTInvalidError, JWTInvalidSignatureError


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
