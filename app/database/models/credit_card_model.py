from datetime import date
from typing import List

from sqlalchemy import String, Float, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .expense_model import ExpenseModel


class CreditCardModel(BaseModel):
    __tablename__ = 'credit_cards'

    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[int] = mapped_column(
        Float(precision=2), default=0.0, nullable=False)
    main_credit_card_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('credit_cards.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    next_closing_date: Mapped[date] = mapped_column(Date(), nullable=True)
    next_expiring_date: Mapped[date] = mapped_column(Date(), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    # Relations
    # expenses: Mapped[List['ExpenseModel']] = relationship()

    # Calculated fields
    # @property
    # def total_spent(self) -> float:
    #     return sum([expense.remaining_amount for expense in self.expenses])

    def __repr__(self) -> str:
        return f'CreditCard {self.name}'

    def __str__(self) -> str:
        return f'CreditCard {self.name}'
