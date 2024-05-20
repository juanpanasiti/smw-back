from datetime import datetime,date
from pydantic import BaseModel


class CreditCardReq(BaseModel):
    alias: str
    limit: int
    main_credit_card_id: int | None = None
    user_id: int
    next_closing_date: date | None = None
    next_expiring_date: date | None = None
    is_enbled: bool = True


class CreditCardRes(BaseModel):
    id: int
    alias: str
    limit: int
    user_id: int
    next_closing_date: date | None
    next_expiring_date: date | None
    # total_spent: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
