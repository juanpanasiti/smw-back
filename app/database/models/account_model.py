from typing import List

from sqlalchemy import String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from app.core.enums.expense_type_enum import ExpenseTypeEnum


class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[float] = mapped_column(Numeric(precision=20, scale=2), default=0.0, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    # FKs
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Relationships
    expenses: Mapped[List['ExpenseModel']] = relationship('ExpenseModel', order_by='ExpenseModel.first_payment_date')

    @property
    def purchases(self) -> List['ExpenseModel']:
        return [expense for expense in self.expenses if expense.type == ExpenseTypeEnum.PURCHASE]

    @property
    def subscriptions(self) -> List['ExpenseModel']:
        return [expense for expense in self.expenses if expense.type == ExpenseTypeEnum.SUBSCRIPTION]

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'account'
    }
