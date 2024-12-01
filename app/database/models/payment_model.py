from sqlalchemy import Float, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.payment_status_enum import PaymentStatusEnum


class PaymentModel(BaseModel):
    __tablename__ = 'payments'

    status: Mapped[str] = mapped_column(String(20), default=PaymentStatusEnum.UNCONFIRMED.value, nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    no_installment: Mapped[int] = mapped_column(Integer(), nullable=False)
    month: Mapped[int] = mapped_column(Integer(), nullable=False)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)

    # FK
    expense_id: Mapped[int] = mapped_column(Integer, ForeignKey('expenses.id'))

    def to_dict(self, include_relationships=False):
        payment_dict = {
            'id': self.id,
            'status': self.status,
            'amount': self.amount,
            'no_installment': self.no_installment,
            'month': self.month,
            'year': self.year,
            'expense_id': self.expense_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return payment_dict

    def __repr__(self) -> str:
        return f'Payment N° {self.no_installment} for expense {self.expense_id}'

    def __str__(self) -> str:
        return f'Payment N° {self.no_installment} for expense {self.expense_id}'
