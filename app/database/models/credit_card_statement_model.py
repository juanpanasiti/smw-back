from datetime import date

from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class CreditCardStatementModel(BaseModel):
    __tablename__ = 'credit_card_statements'

    date_from: Mapped[date] = mapped_column(Date(), nullable=False)
    date_to: Mapped[date] = mapped_column(Date(), nullable=False)  # Period (MM-YYYY)
    expiration_date: Mapped[date] = mapped_column(Date(), nullable=False)

    # PKs
    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))

    # Relations
    # TODO

    def __repr__(self) -> str:
        return f'CreditCardStatement {self.period}'

    def __str__(self) -> str:
        return f'CreditCardStatement {self.period}'
