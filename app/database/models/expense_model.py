from datetime import date
from typing import List

from sqlalchemy import String, Date, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select

from . import BaseModel
from .payment_model import PaymentModel
from .account_model import AccountModel
from .expense_category_model import ExpenseCategoryModel
from app.core.enums.payment_status_enum import PaymentStatusEnum
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


class ExpenseModel(BaseModel):
    __tablename__ = 'expenses'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    acquired_at: Mapped[date] = mapped_column(Date(), default=date.today(), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(precision=20, scale=2), default=0.0, nullable=False)
    type: Mapped[str] = mapped_column(String(20), default=ExpenseTypeEnum.PURCHASE.value, nullable=False)
    installments: Mapped[int] = mapped_column(Integer(), default=1, nullable=False)
    first_payment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=ExpenseStatusEnum.ACTIVE.value, nullable=False)
    spent_type: Mapped[str] = mapped_column(String(20), nullable=True)

    # FKs
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('expense_categories.id'), nullable=True)

    # Relationships
    payments: Mapped[List['PaymentModel']] = relationship(
        'PaymentModel', backref='expense', order_by=PaymentModel.no_installment, lazy='select')
    account: Mapped['AccountModel'] = relationship('AccountModel')
    category: Mapped['ExpenseCategoryModel'] = relationship('ExpenseCategoryModel')

    # Computed fields
    @hybrid_property
    def user_id(self):
        return self.account.user_id

    @user_id.expression
    def user_id(cls):
        return select(AccountModel.user_id).where(AccountModel.id == cls.account_id).scalar_subquery()

    @property
    def remaining_amount(self) -> float:
        if self.type == ExpenseTypeEnum.SUBSCRIPTION:
            return float(self.amount) if self.status == ExpenseStatusEnum.ACTIVE else 0.0
        return sum([float(payment.amount) for payment in self.payments if payment.status not in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])

    @property
    def total_paid(self) -> float:
        if self.type == ExpenseTypeEnum.SUBSCRIPTION:
            return float(self.amount) if self.status == ExpenseStatusEnum.ACTIVE else 0.0
        return sum([float(payment.amount) for payment in self.payments if payment.status in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])

    @property
    def installments_paid(self) -> int:
        return len([payment for payment in self.payments if payment.status in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])

    @property
    def installments_pending(self) -> int:
        return len([payment for payment in self.payments if payment.status not in [PaymentStatusEnum.PAID, PaymentStatusEnum.CANCELED]])

    # Methods

    def to_dict(self, include_relationships=False):
        expense_dict = {
            'id': self.id,
            'title': self.title,
            'cc_name': self.cc_name,
            'acquired_at': self.acquired_at,
            'amount': self.amount,
            'installments': self.installments,
            'type': self.type,
            'first_payment_date': self.first_payment_date,
            'status': self.status,
            'account_id': self.account_id,
            'remaining_amount': self.remaining_amount,
            'total_paid': self.total_paid,
            'installments_paid': self.installments_paid,
            'installments_pending': self.installments_pending,
            'spent_type': self.spent_type,
            'category': self.category.name if self.category else None,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        if include_relationships:
            expense_dict['payments'] = [payment.to_dict() for payment in self.payments]
        return expense_dict

    def __repr__(self) -> str:
        return f'Expense: {self.title}'

    def __str__(self) -> str:
        return f'Expense: {self.title}'
