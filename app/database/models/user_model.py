import bcrypt

from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .profile_model import ProfileModel
from app.core.enums.role_enum import RoleEnum
from app.core.enums.user_status_enum import UserStatusEnum


class UserModel(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False)
    _password: Mapped[str] = mapped_column(
        'password', String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(
        Enum(RoleEnum), default=RoleEnum.COMMON, nullable=False)
    status: Mapped[str] = mapped_column(Enum(UserStatusEnum), default=UserStatusEnum.UNCONFIRMED, nullable=False)

    # Relations
    profile: Mapped['ProfileModel'] = relationship()

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self._password = password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self) -> str:
        return f'User {self.username} ({self.email}) [{self.role}]'

    def __repr__(self) -> str:
        return f'User {self.username} ({self.email}) [{self.role}]'
