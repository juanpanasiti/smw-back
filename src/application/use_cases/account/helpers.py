"""Helper functions for account use cases."""
from src.domain.account import CreditCard
from src.application.dtos import CreditCardResponseDTO


def parse_credit_card(credit_card: CreditCard) -> CreditCardResponseDTO:
    """
    Convert a CreditCard domain entity to CreditCardResponseDTO.
    
    Args:
        credit_card: CreditCard domain entity
        
    Returns:
        CreditCardResponseDTO with all computed values
    """
    return CreditCardResponseDTO(
        id=credit_card.id,
        owner_id=credit_card.owner_id,
        alias=credit_card.alias,
        limit=credit_card.limit.value,
        is_enabled=credit_card.is_enabled,
        main_credit_card_id=credit_card.main_credit_card_id,
        next_closing_date=credit_card.next_closing_date,
        next_expiring_date=credit_card.next_expiring_date,
        financing_limit=credit_card.financing_limit.value,
        total_expenses_count=credit_card.total_expenses_count,
        total_purchases_count=credit_card.total_purchases_count,
        total_subscriptions_count=credit_card.total_subscriptions_count,
        used_limit=credit_card.used_limit.value,
        available_limit=credit_card.available_limit.value,
        used_financing_limit=credit_card.used_financing_limit.value,
        available_financing_limit=credit_card.available_financing_limit.value,
    )
