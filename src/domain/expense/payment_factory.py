from uuid import UUID
from datetime import date

from ..shared import EntityFactoryBase, Amount
from .enums import PaymentStatus
from .expense import Expense


class PaymentFactory(EntityFactoryBase):
    @classmethod
    def create(cls, **kwargs):
        from .payment import Payment  # Import here to avoid circular dependency
        id: UUID | None = kwargs.get('id')
        expense: Expense | None = kwargs.get('expense')
        amount: Amount | None = kwargs.get('amount')
        no_installment: int | None= kwargs.get('no_installment')
        status: PaymentStatus | None= kwargs.get('status')
        payment_date: date | None = kwargs.get('payment_date')

        if id is None or not isinstance(id, UUID):
            raise
        if expense is None or not isinstance(expense, Expense):
            raise ValueError(f'expense must be an instance of Expense, got {type(expense)}')
        if amount is None or not isinstance(amount, Amount):
            raise ValueError(f'amount must be an instance of Amount, got {type(amount)}')
        if no_installment is None or no_installment < 1 or no_installment > expense.installments:
            raise ValueError(f'no_installment must be between 1 and {expense.installments}, got {no_installment}')
        if status is None or not isinstance(status, PaymentStatus):
            raise ValueError(f'status must be an instance of PaymentStatus enum, got {type(status)}')
        if payment_date is None or not isinstance(payment_date, date):
            raise ValueError(f'payment_date must be a date, got {type(payment_date)}')
        
        return Payment(
            id=id,
            expense=expense,
            amount=amount,
            no_installment=no_installment,
            status=status,
            payment_date=payment_date,
        )
