from datetime import date

from sqlalchemy import UUID, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_model import UserModel  # Avoid circular import for type checking
    from .preferences_model import PreferencesModel  # Avoid circular import for type checking


class ProfileModel(BaseModel):
    __tablename__ = 'profiles'

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)

    # Relationships
    user: Mapped['UserModel'] = relationship('UserModel', back_populates='profile', uselist=False)
    preferences: Mapped['PreferencesModel'] = relationship('PreferencesModel', backref='profile', uselist=False, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<ProfileModel id={self.id} user_id={self.user_id}>'
