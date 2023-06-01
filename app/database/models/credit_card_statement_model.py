from datetime import date

from sqlalchemy import String, Date, Float, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from app.core.enums.status_enum import StatusEnum


class CreditCardStatementModel(BaseModel):
    __tablename__= 'credit_card_statements'

    date_from: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    date_to: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    total: Mapped[float] = mapped_column(Float(precision=2), default=0.0, nullable=False)
    period: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(Enum(StatusEnum), default=StatusEnum.TO_CHECK, nullable=False)

    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))

    def __repr__(self) -> str:
        return f'CreditCardStatement {self.period}'

    def __str__(self) -> str:
        return f'CreditCardStatement {self.period}'
