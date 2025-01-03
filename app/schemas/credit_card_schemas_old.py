from datetime import datetime, date
from pydantic import BaseModel
from typing import List

from .expense_schemas_old import ExpenseRes
from app.core.enums.sortable_fields_enums import SortableCreditCardFieldsEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


class CreditCardReq(BaseModel):
    alias: str
    limit: int
    main_credit_card_id: int | None = None
    user_id: int
    next_closing_date: date | None = None
    next_expiring_date: date | None = None
    is_enabled: bool = True


class CreditCardRes(BaseModel):
    id: int
    alias: str
    limit: int
    user_id: int
    next_closing_date: date | None
    next_expiring_date: date | None
    main_credit_card_id: int | None = None
    total_spent: float
    created_at: datetime
    updated_at: datetime
    is_enabled: bool = True
    expenses: List[ExpenseRes]


    class Config:
        from_attributes = True

#! QUERY SCHEMAS


class CreditCardListParams(BaseModel):
    # filter
    # TODO: implement filter by all/main
    expense_status: ExpenseStatusEnum | None = None
    # sort
    order_by: SortableCreditCardFieldsEnum | None = SortableCreditCardFieldsEnum.ID
    order_asc: bool = True
