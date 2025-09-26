from uuid import UUID
from datetime import date

from ..shared import EntityFactoryBase, Amount
from .enums import PaymentStatus


class PaymentFactory(EntityFactoryBase):
    @classmethod
    def create(cls, **kwargs):
        from .payment import Payment  # Import here to avoid circular dependency
        id: UUID | None = kwargs.get('id')
        expense_id: UUID | None = kwargs.get('expense_id')
        amount: Amount | None = kwargs.get('amount')
        no_installment: int | None= kwargs.get('no_installment')
        status: PaymentStatus | None= kwargs.get('status')
        payment_date: date | None = kwargs.get('payment_date')
        is_last_payment: bool | None = kwargs.get('is_last_payment')


        if id is None or not isinstance(id, UUID):
            raise
        if expense_id is None or not isinstance(expense_id, UUID):
            raise ValueError(f'expense_id must be an instance of UUID, got {type(expense_id)}')
        if amount is None or not isinstance(amount, Amount):
            raise ValueError(f'amount must be an instance of Amount, got {type(amount)}')
        if no_installment is None or no_installment < 1:
            raise ValueError(f'no_installment must be at least 1, got {no_installment}')
        if status is None or not isinstance(status, PaymentStatus):
            raise ValueError(f'status must be an instance of PaymentStatus enum, got {type(status)}')
        if payment_date is None or not isinstance(payment_date, date):
            raise ValueError(f'payment_date must be a date, got {type(payment_date)}')
        
        return Payment(
            id=id,
            expense_id=expense_id,
            amount=amount,
            no_installment=no_installment,
            status=status,
            payment_date=payment_date,
            is_last_payment=bool(is_last_payment),
        )
