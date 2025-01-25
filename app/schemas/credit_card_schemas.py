from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import List

from .expense_schemas_old import ExpenseRes
from app.core.enums.sortable_fields_enums import SortableCreditCardFieldsEnum
from app.core.enums.expense_status_enum import ExpenseStatusEnum


class NewCreditCardReq(BaseModel):
    alias: str
    limit: int = 0
    financing_limit: int = 0
    main_credit_card_id: int | None = None
    user_id: int | None = None
    next_closing_date: date | None = None
    next_expiring_date: date | None = None


class UpdateCreditCardReq(BaseModel):
    alias: str | None = None
    limit: int | None = None
    financing_limit: int | None = None
    main_credit_card_id: int | None = None
    user_id: int | None = None
    next_closing_date: date | None = None
    next_expiring_date: date | None = None


class CreditCardRes(BaseModel):
    id: int
    alias: str
    limit: int
    financing_limit: int
    user_id: int
    next_closing_date: date | None
    next_expiring_date: date | None
    main_credit_card_id: int | None = None
    total_spent: float
    created_at: datetime
    updated_at: datetime
    is_enabled: bool = True


class CreditCardListParam(BaseModel):
    # Pagination params
    limit: int = Field(default=10, ge=5, le=100, description='Limit must be between 5 and 100')
    offset: int = Field(default=0, ge=0, description='Offset must be at least 0')
    # Ordering
    order_by: SortableCreditCardFieldsEnum = SortableCreditCardFieldsEnum.ID
    order_asc: bool = True
