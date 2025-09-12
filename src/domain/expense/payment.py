import re
from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..shared import EntityBase
from ..shared import Amount
from .enums import PaymentStatus, ExpenseType


if TYPE_CHECKING:
    from .expense import Expense


class Payment(EntityBase):

    def __init__(
            self,
            id: UUID,
            expense: 'Expense',
            amount: Amount,
            no_installment: int,
            status: PaymentStatus,
            payment_date: date,
    ) -> None:
        super().__init__(id)
        self.expense = expense
        self.amount = amount
        self.no_installment = no_installment
        self.status = status
        self.payment_date = payment_date

    @property
    def is_final_status(self) -> bool:
        'Check if the payment status is final.'
        return self.status in {PaymentStatus.PAID, PaymentStatus.CANCELED}

    @property
    def is_last_payment(self) -> bool:
        'Check if this is the last payment for the expense.'
        from .purchase import Purchase
        if self.is_final_status:
            return False
        if isinstance(self.expense, Purchase) and self.expense.pending_installments == 1:
            return True
        return False

    def to_dict(self, include_relationships: bool = False) -> dict:
        '''Convert the Payment instance to a dictionary representation.'''
        return {
            'id': str(self.id),
            'expense': self.expense.to_dict() if include_relationships else str(self.expense.id),
            'amount': float(self.amount.value),
            'no_installment': self.no_installment,
            'status': self.status.value,
            'payment_date': self.payment_date.isoformat(),
        }
