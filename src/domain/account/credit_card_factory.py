from datetime import date
from operator import not_
from uuid import UUID

from ..shared import EntityFactoryBase, Amount


class CreditCardFactory(EntityFactoryBase):
    
    @staticmethod
    def create(**kwargs):
        from ..auth import User
        from .credit_card import CreditCard
        from ..expense import Expense

        id: UUID | None = kwargs.get('id')
        owner: User | None = kwargs.get('owner')
        alias: str | None = kwargs.get('alias')
        limit: Amount | None = kwargs.get('limit')
        is_enabled: bool | None = kwargs.get('is_enabled')
        main_credit_card_id: UUID | None = kwargs.get('main_credit_card_id')
        next_closing_date: date | None = kwargs.get('next_closing_date')
        next_expiring_date: date | None = kwargs.get('next_expiring_date')
        financing_limit: Amount | None = kwargs.get('financing_limit')
        expenses: list | None = kwargs.get('expenses')

        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if owner is None or not isinstance(owner, User):
            raise ValueError(f'owner must be an instance of User, got {type(owner)}')
        if alias is None or not isinstance(alias, str) or not alias.strip():
            raise ValueError('alias must be a non-empty string')
        if limit is None or not isinstance(limit, Amount):
            raise ValueError('limit must be a positive number')
        if is_enabled is None or not isinstance(is_enabled, bool):
            raise ValueError('is_enabled must be a boolean')
        if main_credit_card_id is None or not isinstance(main_credit_card_id, UUID):
            raise ValueError(f'main_credit_card_id must be a UUID, got {type(main_credit_card_id)}')
        if next_closing_date is None or not isinstance(next_closing_date, date):
            raise ValueError(f'next_closing_date must be a date, got {type(next_closing_date)}')
        if next_expiring_date is None or not isinstance(next_expiring_date, date):
            raise ValueError(f'next_expiring_date must be a date, got {type(next_expiring_date)}')
        if financing_limit is None or not isinstance(financing_limit, Amount):
            raise ValueError('financing_limit must be a positive number')
        if expenses is None or not isinstance(expenses, list):
            raise ValueError('expenses must be a list')
        not_is_expense = next((e for e in expenses if not isinstance(e, Expense)), None)
        if not_is_expense:
            raise ValueError(f'all items in expenses must be instances of Expense, got {type(not_is_expense)}')
        
        return CreditCard(
            id=id,
            owner=owner,
            alias=alias,
            limit=limit,
            is_enabled=is_enabled,
            main_credit_card_id=main_credit_card_id,
            next_closing_date=next_closing_date,
            next_expiring_date=next_expiring_date,
            financing_limit=financing_limit,
            expenses=expenses,
        )
