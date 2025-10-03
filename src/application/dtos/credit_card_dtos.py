from uuid import UUID
from datetime import date

from pydantic import BaseModel

class CreateCreditCardDTO(BaseModel):
    owner_id: UUID
    alias: str
    limit: float
    financing_limit: float
    main_credit_card_id: UUID | None = None
    next_closing_date: date
    next_expiring_date: date


class UpdateCreditCardDTO(BaseModel):
    id: UUID | None = None
    owner_id: UUID | None = None
    alias: str | None = None
    limit: float | None = None
    is_enabled: bool | None = None
    main_credit_card_id: UUID | None = None
    next_closing_date: date | None = None
    next_expiring_date: date | None = None
    financing_limit: float | None = None


class CreditCardResponseDTO(BaseModel):
    id: UUID
    owner_id: UUID
    alias: str
    limit: float
    is_enabled: bool
    main_credit_card_id: UUID | None = None
    next_closing_date: date
    next_expiring_date: date
    financing_limit: float
    total_expenses_count: int
    total_purchases_count: int
    total_subscriptions_count: int
    used_limit: float
    available_limit: float
    used_financing_limit: float
    available_financing_limit: float
