from functools import reduce
from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..shared import Amount, Month, Year
from .account import Account
from .enums import AccountType


if TYPE_CHECKING:
    from ..expense import Payment, Expense


class CreditCard(Account):
    AMOUNT_FIELDS = ['limit', 'financing_limit']

    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        alias: str,
        limit: Amount,
        is_enabled: bool,
        main_credit_card_id: UUID | None,
        next_closing_date: date,
        next_expiring_date: date,
        financing_limit: Amount,
        expenses: list['Expense'],
    ):
        super().__init__(id, owner_id, alias, limit, is_enabled)
        self.main_credit_card_id = main_credit_card_id
        self.next_closing_date = next_closing_date
        self.next_expiring_date = next_expiring_date
        self.financing_limit = financing_limit
        self.expenses = expenses

    @property
    def account_type(self) -> AccountType:
        """Return CREDIT_CARD as the account type."""
        return AccountType.CREDIT_CARD

    @property
    def total_expenses_count(self) -> int:
        """Return the total number of expenses associated with this credit card."""
        return len(self.expenses)

    @property
    def total_purchases_count(self) -> int:
        """Return the total number of purchase expenses associated with this credit card."""
        from ..expense import ExpenseType
        return len([exp for exp in self.expenses if exp.expense_type == ExpenseType.PURCHASE])

    @property
    def total_subscriptions_count(self) -> int:
        from ..expense import ExpenseType
        """Return the total number of subscription expenses associated with this credit card."""
        return len([exp for exp in self.expenses if exp.expense_type == ExpenseType.SUBSCRIPTION])

    @property
    def used_limit(self) -> Amount:
        """Calculate and return the used limit of the credit card."""
        return sum((exp.pending_amount for exp in self.expenses), Amount(0))

    @property
    def available_limit(self) -> Amount:
        """Calculate and return the available limit of the credit card."""
        return self.limit - self.used_limit

    @property
    def used_financing_limit(self) -> Amount:
        """Calculate and return the used financing limit of the credit card."""
        return sum((exp.pending_financing_amount for exp in self.expenses), Amount(0))

    @property
    def available_financing_limit(self) -> Amount:
        """Calculate and return the available financing limit of the credit card."""
        return self.financing_limit - self.used_financing_limit

    def update_from_dict(self, data: dict) -> None:
        """Update the CreditCard instance with values from a dictionary."""
        for key, value in data.items():
            if key in self.AMOUNT_FIELDS and isinstance(value, (int, float)):
                value = Amount(value)
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self, include_relationships: bool = False) -> dict:
        '''Convert the CreditCard instance to a dictionary representation.'''
        base_dict = super().to_dict(include_relationships)
        
        if include_relationships:
            from ..expense import PurchaseFactory
            expenses = [PurchaseFactory.create(**e.to_dict(include_relationships)) for e in self.expenses]
        else:
            expenses = [str(e.id) for e in self.expenses]
        
        base_dict.update({
            'main_credit_card_id': str(self.main_credit_card_id) if self.main_credit_card_id else None,
            'next_closing_date': self.next_closing_date.isoformat(),
            'next_expiring_date': self.next_expiring_date.isoformat(),
            'financing_limit': self.financing_limit.value,
            'expenses': expenses,
        })
        
        return base_dict

    def get_payments(self, month: Month | None = None, year: Year | None = None) -> list['Payment']:
        'Get all payments for this credit card in a given month and year.'
        if (month is None and year is not None) or (month is not None and year is None):
            raise ValueError('Both month and year must be provided together or both must be None')

        return reduce(lambda acc, exp: acc + exp.get_payments(month, year), self.expenses, [])
