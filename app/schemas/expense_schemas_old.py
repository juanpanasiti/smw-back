from datetime import date
from pydantic import BaseModel
from typing import List

from .payment_schemas_old import PaymentRes
from app.core.enums.expense_type_enum import ExpenseTypeEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum
from app.core.enums.sortable_fields_enums import SortableExpenseFieldsEnum


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
    title: str
    cc_name: str
    amount: float
    acquired_at: date
    account_id: int


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
    account_id: int
    remaining_amount: float
    total_paid: float
    installments_paid: int
    installments_pending: int
    payments: List[PaymentRes] = []

    class Config:
        from_attributes = True

#! QUERY SCHEMAS


class ExpenseListParams(BaseModel):
    # filter
    type: ExpenseTypeEnum | None = None
    status: ExpenseStatusEnum | None = None
    # sort
    order_by: SortableExpenseFieldsEnum | None = SortableExpenseFieldsEnum.ID
    order_asc: bool = True
