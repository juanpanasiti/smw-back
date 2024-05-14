from pydantic import BaseModel

from app.core.enums.payment_status_enum import PaymentStatusEnum


class NewPaymentReq(BaseModel):
    expense_id: int
    status: PaymentStatusEnum = PaymentStatusEnum.UNCONFIRMED
    number: int
    month: int
    year: int
    amount: float

class PaymentReq(BaseModel):
    expense_id: int | None = None
    status: PaymentStatusEnum | None = None
    number: int | None = None
    month: int | None = None
    year: int | None = None
    amount: float | None = None


class PaymentRes(BaseModel):
    id: int
    expense_id: int
    status: PaymentStatusEnum
    number: int
    month: int
    year: int
    amount: float

    class Config:
        from_attributes = True
