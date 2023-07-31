from datetime import datetime, date
from pydantic import BaseModel

# ! PURCHASES
class NewCCPurchaseReq(BaseModel):
    title: str
    cc_name: str
    total_amount: float
    total_installments: int
    purchased_at: date


class CCPurchaseReq(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    total_amount: float | None = None
    total_installments: int | None = None
    purchased_at: date | None = None
    credit_card_id: int | None = None

class CCPurchaseRes(BaseModel):
    id: int
    title: str
    cc_name: str
    total_amount: float
    total_installments: int
    purchased_at: date
    credit_card_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ! SUBSCRIPTIONS
class NewCCSubscriptionReq(BaseModel):
    title: str
    cc_name: str
    total_amount: float
    is_active: bool = True
    purchased_at: date


class CCSubscriptionReq(BaseModel):
    title: str | None = None
    cc_name: str | None = None
    total_amount: float | None = None
    is_active: bool | None = None
    purchased_at: date | None = None
    credit_card_id: int | None = None

class CCSubscriptionRes(BaseModel):
    id: int
    title: str
    cc_name: str
    total_amount: float
    purchased_at: date
    is_active: bool
    credit_card_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True