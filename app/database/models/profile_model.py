from sqlalchemy import String, Integer, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class ProfileModel(BaseModel):
    __tablename__ = 'profiles'

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    # PKs
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
