from datetime import date
from typing import List

from sqlalchemy import String, Date, Float, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel
from .payment_model import PaymentModel
from app.core.enums.payment_status_enum import PaymentStatusEnum
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


class ExpenseModel(BaseModel):
    __tablename__ = 'expenses'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    acquired_at: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    type: Mapped[str] = mapped_column(Enum(ExpenseTypeEnum), default=ExpenseTypeEnum.PURCHASE, nullable=False)
    installments: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    first_payment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    status: Mapped[str] = mapped_column(Enum(ExpenseStatusEnum), default=ExpenseStatusEnum.ACTIVE, nullable=False)

    # PKs
    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))

    # Relations
    payments: Mapped[List['PaymentModel']] = relationship(order_by=PaymentModel.no_installment)

    # Calculated fields
    @property
    def remaining_amount(self) -> float:
        if self.type == ExpenseTypeEnum.SUBSCRIPTION:
            return self.amount if self.status == ExpenseStatusEnum.ACTIVE else 0.0
        return sum([payment.amount for payment in self.payments if payment.status not in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])
    
    @property
    def total_paid(self) -> float:
        if self.type == ExpenseTypeEnum.SUBSCRIPTION:
            return self.amount if self.status == ExpenseStatusEnum.ACTIVE else 0.0
        return sum([payment.amount for payment in self.payments if payment.status in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])
    
    @property
    def installments_paid(self) -> int:
        return len([payment for payment in self.payments if payment.status in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])
    
    @property
    def installments_pending(self) -> int:
        return len([payment for payment in self.payments if payment.status not in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])

    def __repr__(self) -> str:
        return f'Expense: {self.title}'

    def __str__(self) -> str:
        return f'Expense: {self.title}'
