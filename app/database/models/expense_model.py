from datetime import date
from typing import List

from sqlalchemy import String, Date, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .payment_model import PaymentModel
from app.core.enums.status_enum import StatusEnum


class ExpenseModel(BaseModel):
    __tablename__ = 'expenses'

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
    payments: Mapped[List['PaymentModel']] = relationship(order_by=PaymentModel.number)

    # Calculated fields
    @property
    def remaining_amount(self) -> float:
        if self.is_subscription:
            return self.total_amount if self.is_active else 0.0
        return sum([payment.amount for payment in self.payments if payment.status not in [StatusEnum.PAID, StatusEnum.CANCELED]])
    
    @property
    def total_paid(self) -> float:
        if self.is_subscription:
            return self.total_amount if self.is_active else 0.0
        return sum([payment.amount for payment in self.payments if payment.status in [StatusEnum.PAID, StatusEnum.CANCELED]])
    
    @property
    def installments_paid(self) -> int:
        return len([payment for payment in self.payments if payment.status in [StatusEnum.PAID, StatusEnum.CANCELED]])
    
    @property
    def installments_pending(self) -> int:
        return len([payment for payment in self.payments if payment.status not in [StatusEnum.PAID, StatusEnum.CANCELED]])
    
    @property
    def first_payment(self) -> str:
        return f'{self.payments[0].month}/{self.payments[0].year}' if self.payments else '---'

    def __repr__(self) -> str:
        return f'Expense: {self.title}'

    def __str__(self) -> str:
        return f'Expense: {self.title}'
