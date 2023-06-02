from datetime import date

from pydantic import BaseModel

from app.core.enums.status_enum import StatusEnum


class PurchasePaymentBase(BaseModel):
    amount: float
    status: StatusEnum
    number: int
    paid_date: date

class PurchasePaymentRequest(PurchasePaymentBase):
    pass

class PurchasePaymentResponse(PurchasePaymentBase):
    id: int