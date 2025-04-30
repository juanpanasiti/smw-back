from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.enums import ExpenseTypeEnum, ExpenseStatusEnum, SortableExpenseFieldsEnum, ExpenseSpentTypeEnum
from .payment_schemas_v2 import PaymentResV2


class NewExpenseReqV2(BaseModel):
    title: str
    cc_name: str
    acquired_at: date
    amount: float
    type: ExpenseTypeEnum
    installments: int
    first_payment_date: date
    account_id: int
    spent_type: Optional[ExpenseSpentTypeEnum] = None
    category_id: Optional[int] = None


class UpdateExpenseReqV2(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    acquired_at: date | None = None
    amount: float | None = None
    spent_type: Optional[ExpenseSpentTypeEnum] = None
    category_id: Optional[int] = None


class ExpenseResV2(BaseModel):
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
    spent_type: Optional[ExpenseSpentTypeEnum] = None
    category: Optional[str] = None
    category_id: Optional[int] = None
    payments: List[PaymentResV2] = []


class ExpenseListParamV2(BaseModel):
    # Pagination params
    limit: int | None = Field(default=None, ge=1, description='Limit must be between 5 and 100')
    offset: int = Field(default=0, ge=0, description='Offset must be at least 0')
    # Ordering
    order_by: SortableExpenseFieldsEnum = SortableExpenseFieldsEnum.ID
    order_asc: bool = True
