from datetime import datetime,date
from pydantic import BaseModel


class NewCreditCardReq(BaseModel):
    name: str
    limit: int

class CreditCardReq(BaseModel):
    name: str | None = None
    limit: int | None = None
    user_id: int | None = None
    closing_date: date | None
    expiring_date: date | None


class CreditCardRes(BaseModel):
    id: int
    name: str
    limit: int
    user_id: int
    closing_date: date | None
    expiring_date: date | None
    total_spent: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
