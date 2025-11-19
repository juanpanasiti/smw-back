from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.domain.auth import Role
from src.application.helpers.security import decode_jwt
from src.application.dtos import DecodedJWT
from src.entrypoints.exceptions import Forbidden, Unauthorized
from src.config import settings
from src.common.exceptions import JWTExpiredError, JWTInvalidSignatureError, JWTInvalidError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v3/auth/oauth')


def has_permission(allowed_roles: list[Role] = []):
    async def get_token_payload(authorization=Depends(oauth2_scheme)) -> DecodedJWT:
        try:
            payload = decode_jwt(
                token=authorization,
                secret=settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM,
            )

            if len(allowed_roles) > 0 and payload['role'] not in [role.value for role in allowed_roles]:
                raise Forbidden('You have no access to this resource.', 'USER_FORBIDDEN')
            return DecodedJWT(**payload)
        except (JWTExpiredError, JWTInvalidSignatureError, JWTInvalidError) as e:
            raise Unauthorized(str(e), e.code)
        except InvalidTokenError as e:
            raise Unauthorized('Invalid token', 'TOKEN_INVALID_ERROR')
    return get_token_payload
