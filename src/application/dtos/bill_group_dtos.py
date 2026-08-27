from uuid import UUID

from pydantic import BaseModel


class CreateBillGroupDTO(BaseModel):
    """DTO for creating a new BillGroup."""
    
    owner_id: UUID
    alias: str
    is_enabled: bool = True


class UpdateBillGroupDTO(BaseModel):
    """DTO for updating an existing BillGroup."""
    
    alias: str | None = None
    is_enabled: bool | None = None


class BillGroupResponseDTO(BaseModel):
    """DTO for BillGroup response."""
    
    id: UUID
    owner_id: UUID
    alias: str
    is_enabled: bool
    total_expenses_count: int
    total_bills_count: int
    pending_bills_count: int
    used_limit: float  # Total pending amount
    estimated_monthly_cost: float
    total_paid_this_year: float


class BillGroupSummaryDTO(BaseModel):
    """DTO for BillGroup summary with grouped data."""
    
    id: UUID
    alias: str
    is_enabled: bool
    total_bills: int
    pending_bills: int
    estimated_monthly_cost: float
    total_paid_this_year: float
    bills_by_frequency: dict[str, int]  # frequency -> count
