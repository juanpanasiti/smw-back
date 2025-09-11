from uuid import UUID, uuid4
from datetime import date

from ..shared import date_helpers, Amount
from ..account import Account
from .exceptions import PaymentNotFoundInExpenseException
from .enums import ExpenseType, ExpenseStatus, PaymentStatus
from .expense import Expense
from .expense_category import ExpenseCategory as Category
from .payment import Payment



class Purchase(Expense):
    VALID_STATUS = {ExpenseStatus.PENDING, ExpenseStatus.FINISHED}

    def __init__(
        self,
        id: UUID,
        account: Account,
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
            account,
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
        total_financing = Amount(0)
        if self.installments == 1:
            # If there is only one installment, there is no financing
            return total_financing
        for payment in self.payments:
            if not payment.is_final_status:
                total_financing += payment.amount
        return total_financing

    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the purchase made in one payment.'
        if self.installments > 1:
            return Amount(0)
        # If the purchase has only one installment and it is not a final status, return the total amount
        if self.payments[0].is_final_status:
            return Amount(0)
        return self.amount

    def calculate_payments(self) -> None:
        remaining_amount = self.amount.value
        remaining_installments = self.installments
        payment_date: date = self.first_payment_date or self.acquired_at
        for no in range(1, self.installments + 1):
            installment_amount = Amount(remaining_amount / remaining_installments)
            payment = Payment(
                id=uuid4(),
                expense=self,
                amount=installment_amount,
                no_installment=no,
                status=PaymentStatus.UNCONFIRMED,
                payment_date=payment_date
            )
            self.payments.append(payment)
            remaining_amount -= installment_amount.value
            remaining_installments -= 1
            payment_date = date_helpers.add_months_to_date(payment_date, 1) if self.installments > 1 else payment_date

    def update_status(self) -> None:
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
            self.update_status()
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
