from datetime import datetime
from pydantic import BaseModel, EmailStr

from .user_schemas_old import UserRes
from app.core.enums.role_enum import RoleEnum


class LoginUser(BaseModel):
    username: str
    password: str


class RegisterUser(LoginUser):
    email: EmailStr
    first_name: str
    last_name: str


class TokenResponse(UserRes):
    access_token: str = ''
    token_type: str = 'bearer'

class DecodedJWT(BaseModel):
    user_id: int
    role: RoleEnum
    exp: datetime
