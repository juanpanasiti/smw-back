from functools import reduce
from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..auth import User
from .account import Account
from ..shared import Amount


if TYPE_CHECKING:
    from ..expense import Payment, Expense



class CreditCard(Account):
    def __init__(
        self,
        id: UUID,
        owner: User,
        alias: str,
        limit: Amount,
        is_enabled: bool,
        main_credit_card_id: UUID,
        next_closing_date: date,
        next_expiring_date: date,
        financing_limit: Amount,
        expenses: list['Expense'],
    ):
        super().__init__(id, owner, alias, limit, is_enabled)
        self.main_credit_card_id = main_credit_card_id
        self.next_closing_date = next_closing_date
        self.next_expiring_date = next_expiring_date
        self.financing_limit = financing_limit
        self.expenses = expenses

    def to_dict(self, include_relationships: bool = False) -> dict:
        '''Convert the CreditCard instance to a dictionary representation.'''
        if include_relationships:
            from ..expense import PurchaseFactory
            expenses = [PurchaseFactory.create(**e.to_dict(include_relationships)) for e in self.expenses]
        else:
            expenses = [str(e.id) for e in self.expenses]
        return {
            'id': str(self.id),
            'owner': str(self.owner.id) if not include_relationships else self.owner.to_dict(),
            'alias': self.alias,
            'limit': self.limit.value,
            'is_enabled': self.is_enabled,
            'main_credit_card_id': str(self.main_credit_card_id),
            'next_closing_date': self.next_closing_date.isoformat(),
            'next_expiring_date': self.next_expiring_date.isoformat(),
            'financing_limit': self.financing_limit.value,
            'expenses': expenses,
        }

    def get_payments(self, month: int | None = None, year: int | None = None) -> list['Payment']:
        'Get all payments for this credit card in a given month and year.'
        if (month is None and year is not None) or (month is not None and year is None):
            raise ValueError('Both month and year must be provided together or both must be None')
        if month is not None and (month < 1 or month > 12):
            raise ValueError('month must be between 1 and 12')
        if year is not None and year < 2000:
            raise ValueError('year must be a positive integer greater than 2000')
        # FIXME: replace with Month and Year value objects

        return reduce(lambda acc, exp: acc + exp.get_payments(month, year), self.expenses, [])
