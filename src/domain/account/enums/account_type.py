from enum import Enum


class AccountType(str, Enum):
    """Enum for different types of accounts."""

    CREDIT_CARD = 'credit_card'
    DEBIT = 'debit'
    BILL_GROUP = 'bill_group'
