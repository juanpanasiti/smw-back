import re
from uuid import UUID
from datetime import date
from typing import TYPE_CHECKING

from ..shared import EntityBase
from ..shared import Amount
from .enums import PaymentStatus


if TYPE_CHECKING:
    from .expense import Expense


class Payment(EntityBase):

    def __init__(
            self,
            id: UUID,
            expense_id: UUID,
            amount: Amount,
            no_installment: int,
            status: PaymentStatus,
            payment_date: date,
            is_last_payment: bool,
    ) -> None:
        super().__init__(id)
        self.expense_id = expense_id
        self.amount = amount
        self.no_installment = no_installment
        self.status = status
        self.payment_date = payment_date
        self.is_last_payment = is_last_payment

    @property
    def is_final_status(self) -> bool:
        'Check if the payment status is final.'
        return self.status in {PaymentStatus.PAID, PaymentStatus.CANCELED}

    def to_dict(self) -> dict:
        '''Convert the Payment instance to a dictionary representation.'''
        return {
            'id': str(self.id),
            'expense_id': str(self.expense_id),
            'amount': float(self.amount.value),
            'no_installment': self.no_installment,
            'status': self.status.value,
            'payment_date': self.payment_date.isoformat(),
        }
