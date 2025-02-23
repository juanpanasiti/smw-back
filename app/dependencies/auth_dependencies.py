from typing import List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.enums.role_enum import RoleEnum as Role
from app.core.jwt import jwt_manager
from app.exceptions.client_exceptions import Forbidden, Unauthorized
from app.schemas.auth_schemas import DecodedJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def has_permission(allowed_roles: List[Role] = []):
    async def get_token_payload(authorization=Depends(oauth2_scheme)) -> DecodedJWT:
        try:
            payload = jwt_manager.decode(authorization)

            if len(allowed_roles) > 0 and payload['role'] not in [role.value for role in allowed_roles]:
                raise Forbidden('You have no access to this resource.', 'USER_FORBIDDEN')
            return DecodedJWT(**payload)
        except InvalidTokenError:
            raise Unauthorized('Invalid token', 'TOKEN_INVALID_ERROR')
    return get_token_payload
