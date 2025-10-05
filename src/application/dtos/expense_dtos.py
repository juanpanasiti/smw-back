from uuid import UUID
from datetime import date

from pydantic import BaseModel, Field

from src.domain.expense.enums import ExpenseStatus, ExpenseType
from .payment_dtos import PaymentResponseDTO as Payment


class ExpenseResponseDTO(BaseModel):
    id: UUID
    account_id: UUID
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    expense_type: ExpenseType
    installments: int
    first_payment_date: date
    status: ExpenseStatus
    category_id: UUID
    payments: list[Payment] = Field(default_factory=list)
    is_one_time_payment: bool
    paid_amount: float
    pending_installments: int
    done_installments: int
    pending_financing_amount: float
    pending_amount: float


class CreatePurchaseDTO(BaseModel):
    account_id: UUID
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    installments: int
    first_payment_date: date
    category_id: UUID


class UpdatePurchaseDTO(BaseModel):
    account_id: UUID | None = None
    title: str | None = None
    cc_name: str | None = None
    acquired_at: date | None = None
    amount: float | None = None
    first_payment_date: date | None = None
    status: ExpenseStatus | None = None
    category_id: UUID | None = None


class CreateSubscriptionDTO(BaseModel):
    account_id: UUID
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    installments: int
    first_payment_date: date
    status: ExpenseStatus
    category_id: UUID


class UpdateSubscriptionDTO(BaseModel):
    account_id: UUID | None = None
    title: str | None = None
    cc_name: str | None = None
    acquired_at: date | None = None
    amount: float | None = None
    expense_type: ExpenseType | None = None
    first_payment_date: date | None = None
    status: ExpenseStatus | None = None
    category_id: UUID | None = None
