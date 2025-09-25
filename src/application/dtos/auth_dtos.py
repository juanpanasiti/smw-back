from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict

from src.domain.auth import Role


class RegisterUserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.FREE_USER
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class LoginUserDTO(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class LoggedInUserDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: Role
    access_token: str = ''
    token_type: str = 'bearer'

    model_config = ConfigDict(from_attributes=True)
