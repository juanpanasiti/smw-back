from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.core.enums.role_enum import RoleEnum


class NewUserReq(BaseModel):
    username: str
    password: str
    email: EmailStr

    class Config:
        from_attributes=True


class UserRes(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True
