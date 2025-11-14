from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.domain.auth.enums.role import Role


class RegisterUserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.FREE_USER
    first_name: str
    last_name: str


class LoginUserDTO(BaseModel):
    username: str
    password: str


class LoggedInUserDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: Role
    access_token: str = ''
    token_type: str = 'bearer'


class DecodedJWT(BaseModel):
    sub: str  # User ID as string (UUID)
    role: Role
    email: EmailStr
    exp: datetime

    @property
    def user_id(self) -> UUID:
        """Parse sub field as UUID."""
        return UUID(self.sub)
