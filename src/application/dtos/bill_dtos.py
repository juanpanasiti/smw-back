from __future__ import annotations

from uuid import UUID
from datetime import date

from pydantic import BaseModel, Field, field_validator

from src.domain.expense.enums import BillFrequency
from .payment_dtos import PaymentResponseDTO, CreatePaymentDTO


class CreateBillDTO(BaseModel):
    """DTO for creating a new Bill."""
    
    account_id: UUID  # BillGroup ID
    description: str
    amount: float
    bill_date: date
    frequency: BillFrequency = BillFrequency.MONTHLY
    next_bill_month: int | None = None
    next_bill_year: int | None = None
    notes: str = ''
    payments: list[CreatePaymentDTO] = Field(default_factory=list)

    @field_validator('next_bill_month')
    @classmethod
    def validate_month(cls, v: int | None) -> int | None:
        if v is not None and not 1 <= v <= 12:
            raise ValueError('next_bill_month must be between 1 and 12')
        return v


class UpdateBillDTO(BaseModel):
    """DTO for updating an existing Bill."""
    
    description: str | None = None
    amount: float | None = None
    bill_date: date | None = None
    frequency: BillFrequency | None = None
    next_bill_month: int | None = None
    next_bill_year: int | None = None
    notes: str | None = None

    @field_validator('next_bill_month')
    @classmethod
    def validate_month(cls, v: int | None) -> int | None:
        if v is not None and not 1 <= v <= 12:
            raise ValueError('next_bill_month must be between 1 and 12')
        return v


class UpdateBillNextDateDTO(BaseModel):
    """DTO for updating only the next bill date."""
    
    next_bill_month: int
    next_bill_year: int

    @field_validator('next_bill_month')
    @classmethod
    def validate_month(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError('next_bill_month must be between 1 and 12')
        return v


class BillResponseDTO(BaseModel):
    """DTO for Bill response."""
    
    id: UUID
    account_id: UUID
    description: str
    amount: float
    bill_date: date
    frequency: BillFrequency
    next_bill_month: int | None
    next_bill_year: int | None
    next_bill_date_display: str | None
    notes: str
    total_amount: float
    paid_amount: float
    pending_amount: float
    is_fully_paid: bool
    payments: list[PaymentResponseDTO] = Field(default_factory=list)


class BillListResponseDTO(BaseModel):
    """DTO for list of Bills with pagination."""
    
    bills: list[BillResponseDTO]
    total: int
    page: int
    page_size: int


class UpcomingBillDTO(BaseModel):
    """DTO for upcoming bill notification."""
    
    id: UUID
    account_id: UUID
    account_alias: str  # BillGroup alias
    description: str
    amount: float
    frequency: BillFrequency
    next_bill_month: int
    next_bill_year: int
    next_bill_date_display: str
    notes: str
