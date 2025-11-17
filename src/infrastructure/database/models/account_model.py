import uuid
from sqlalchemy import String, Boolean, ForeignKey, Numeric, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from . import BaseModel

if TYPE_CHECKING:
    from . import UserModel, ExpenseModel


class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[float] = mapped_column(Numeric(precision=20, scale=2), default=0.0, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    account_type: Mapped[str] = mapped_column('type', String(20), nullable=False)

    # FKs
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Relationships
    owner: Mapped['UserModel'] = relationship('UserModel')
    expenses: Mapped[list['ExpenseModel']] = relationship('ExpenseModel', back_populates='account', cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_on': account_type,
        'polymorphic_identity': 'account'
    }
