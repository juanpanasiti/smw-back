from datetime import date
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import String, Date, Integer, ForeignKey, Numeric, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select

from . import BaseModel
from .payment_model import PaymentModel
from src.domain.expense.enums import ExpenseType, ExpenseStatus

if TYPE_CHECKING:
    from . import AccountModel, ExpenseCategoryModel


class ExpenseModel(BaseModel):
    __tablename__ = 'expenses'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    acquired_at: Mapped[date] = mapped_column(Date(), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(precision=20, scale=2), default=0.0, nullable=False)
    expense_type: Mapped[str] = mapped_column(String(20), default=ExpenseType.PURCHASE.value, nullable=False)
    installments: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    first_payment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=ExpenseStatus.ACTIVE.value, nullable=False)
    spent_type: Mapped[str] = mapped_column(String(20), nullable=True)

    # FKs
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('accounts.id'))
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('expense_categories.id'), nullable=True)

    # Relationships
    payments: Mapped[list['PaymentModel']] = relationship(
        'PaymentModel', backref='expense', order_by=lambda: PaymentModel.no_installment, lazy='select', cascade='all, delete-orphan')
    account: Mapped['AccountModel'] = relationship('AccountModel', back_populates='expenses')
    category: Mapped['ExpenseCategoryModel'] = relationship('ExpenseCategoryModel')

    # Computed fields
    @hybrid_property
    def owner_id(self):  # type: ignore[reportRedeclaration]
        return self.account.owner_id

    @owner_id.expression
    def owner_id(cls):
        return select(AccountModel.owner_id).where(AccountModel.id == cls.account_id).scalar_subquery()

    def __repr__(self) -> str:
        return f'Expense: {self.title}'

    def __str__(self) -> str:
        return f'Expense: {self.title}'
