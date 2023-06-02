from typing import List
from datetime import date

from pydantic import BaseModel

from app.core.enums.status_enum import StatusEnum


class CreditCardStatementBase(BaseModel):
    date_from: date
    date_to: date
    total: float
    period: str
    status: StatusEnum

class CreditCardStatementRequest(CreditCardStatementBase):
    status:StatusEnum = StatusEnum.TO_CHECK

class CreditCardStatementResponse(CreditCardStatementBase):
    id: int