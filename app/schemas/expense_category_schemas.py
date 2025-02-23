from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class NewExpenseCategoryReq(BaseModel):
    name: str
    description: str
    is_income: bool = False
    user_id: int


class UpdateExpenseCategoryReq(BaseModel):
    name: str | None = None
    description: str | None = None

class ExpenseCategoryRes(BaseModel):
    id: int
    name: str
    description: str
    is_income: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
