from pydantic import BaseModel

from app.core.enums.payment_status_enum import PaymentStatusEnum


class NewPaymentReq(BaseModel):
    status: PaymentStatusEnum = PaymentStatusEnum.UNCONFIRMED
    month: int
    year: int
    amount: float


class UpdatePaymentReq(BaseModel):
    status: PaymentStatusEnum | None = None
    amount: float | None = None


class PaymentReq(BaseModel):
    expense_id: int | None = None
    status: PaymentStatusEnum | None = None
    no_installment: int | None = None
    month: int | None = None
    year: int | None = None
    amount: float | None = None


class PaymentRes(BaseModel):
    id: int
    expense_id: int
    status: PaymentStatusEnum
    no_installment: int
    month: int
    year: int
    amount: float

    class Config:
        from_attributes = True


class PaymentUpdateQueryParams(BaseModel):
    recalculate_amounts: bool = False
