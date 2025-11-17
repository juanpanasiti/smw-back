from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from datetime import date

from src.domain.expense.enums import PaymentStatus, ExpenseStatus
from src.domain.account.enums import AccountType


class PeriodPaymentDTO(BaseModel):
    """Payment with enriched data for period view."""
    
    model_config = ConfigDict(from_attributes=True)
    
    # Payment data
    payment_id: UUID = Field(..., description="Payment ID")
    amount: float = Field(..., description="Payment amount")
    status: PaymentStatus = Field(..., description="Payment status")
    payment_date: date = Field(..., description="Payment due date")
    no_installment: int = Field(..., description="Installment number")
    is_last_payment: bool = Field(..., description="Whether this is the last installment")
    
    # Expense data (for filtering and display)
    expense_id: UUID = Field(..., description="Expense ID")
    expense_title: str = Field(..., description="Expense title/description")
    expense_cc_name: str = Field(..., description="Name used on credit card")
    expense_acquired_at: date = Field(..., description="Date when expense was acquired")
    expense_installments: int = Field(..., description="Total number of installments")
    expense_status: ExpenseStatus = Field(..., description="Expense status")
    expense_category_name: str | None = Field(None, description="Category name if exists")
    
    # Account data (for filtering)
    account_id: UUID = Field(..., description="Account ID")
    account_alias: str = Field(..., description="Account alias/name")
    account_is_enabled: bool = Field(..., description="Whether account is enabled")
    account_type: AccountType = Field(..., description="Type of account")


class PeriodResponseDTO(BaseModel):
    """Period with all calculated data and enriched payments."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Period ID")
    period_str: str = Field(..., description="Period in MM/YYYY format")
    month: int = Field(..., ge=1, le=12, description="Month number")
    year: int = Field(..., description="Year")
    
    # Calculated amounts
    total_amount: float = Field(..., description="Total amount of all payments")
    total_confirmed_amount: float = Field(..., description="Total of confirmed + paid payments")
    total_paid_amount: float = Field(..., description="Total of paid payments only")
    total_pending_amount: float = Field(..., description="Total of unconfirmed payments")
    
    # Counters
    total_payments: int = Field(..., description="Total number of payments")
    pending_payments_count: int = Field(..., description="Number of pending payments")
    completed_payments_count: int = Field(..., description="Number of completed payments")
    
    # Enriched payments
    payments: list[PeriodPaymentDTO] = Field(default_factory=list, description="List of enriched payments")


class PeriodSummaryDTO(BaseModel):
    """Lightweight period summary (for lists and charts)."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Period ID")
    period_str: str = Field(..., description="Period in MM/YYYY format")
    month: int = Field(..., ge=1, le=12, description="Month number")
    year: int = Field(..., description="Year")
    
    # Calculated amounts
    total_amount: float = Field(..., description="Total amount of all payments")
    total_confirmed_amount: float = Field(..., description="Total of confirmed + paid payments")
    total_paid_amount: float = Field(..., description="Total of paid payments only")
    
    # Counter
    total_payments: int = Field(..., description="Total number of payments")

