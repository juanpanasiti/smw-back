from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator

from app.core.enums.role_enum import RoleEnum
from .profile_schemas_old import ProfileRes


class NewUserReq(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes=True

    @field_validator('username')
    def username_is_valid(cls, value: str):
        if not value:
            raise ValueError('Username cannot be empty')
        if value[0].isdigit():
            raise ValueError('Username must not start with a number')
        if not all(c.isalnum() or c == '_' for c in value):
            raise ValueError(
                'Username must contain only letters, numbers and underscores')
        if not 5 <= len(value) <= 15:
            raise ValueError(
                'Username length must be between 5 and 15 characters')
        return value
    
    @field_validator('password')
    def password_is_valid(cls, value):
        if not value:
            raise ValueError('Password cannot be empty')
        if not 8 <= len(value) <= 32:
            raise ValueError(
                'Password length must be between 8 and 32 characters')
        return value


class UserRes(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    profile: ProfileRes
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True
