from pydantic import BaseModel

from app.core.enums.role_enum import RoleEnum


class UserSchemaBase(BaseModel):
    username: str
    email: str

class UserRequest(UserSchemaBase):
    email: str = ''
    password: str

class UserResponse(UserSchemaBase):
    id: int
    role: RoleEnum

