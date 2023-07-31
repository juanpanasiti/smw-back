from datetime import datetime
from pydantic import BaseModel


class NewCreditCardReq(BaseModel):
    name: str
    limit: int
    main_credit_card_id: int | None = None

class CreditCardReq(BaseModel):
    name: str | None = None
    limit: int | None = None
    main_credit_card_id: int | None = None
    user_id: int | None = None


class CreditCardRes(BaseModel):
    id: int
    name: str
    limit: int
    main_credit_card_id: int | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
