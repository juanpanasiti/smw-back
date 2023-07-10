from sqlalchemy import Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class StatementItemModel(BaseModel):
    __tablename__ = 'statement_items'

    amount: Mapped[float] = mapped_column(Float(precision=2), default=0, nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    # PKs
    cc_statement_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_card_statements.id'))
    cc_expense_id: Mapped[int] = mapped_column(Integer, ForeignKey('credit_card_expenses.id'))

    # Relations
    # TODO
