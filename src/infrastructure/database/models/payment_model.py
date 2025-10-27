from datetime import date
import uuid

from sqlalchemy import Float, Integer, String, Date, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from src.domain.expense.enums import PaymentStatus


class PaymentModel(BaseModel):
    __tablename__ = 'payments'

    status: Mapped[str] = mapped_column(String(20), default=PaymentStatus.UNCONFIRMED.value, nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    no_installment: Mapped[int] = mapped_column(Integer(), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date(), nullable=True)
    is_last_payment: Mapped[bool] = mapped_column(default=False, nullable=False)

    # FK
    expense_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('expenses.id'))

    def __repr__(self) -> str:
        return f'Payment N° {self.no_installment} for expense {self.expense_id}'

    def __str__(self) -> str:
        return f'Payment N° {self.no_installment} for expense {self.expense_id}'
