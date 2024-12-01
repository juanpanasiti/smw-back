from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List

from app.core.enums import ExpenseTypeEnum, ExpenseStatusEnum, SortableExpenseFieldsEnum
from .payment_schemas import PaymentRes


class NewExpenseReq(BaseModel):
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    account_id: int


class UpdateExpenseReq(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    acquired_at: date | None = None
    amount: float | None = None


class ExpenseRes(BaseModel):
    id: int
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    status: ExpenseStatusEnum
    account_id: int
    remaining_amount: float
    total_paid: float
    installments_paid: int
    installments_pending: int
    created_at: datetime
    updated_at: datetime
    payments: List[PaymentRes] = []


class ExpenseListParam(BaseModel):
    # Pagination params
    limit: int | None = Field(default=None, ge=1, description='Limit must be between 5 and 100')
    offset: int = Field(default=0, ge=0, description='Offset must be at least 0')
    # Ordering
    order_by: SortableExpenseFieldsEnum = SortableExpenseFieldsEnum.ID
    order_asc: bool = True
