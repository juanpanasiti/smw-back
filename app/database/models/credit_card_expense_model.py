from datetime import date

from sqlalchemy import String, Date, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class CreditCardExpenseModel(BaseModel):
    __tablename__ = 'credit_card_expenses'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    is_subscription: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    total_installments: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    purchased_at: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)

    # PKs
    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))

    # Relations
    # TODO

    def __repr__(self) -> str:
        return f'Expense: {self.title}'

    def __str__(self) -> str:
        return f'Expense: {self.title}'
