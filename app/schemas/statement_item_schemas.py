from datetime import date

from pydantic import BaseModel


class StatementItemBase(BaseModel):
    carged_date: date
    amount: float


class StatementItemRequest(StatementItemBase):
    pass


class StatementItemResponse(StatementItemBase):
    id: int
