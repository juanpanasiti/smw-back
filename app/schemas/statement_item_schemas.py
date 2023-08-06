from datetime import datetime
from pydantic import BaseModel


class NewStatementItemReq(BaseModel):
    amount: float
    installment_no: int
    cc_expense_id: int

class StatementItemReq(BaseModel):
    installment_no: int | None = None
    cc_statement_id: int | None = None
    amount: float | None = None
    cc_expense_id: int | None = None


class StatementItemRes(BaseModel):
    id: int
    amount: float
    is_confirmed: bool
    installment_no: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
