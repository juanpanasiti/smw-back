from datetime import datetime,date
from pydantic import BaseModel

from app.core.enums.sortable_fields_enums import SortableCreditCardFieldsEnum


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
    main_credit_card_id: int | None = None
    # total_spent: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

#! QUERY SCHEMAS

class CreditCardListParams(BaseModel):
    # filter
    # TODO: implement filter by all/main
    # sort
    order_by: SortableCreditCardFieldsEnum | None = SortableCreditCardFieldsEnum.ID
    order_asc: bool = True