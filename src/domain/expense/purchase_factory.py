from datetime import date
from uuid import UUID

from ..shared import EntityFactoryBase, Amount
from .purchase import Purchase


class PurchaseFactory(EntityFactoryBase):
    @staticmethod
    def create(**kwargs):
        from .payment import Payment

        id: UUID | None = kwargs.get('id')
        account_id: UUID | None = kwargs.get('account_id')
        title: str | None = kwargs.get('title')
        cc_name: str | None = kwargs.get('cc_name')
        acquired_at: date | None = kwargs.get('acquired_at')
        amount: Amount | None = kwargs.get('amount')
        installments: int | None = kwargs.get('installments')
        first_payment_date: date | None = kwargs.get('first_payment_date')
        category_id: UUID | None = kwargs.get('category_id')
        payments: list['Payment'] | None = kwargs.get('payments')

        # Validations
        if id is None or not isinstance(id, UUID):
            raise ValueError(f'id must be a UUID, got {type(id)}')
        if account_id is None or not isinstance(account_id, UUID):
            raise ValueError(f'account_id must be a UUID, got {type(account_id)}')
        if title is None or not isinstance(title, str) or not title.strip():
            raise ValueError('title must be a non-empty string')
        if cc_name is None or not isinstance(cc_name, str) or not cc_name.strip():
            raise ValueError('cc_name must be a non-empty string')
        if acquired_at is None or not isinstance(acquired_at, date):
            raise ValueError(f'acquired_at must be a date, got {type(acquired_at)}')
        if amount is None or not isinstance(amount, Amount):
            raise ValueError(f'amount must be a valid Amount instance, got {type(amount)}')
        if installments is None or not isinstance(installments, int) or installments < 1:
            raise ValueError('installments must be a positive integer')
        if first_payment_date is None or not isinstance(first_payment_date, date):
            raise ValueError(f'first_payment_date must be a date, got {type(first_payment_date)}')
        if category_id is None or not isinstance(category_id, UUID):
            raise ValueError(f'category_id must be a UUID, got {type(category_id)}')
        if payments is None or not isinstance(payments, list) or not all(isinstance(p, 'Payment') for p in payments):
            raise ValueError('payments must be a list of Payment instances')

        return Purchase(
            id=id,
            account_id=account_id,
            title=title,
            cc_name=cc_name,
            acquired_at=acquired_at,
            amount=amount,
            installments=installments,
            first_payment_date=first_payment_date,
            category_id=category_id,
            payments=payments,
        )
