from datetime import date

from sqlalchemy import String, Integer, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.status_enum import StatusEnum


class PurchasePaymentModel(BaseModel):
    __tablename__ = 'purchase_payments'

    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(Enum(StatusEnum), default=StatusEnum.TO_CHECK, nullable=False)
    number: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    paid_date: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)

    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey('purchases.id'))

    def update_data(self, new_data):
        return super().update_data(new_data)