from pydantic import BaseModel

from app.core.enums.status_enum import StatusEnum


class NewPaymentReq(BaseModel):
    expense_id: int
    status: StatusEnum = StatusEnum.UNCONFIRMED
    number: int
    month: int
    year: int
    amount: float

class PaymentReq(BaseModel):
    status: StatusEnum | None = None
    number: int | None = None
    month: int | None = None
    year: int | None = None
    amount: float | None = None


class PaymentRes(BaseModel):
    id: int
    expense_id: int
    status: StatusEnum
    number: int
    month: int
    year: int
    amount: float

    class Config:
        from_attributes = True
