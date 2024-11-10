from typing import List

from sqlalchemy import String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .expense_model import ExpenseModel


class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    # PKs
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Relations
    expenses: Mapped[List['ExpenseModel']] = relationship('ExpenseModel', order_by='ExpenseModel.first_payment_date')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'account'
    }
