from datetime import date

from sqlalchemy import String, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


class StatementItemModel(BaseModel):
    __tablename__ = 'statement_items'
    
    carged_date: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), default=0, nullable=False)

    credit_card_statement_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_card_statements.id'))
    purchase_payment_id: Mapped[int] = mapped_column(Integer, ForeignKey('purchase_payments.id'))

    def update_data(self, new_data):
        return super().update_data(new_data)