from datetime import date
from uuid import UUID

from ..shared import EntityFactoryBase, Amount



class PurchaseFactory(EntityFactoryBase):
    @staticmethod
    def create(**kwargs):
        from ..account import Account
        from .purchase import Purchase
        from .expense_category import ExpenseCategory as Category
        from .payment import Payment

        id: UUID | None = kwargs.get('id')
        account: Account | None = kwargs.get('account')
        title: str | None = kwargs.get('title')
        cc_name: str | None = kwargs.get('cc_name')
        acquired_at: date | None = kwargs.get('acquired_at')
        amount: int | float | None = kwargs.get('amount')
        installments: int | None = kwargs.get('installments')
        first_payment_date: date | None = kwargs.get('first_payment_date')
        category: Category | None = kwargs.get('category')
        payments: list[Payment] | None = kwargs.get('payments')

        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if account is None or not isinstance(account, Account):
            raise ValueError(f'account must be an instance of Account, got {type(account)}')
        if title is None or not isinstance(title, str) or not title.strip():
            raise ValueError('title must be a non-empty string')
        if cc_name is None or not isinstance(cc_name, str) or not cc_name.strip():
            raise ValueError('cc_name must be a non-empty string')
        if acquired_at is None or not isinstance(acquired_at, date):
            raise ValueError(f'acquired_at must be a date, got {type(acquired_at)}')
        if amount is None or not isinstance(amount, Amount):
            raise ValueError('amount must be a positive number')
        if installments is None or not isinstance(installments, int) or installments < 1:
            raise ValueError('installments must be a positive integer')
        if first_payment_date is None or not isinstance(first_payment_date, date):
            raise ValueError(f'first_payment_date must be a date, got {type(first_payment_date)}')
        if category is None or not isinstance(category, Category):
            raise ValueError(f'category must be an instance of Category, got {type(category)}')
        if payments is None or not isinstance(payments, list) or not all(isinstance(p, Payment) for p in payments):
            raise ValueError('payments must be a list of Payment instances')

        return Purchase(
            id=id,
            account=account,
            title=title,
            cc_name=cc_name,
            acquired_at=acquired_at,
            amount=amount,
            installments=installments,
            first_payment_date=first_payment_date,
            category=category,
            payments=payments,
        )
