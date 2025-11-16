from uuid import UUID, uuid4
from datetime import date

from ..shared import date_helpers, Amount
from .exceptions import PaymentNotFoundInExpenseException
from .enums import ExpenseType, ExpenseStatus, PaymentStatus
from .expense import Expense
from .payment import Payment
from .payment_factory import PaymentFactory


class Purchase(Expense):
    VALID_STATUS = {ExpenseStatus.PENDING, ExpenseStatus.FINISHED}

    def __init__(
        self,
        id: UUID,
        account_id: UUID,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        installments: int,
        first_payment_date: date,
        category_id: UUID,
        payments: list[Payment],
    ):
        super().__init__(
            id,
            account_id,
            title,
            cc_name,
            acquired_at,
            amount,
            ExpenseType.PURCHASE,
            installments,
            first_payment_date,
            ExpenseStatus.PENDING,
            category_id,
            payments,
        )
        if not payments:
            self.calculate_payments()

    @property
    def paid_amount(self) -> Amount:
        'Calculate the total amount paid for the purchase.'
        total_paid = sum(payment.amount.value for payment in self.payments if payment.is_final_status)
        return Amount(total_paid)

    @property
    def pending_installments(self) -> int:
        'Calculate the number of pending installments.'
        return len([payment for payment in self.payments if not payment.is_final_status])

    @property
    def done_installments(self) -> int:
        'Calculate the number of installments that have been paid.'
        return len([payment for payment in self.payments if payment.is_final_status])

    @property
    def pending_financing_amount(self) -> Amount:
        '''Calculate the pending financing amount of the purchase.'''
        if self.installments == 1:
            # If there is only one installment, there is no financing
            return Amount(0)
        return self.pending_amount

    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the purchase made in one payment.'
        total_amount = self.amount.value
        for payment in self.payments:
            if payment.is_final_status:
                total_amount -= payment.amount.value
        return Amount(total_amount)

    def calculate_payments(self) -> None:
        remaining_amount = self.amount.value
        remaining_installments = self.installments
        payment_date: date = self.first_payment_date or self.acquired_at
        for no in range(1, self.installments + 1):
            installment_amount = Amount(remaining_amount / remaining_installments)
            payment = PaymentFactory.create(
                id=uuid4(),
                expense_id=self.id,
                amount=installment_amount,
                no_installment=no,
                status=PaymentStatus.UNCONFIRMED,
                payment_date=payment_date,
                is_last_payment=(no == self.installments)
            )
            self.payments.append(payment)
            remaining_amount -= installment_amount.value
            remaining_installments -= 1
            payment_date = date_helpers.add_months_to_date(payment_date, 1) if self.installments > 1 else payment_date

    def __update_status(self) -> None:
        'Update the status of the purchase based on current conditions.'
        if any(not payment.is_final_status for payment in self.payments):
            self.status = ExpenseStatus.PENDING
        else:
            self.status = ExpenseStatus.FINISHED

    def update_payment(self, payment: Payment) -> None:
        'Update a specific payment and rebalance the remaining non-final payments to keep totals consistent.'
        payment_to_update = next((p for p in self.payments if p.id == payment.id), None)
        if not payment_to_update:
            raise PaymentNotFoundInExpenseException(f'Payment with id {payment.id} not found in purchase.')

        payment_to_update.amount = payment.amount
        payment_to_update.status = payment.status

        self.__rebalance_open_payments(payment_to_update)

    def __rebalance_open_payments(self, anchor_payment: Payment | None = None) -> None:
        def to_cents(value: float) -> int:
            return int(round(value * 100))

        def assign_amount(payment: Payment, cents: int) -> None:
            precision = getattr(payment.amount, 'precision', 2)
            payment.amount = Amount(cents / 100, precision)

        open_payments = [p for p in self.payments if not p.is_final_status]
        if not open_payments:
            self.__update_status()
            return

        total_cents = to_cents(self.amount.value)
        final_cents = sum(to_cents(payment.amount.value) for payment in self.payments if payment.is_final_status)
        remaining_cents = total_cents - final_cents
        if remaining_cents < 0:
            raise ValueError('Final payments amount cannot exceed purchase total.')

        active_anchor = anchor_payment if anchor_payment and not anchor_payment.is_final_status else None
        payments_to_adjust = open_payments

        if active_anchor:
            anchor_cents = to_cents(active_anchor.amount.value)
            remaining_cents -= anchor_cents
            if remaining_cents < 0:
                raise ValueError('Updated payment amount exceeds available pending amount for purchase.')
            payments_to_adjust = [payment for payment in open_payments if payment.id != active_anchor.id]

        if not payments_to_adjust:
            if remaining_cents != 0:
                raise ValueError('Updated payment amount leaves an inconsistent pending total.')
            self.__update_status()
            return

        slots = len(payments_to_adjust)
        base_cents = remaining_cents // slots
        remainder = remaining_cents % slots

        for payment in payments_to_adjust:
            cents = base_cents + (1 if remainder > 0 else 0)
            remainder = max(0, remainder - 1)
            assign_amount(payment, cents)

        self.__update_status()

    def to_dict(self, include_relations: bool = False) -> dict:
        payments = []
        if include_relations:
            payments = [payment.to_dict() for payment in self.payments]
        else:
            payments = [str(payment.id) for payment in self.payments]
        return {
            # TODO: review
            'id': str(self.id),
            'account_id': str(self.account_id),
            'title': self.title,
            'cc_name': self.cc_name,
            'acquired_at': self.acquired_at.isoformat(),
            'amount': float(self.amount.value),
            'expense_type': self.expense_type.value,
            'installments': self.installments,
            'first_payment_date': self.first_payment_date.isoformat(),
            'status': self.status.value,
            'category_id': str(self.category_id),
            'payments': payments,
        }

    def __repr__(self) -> str:
        return f'<Purchase id={self.id} title="{self.title}" status={self.status}>'