from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from .statement_item_schemas import StatementItemRes


class NewCCStatementReq(BaseModel):
    date_from: date
    date_to: date
    expiration_date: date


class CCStatementReq(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    expiration_date: date | None = None
    credit_card_id: int | None = None

class CCStatementRes(BaseModel):
    id: int
    credit_card_id: int
    date_from: date
    date_to: date
    expiration_date: date
    
    period: str
    # credit_card = None
    items: List[StatementItemRes] = []
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

