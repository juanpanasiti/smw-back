from datetime import date

from pydantic import BaseModel

from app.core.enums.status_enum import StatusEnum


class PurchaseBase(BaseModel):
    name: str
    cc_name: str
    amount: float
    total_installments: int
    status: StatusEnum
    purchased_at: date
    is_subscription: bool

class PurchaseRequest(PurchaseBase):
    pass


class PurchaseResponse(PurchaseBase):
    id: int