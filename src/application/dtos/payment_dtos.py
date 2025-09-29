from uuid import UUID
from datetime import date

from pydantic import BaseModel

from src.domain.expense.enums import PaymentStatus


class PaymentResponseDTO(BaseModel):
    id: UUID
    expense_id: UUID
    amount: float
    no_installment: int
    status: PaymentStatus
    payment_date: date
    is_last_payment: bool



class CreatePaymentDTO(BaseModel):
    expense_id: UUID
    amount: float
    payment_date: date



class UpdatePaymentDTO(BaseModel):
    amount: float
    status: PaymentStatus
    payment_date: date

