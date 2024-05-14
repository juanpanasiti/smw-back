from sqlalchemy import Float, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.payment_status_enum import PaymentStatusEnum


class PaymentModel(BaseModel):
    __tablename__ = 'payments'

    status: Mapped[str] = mapped_column(
        Enum(PaymentStatusEnum), default=PaymentStatusEnum.UNCONFIRMED, nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    number: Mapped[int] = mapped_column(Integer(), nullable=False)
    month: Mapped[int] = mapped_column(Integer(), nullable=False)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)

    # FK
    expense_id: Mapped[int] = mapped_column(Integer, ForeignKey('expenses.id'))

    def __repr__(self) -> str:
        return f'Payment N° {self.number} for expense {self.expense_id}'

    def __str__(self) -> str:
        return f'Payment N° {self.number} for expense {self.expense_id}'