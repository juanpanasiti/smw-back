from uuid import UUID

from ..shared import EntityBase, Amount
from ..account import Account
from .payment import Payment


class Period(EntityBase):
    def __init__(
        self,
        id: UUID,
        month: int,
        year: int,
        payments: list[Payment],
    ):
        super().__init__(id)
        self.month = month
        self.year = year
        self.payments = payments

    @property
    def period_str(self) -> str:
        'Return the period in MM/YYYY format.'
        return f'{self.month:02}/{self.year}'

    @property
    def total_amount(self) -> Amount:
        'Calculate the total amount of all payments in this period.'
        total = sum(payment.amount.value for payment in self.payments)
        return Amount(total)

    @property
    def total_paid_amount(self) -> Amount:
        'Calculate the total amount of all paid payments in this period.'
        total = sum(payment.amount.value for payment in self.payments if payment.status == 'paid')
        return Amount(total)

    @property
    def total_pending_amount(self) -> Amount:
        'Calculate the total amount of all pending payments in this period.'
        total = sum(payment.amount.value for payment in self.payments if payment.status == 'pending')
        return Amount(total)

    @property
    def pending_payments(self) -> list[Payment]:
        'Return a list of payments that are not in a final status.'
        return [payment for payment in self.payments if not payment.is_final_status]

    @property
    def completed_payments(self) -> list[Payment]:
        'Return a list of payments that are in a final status.'
        return [payment for payment in self.payments if payment.is_final_status]

    @property
    def total_payments(self) -> int:
        'Return the total number of payments in this period.'
        return len(self.payments)

    def to_dict(self, include_relationships: bool = False) -> dict:
        '''Convert the Period instance to a dictionary representation.'''
        return {
            'id': str(self.id),
            'month': self.month,
            'year': self.year,
            'payments': [p.to_dict(include_relationships) for p in self.payments] if include_relationships else [str(p.id) for p in self.payments],
        }
    
    def add_payment(self, payment: Payment):
        'Add a payment to the period.'
        if not isinstance(payment, Payment):
            raise ValueError('payment must be an instance of Payment')
        existing_payment = next((p for p in self.payments if p.id == payment.id), None)
        if not existing_payment:
            self.payments.append(payment)

    def fill_from_account(self, account: Account):
        'Fill the period with payments from the given account.'
        for payment in account.get_payments(self.month, self.year):
            try:
                self.add_payment(payment)
            except ValueError:
                continue
