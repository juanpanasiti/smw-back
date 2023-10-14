from datetime import date
from typing import List

from sqlalchemy import String, Float, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .expense_model import ExpenseModel




class CreditCardModel(BaseModel):
    __tablename__ = 'credit_cards'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    limit: Mapped[int] = mapped_column(Float(precision=2), default=0.0, nullable=False)

    main_credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    closing_date: Mapped[date] = mapped_column(Date(), nullable=True)
    expiring_date: Mapped[date] = mapped_column(Date(), nullable=True)

    # Relations
    expenses: Mapped[List['ExpenseModel']] = relationship()

    # Calculated fields
    @property
    def total_spent(self) -> float:
        return sum([expense.get_remaining_amount() for expense in self.expenses])


    def __repr__(self) -> str:
        return f'CreditCard {self.name}'

    def __str__(self) -> str:
        return f'CreditCard {self.name}'
