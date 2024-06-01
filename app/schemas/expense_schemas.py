from datetime import datetime, date
from pydantic import BaseModel
from typing import List

from .payment_schemas import PaymentRes
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


class NewExpenseReq(BaseModel):
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    credit_card_id: int


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
