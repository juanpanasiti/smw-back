from pydantic import BaseModel

from app.core.enums.expense_type_enum import ExpenseTypeEnum


class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10


class ExpenseListParams(BaseModel):
    type: ExpenseTypeEnum | None = None
