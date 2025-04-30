from pydantic import BaseModel

from app.core.enums.payment_status_enum import PaymentStatusEnum


class NewPaymentReqV1(BaseModel):
    status: PaymentStatusEnum = PaymentStatusEnum.UNCONFIRMED
    month: int
    year: int
    amount: float


class UpdatePaymentReqV1(BaseModel):
    status: PaymentStatusEnum | None = None
    amount: float | None = None


class PaymentReqV1(BaseModel):
    expense_id: int | None = None
    status: PaymentStatusEnum | None = None
    no_installment: int | None = None
    month: int | None = None
    year: int | None = None
    amount: float | None = None


class PaymentResV1(BaseModel):
    id: int
    expense_id: int
    status: PaymentStatusEnum
    no_installment: int
    month: int
    year: int
    amount: float

    class Config:
        from_attributes = True


class PaymentUpdateQueryParamsV1(BaseModel):
    recalculate_amounts: bool = False
