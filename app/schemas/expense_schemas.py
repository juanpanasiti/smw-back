from datetime import datetime, date
from pydantic import BaseModel
from typing import List

from .payment_schemas import PaymentRes
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


# ! EXPENSES
class NewExpenseReq(BaseModel):
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    credit_card_id: int
    user_id: int | None = None


class UpdateExpenseReq(BaseModel):
    title: str
    cc_name: str
    acquired_at: date
    credit_card_id: int


class ExpenseRes(NewExpenseReq):
    id: int
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    status: ExpenseStatusEnum
    credit_card_id: int
    user_id: int | None = None

    class Config:
        from_attributes = True

# ! PURCHASES


class NewPurchaseReq(BaseModel):
    title: str
    cc_name: str
    total_amount: float
    total_installments: int
    purchased_at: date
    first_installment: date


class PurchaseReq(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    total_amount: float | None = None
    total_installments: int | None = None
    purchased_at: date | None = None
    credit_card_id: int | None = None


class PurchaseRes(BaseModel):
    id: int
    title: str
    cc_name: str
    total_amount: float
    total_installments: int
    purchased_at: date
    credit_card_id: int
    created_at: datetime
    updated_at: datetime
    remaining_amount: float
    total_paid: float
    installments_paid: int
    installments_pending: int
    first_payment: str
    payments: List[PaymentRes] = []

    class Config:
        from_attributes = True

# ! SUBSCRIPTIONS


class NewSubscriptionReq(BaseModel):
    title: str
    cc_name: str
    total_amount: float
    is_active: bool = True
    purchased_at: date


class SubscriptionReq(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    total_amount: float | None = None
    is_active: bool | None = None
    purchased_at: date | None = None
    credit_card_id: int | None = None


class SubscriptionRes(BaseModel):
    id: int
    title: str
    cc_name: str
    total_amount: float
    purchased_at: date
    is_active: bool
    credit_card_id: int
    created_at: datetime
    updated_at: datetime
    payments: List[PaymentRes] = []

    class Config:
        from_attributes = True

# ! EXPENSE LIST


class ExepenseListResponse(BaseModel):
    purchases: List[PurchaseRes] = []
    subscriptions: List[SubscriptionRes] = []

    class Config:
        from_attributes = True
