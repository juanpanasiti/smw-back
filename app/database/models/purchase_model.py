from datetime import date

from sqlalchemy import String, Date, Float, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.status_enum import StatusEnum


class PurchaseModel(BaseModel):
    __tablename__= 'purchases'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    total_installments: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    status: Mapped[str] = mapped_column(Enum(StatusEnum), default=StatusEnum.TO_CHECK, nullable=False)
    purchased_at: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    is_subscription: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))

    def __repr__(self) -> str:
        return f'Purchase: {self.name}'

    def __str__(self) -> str:
        return f'Purchase: {self.name}'
    
    def update_data(self, new_data):
        return super().update_data(new_data)
