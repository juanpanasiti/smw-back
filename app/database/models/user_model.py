from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.role_enum import RoleEnum

class UserModel(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(64), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(Enum(RoleEnum), default=RoleEnum.COMMON, nullable=False)

    def __str__(self) -> str:
        return f'User {self.username} ({self.email})'

    def __repr__(self) -> str:
        return f'User {self.username} ({self.email})'
