import bcrypt

from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.role_enum import RoleEnum


class UserModel(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    _hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(Enum(RoleEnum), default=RoleEnum.COMMON, nullable=False)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password.decode('utf-8')

    def __str__(self) -> str:
        return f'User {self.username} ({self.email}) [{self.role}]'

    def __repr__(self) -> str:
        return f'User {self.username} ({self.email}) [{self.role}]'
