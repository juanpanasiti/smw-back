from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic_tooltypes import Partial

from app.core.enums.sortable_fields_enums import SortableCreditCardFieldsEnum
from .examples import credit_card_schema_examples as credit_card_examples


class CreditCardAmounts(BaseModel):
    single_payment_total: float = Field(..., ge=0, description='Total amount of one-time purchases (not in installments)')
    installment_total: float = Field(..., ge=0, description='Total amount of purchases made in installments')
    monthly_subscriptions_total: float = Field(..., ge=0, description='Estimated total monthly cost of active subscriptions')

    model_config = {
        'json_schema_extra': {
            'example': credit_card_examples.CREDIT_CARD_AMOUNT_1
        }
    }


class CreditCardItems(BaseModel):
    single_payment_purchases: int = Field(..., ge=0, description='Number of one-time (non-installment) purchases')
    installment_purchases: int = Field(..., ge=0, description='Total number of purchases made in installments')
    new_installment_purchases: int = Field(..., ge=0, description='Number of new installment purchases with no payments yet made')
    last_installment_purchases: int = Field(..., ge=0, description='Number of installment purchases with only one payment left')
    subscriptions: int = Field(..., ge=0, description='Number of active monthly subscriptions')

    model_config = {
        'json_schema_extra': {
            'example': credit_card_examples.CREDIT_CARD_ITEM_1
        }
    }


class NewCreditCardReq(BaseModel):
    alias: str
    limit: int = 0
    financing_limit: int = 0
    main_credit_card_id: int | None = None
    user_id: int | None = None
    next_closing_date: date | None = None
    next_expiring_date: date | None = None


UpdateCreditCardReq = Partial[NewCreditCardReq]


class ExtensionCreditCardRes(BaseModel):
    id: int
    alias: str
    amounts: CreditCardAmounts = Field(..., description='Amounts related only to this card')
    items: CreditCardItems = Field(..., description='Item counts related only to this card')
    created_at: datetime
    updated_at: datetime
    is_enabled: bool = Field(True, description='Whether the card is currently enabled')

    model_config = {
        'json_schema_extra': {
            'example': credit_card_examples.EXTENSION_CREDIT_CARD_1
        }
    }


class CreditCardRes(BaseModel):
    id: int
    alias: str
    limit: int = Field(..., description='Limit for one-payment purchases', gt=0)
    financing_limit: int = Field(..., description='Limit for installment purchases (2 or more payments)', gt=0)
    user_id: int
    next_closing_date: Optional[date] = Field(None, description='Next billing cycle closing date')
    next_expiring_date: Optional[date] = Field(None, description='Next invoice due date')
    main_credit_card_id: Optional[int] = Field(None, description='Parent card ID if this is an extension')
    amounts: CreditCardAmounts = Field(..., description='Amounts related only to this card')
    items: CreditCardItems = Field(..., description='Item counts related only to this card')
    extensions: List[ExtensionCreditCardRes]
    created_at: datetime
    updated_at: datetime
    is_enabled: bool = Field(True, description='Whether the card is currently enabled')

    model_config = {
        'json_schema_extra': {
            'example': credit_card_examples.MAIN_CREDIT_CARD_1
        }
    }


class CreditCardListParam(BaseModel):
    # Pagination params
    limit: int = Field(default=10, ge=5, le=100, description='Limit must be between 5 and 100')
    offset: int = Field(default=0, ge=0, description='Offset must be at least 0')
    # Ordering
    order_by: SortableCreditCardFieldsEnum = SortableCreditCardFieldsEnum.ID
    order_asc: bool = True
