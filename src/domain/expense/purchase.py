from uuid import UUID, uuid4
from datetime import date

from ..shared import date_helpers, Amount
from .exceptions import PaymentNotFoundInExpenseException
from .enums import ExpenseType, ExpenseStatus, PaymentStatus
from .expense import Expense
from .expense_category import ExpenseCategory as Category
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
        category: Category,
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
            category,
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
        'Update a specific payment and adjust the purchase status and unconfirmed payment amounts accordingly.'
        payment_to_update = next((p for p in self.payments if p.id == payment.id), None)
        if not payment_to_update:
            raise PaymentNotFoundInExpenseException(f'Payment with id {payment.id} not found in purchase.')

        payment_to_update.amount = payment.amount
        payment_to_update.status = payment.status

        pending_payments = [p for p in self.payments if not p.is_final_status]
        if not pending_payments:
            self.__update_status()
            return

        pendig_amount = self.pending_amount
        if all(payment.status == PaymentStatus.CONFIRMED for payment in pending_payments):
            self.amount = Amount(sum(payment.amount.value for payment in pending_payments))
            return

        for payment in pending_payments:
            if payment.status == PaymentStatus.CONFIRMED:
                continue
            else:
                payment.amount = Amount(pendig_amount.value / len(pending_payments))
                pendig_amount = Amount(pendig_amount.value - payment.amount.value)

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
            'category': self.category.to_dict() if include_relations else str(self.category.id),
            'payments': payments,
        }

    def __repr__(self) -> str:
        return f'<Purchase id={self.id} title="{self.title}" status={self.status}>'