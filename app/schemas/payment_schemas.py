from datetime import datetime
from pydantic import BaseModel, Field

from app.core.enums.payment_status_enum import PaymentStatusEnum
from app.core.enums.sortable_fields_enums import SortablePaymentFieldsEnum


class NewPaymentReq(BaseModel):
    amount: float
    no_installment: int = Field(ge=1)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000)
    expense_id: int


class UpdatePaymentReq(BaseModel):
    amount: float | None = None
    no_installment: int | None = None
    month: int | None = None
    year: int | None = None
    status: PaymentStatusEnum | None = None


class PaymentRes(BaseModel):
    id: int
    status: PaymentStatusEnum
    amount: float
    no_installment: int
    month: int
    year: int
    expense_id: int
    created_at: datetime
    updated_at: datetime


class PaymentListParam(BaseModel):
    # Pagination params
    limit: int | None = Field(default=None, ge=1, description='Limit must be between 5 and 100')
    offset: int = Field(default=0, ge=0, description='Offset must be at least 0')
    # Ordering
    order_by: SortablePaymentFieldsEnum = SortablePaymentFieldsEnum.ID
    order_asc: bool = True
