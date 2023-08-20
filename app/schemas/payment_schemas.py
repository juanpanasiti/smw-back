from pydantic import BaseModel

from app.core.enums.status_enum import StatusEnum


class PaymentReq(BaseModel):
    expense_id: int
    status: StatusEnum = StatusEnum.UNCONFIRMED
    number: int
    month: int
    year: int
    amount: float


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
