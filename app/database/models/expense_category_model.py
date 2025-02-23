from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import select

from . import BaseModel


class ExpenseCategoryModel(BaseModel):
    __tablename__ = 'expense_categories'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), default='')
    is_income: Mapped[bool] = mapped_column(default=False)

    # FKs
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
