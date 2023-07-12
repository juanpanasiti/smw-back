from datetime import datetime
from pydantic import BaseModel


class NewCreditCardReq(BaseModel):
    name: str
    limit: float
    main_credit_card_id: int | None

class CreditCardReq(BaseModel):
    name: str | None = None
    limit: float | None = None
    main_credit_card_id: int | None = None
    user_id: int


class CreditCardRes(BaseModel):
    id: int
    name: str
    limit: float
    main_credit_card_id: int | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
