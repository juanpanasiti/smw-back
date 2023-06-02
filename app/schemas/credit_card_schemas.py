from datetime import date
from typing import List

from pydantic import BaseModel


class CreditCardBase(BaseModel):
    name: str
    closing_date: date
    expiring_date: date
    limit: float

class CreditCardRequest(CreditCardBase):
    user_id: int

class CreditCardResponse(CreditCardBase):
    id: int
    extensions: List[CreditCardBase]
    main_cc: CreditCardBase

