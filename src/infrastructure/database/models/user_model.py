from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base_model import BaseModel
from .profile_model import ProfileModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relationships
    profile: Mapped['ProfileModel'] = relationship('ProfileModel', back_populates='user', uselist=False, cascade='all, delete-orphan')


    def __repr__(self) -> str:
        return f'<UserModel id={self.id} email={self.email}>'