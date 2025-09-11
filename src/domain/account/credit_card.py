from uuid import UUID
from datetime import date

from src.domain.expense.purchase_factory import PurchaseFactory


from ..auth import User


# from ..period.models.period import Period
from .account import Account
from ..shared import Amount


class CreditCard(Account):
    from ..expense.purchase_factory import PurchaseFactory
    def __init__(
        self,
        owner: User,
        alias: str,
        limit: Amount,
        is_enabled: bool,
        main_credit_card_id: UUID,
        next_closing_date: date,
        next_expiring_date: date,
        financing_limit: Amount,
        expenses: list,
        # periods: list[Period],
        id: UUID,
    ):
        super().__init__(id, owner, alias, limit, is_enabled)
        self.main_credit_card_id = main_credit_card_id
        self.next_closing_date = next_closing_date
        self.next_expiring_date = next_expiring_date
        self.financing_limit = financing_limit
        self.expenses = expenses
        # self.periods = periods if periods is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> 'CreditCard':
        '''Create a CreditCard instance from a dictionary representation.'''
        return cls(
            id=data['id'],
            owner=User.from_dict(data['owner']),
            alias=data['alias'],
            limit=Amount(data['limit']),
            is_enabled=data['is_enabled', True],
            main_credit_card_id=data['main_credit_card_id'],
            next_closing_date=data['next_closing_date'],
            next_expiring_date=data['next_expiring_date'],
            financing_limit=Amount(data['financing_limit']),
            expenses=cls.expense_list_from_dict(data['expenses']),
        )

    @staticmethod
    def expense_list_from_dict(data: list[dict]) -> list:
        '''Convert a list of expense dictionaries to a list of Expense instances.'''
        from ..expense import  ExpenseType, Subscription
        expenses = []
        for exp_data in data:
            match exp_data.get('expense_type'):
                case ExpenseType.PURCHASE.value:
                    expenses.append(PurchaseFactory.create(**exp_data))
                case ExpenseType.SUBSCRIPTION.value:
                    pass
                    expenses.append(Subscription.from_dict(exp_data))
        return expenses
