from datetime import date
from typing import List

from sqlalchemy import Date, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


class CreditCardStatementModel(BaseModel):
    __tablename__ = 'credit_card_statements'

    date_from: Mapped[date] = mapped_column(Date(), nullable=False)
    date_to: Mapped[date] = mapped_column(Date(), nullable=False)  # Period (MM-YYYY)
    expiration_date: Mapped[date] = mapped_column(Date(), nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean(), default=False, server_default='False', nullable=False)

    # FKs
    credit_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_cards.id'))
    
    @property
    def period(self) -> str:
        if self.date_from.month == self.date_to.month and self.date_from.year == self.date_to.year:
            return f'{date.strftime(self.date_from, "%b/%Y")}'
        return f'{date.strftime(self.date_from, "%b/%Y")}-{date.strftime(self.date_to, "%b/%Y")}'
    # Relations
    items: Mapped[List['StatementItemModel']] = relationship()
    # TODO

    def __repr__(self) -> str:
        return f'CreditCardStatement {self.period}'

    def __str__(self) -> str:
        return f'CreditCardStatement {self.period}'
