from uuid import UUID, uuid4
from datetime import date

from ..shared import date_helpers, Amount
from ..account import Account
from .exceptions import PaymentNotFoundInExpenseException
from .enums import ExpenseType, ExpenseStatus, PaymentStatus
from .expense import Expense
from .expense_category import ExpenseCategory as Category
from .payment import Payment


class Subscription(Expense):
    VALID_STATUS = {ExpenseStatus.ACTIVE, ExpenseStatus.CANCELLED}

    def __init__(
        self,
        id: UUID,
        account: Account,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
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
            ExpenseType.SUBSCRIPTION,
            1,  # Subscriptions typically have one installment at the beginning
            first_payment_date,
            ExpenseStatus.ACTIVE,
            category,
            payments,
        )
        if not payments:
            next_payment = self.get_next_payment()
            self.payments.append(next_payment)
    # TODO: Revisar metodos en comun con Purchase para moverlos a la clase base Expense

    @property
    def paid_amount(self) -> Amount:
        'Calculate the total amount paid for the subscription.'
        total_paid = sum(payment.amount.value for payment in self.payments if payment.status == PaymentStatus.PAID)
        return Amount(total_paid)

    @property
    def pending_installments(self) -> int:
        return len([p for p in self.payments if p.status not in {PaymentStatus.PAID, PaymentStatus.CANCELED}])

    @property
    def done_installments(self) -> int:
        'Calculate the number of done installments for the subscription.'
        return len([p for p in self.payments if p.status == PaymentStatus.PAID])

    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the subscription.'
        total_pending = sum(payment.amount.value for payment in self.payments if payment.status not in {PaymentStatus.PAID, PaymentStatus.CANCELED})
        return Amount(total_pending)

    @property
    def pending_financing_amount(self) -> Amount:
        'A suscription has not financing amounts.'
        return Amount(0)

    def add_new_payment(self, payment: Payment) -> None:
        if payment.expense.id != self.id:
            raise ValueError('Payment expense ID does not match subscription ID')
        self.amount = payment.amount
        self.payments.append(payment)
        self.__sort_payments_by_date()
        self.__update_amount()

    def remove_payment(self, payment_id: UUID) -> None:
        for payment in self.payments:
            if payment.id == payment_id:
                self.payments.remove(payment)
                self.__update_amount()
                return
        raise PaymentNotFoundInExpenseException(f'Payment with ID {payment_id} not found in subscription {self.title}.')

    def update_payment(self, payment_id: UUID, payment_updated: Payment) -> None:
        for i, payment in enumerate(self.payments):
            if payment.id == payment_id:
                self.payments[i] = payment_updated
                self.__sort_payments_by_date()
                self.__update_amount()
                return
        if self.payments[-1].id == payment_id:
            self.amount = payment_updated.amount
        raise PaymentNotFoundInExpenseException(f'Payment with ID {payment_id} not found in subscription {self.title}.')

    def get_next_payment(self, factor: Amount = Amount(1.0), is_simulated: bool = False) -> Payment:
        if factor.value <= 0:
            raise ValueError('Factor must be greater than zero')
        last_payment_date = self.payments[-1].payment_date if self.payments else None
        next_payment_date = date_helpers.add_months_to_date(last_payment_date, 1) if last_payment_date else self.first_payment_date
        return Payment(
            id=uuid4(),
            expense=self,
            amount=Amount(self.amount.value * factor.value),
            no_installment=len(self.payments) + 1,
            status=PaymentStatus.SIMULATED if is_simulated else PaymentStatus.UNCONFIRMED,
            payment_date=next_payment_date
        )

    def __sort_payments_by_date(self) -> None:
        self.payments.sort(key=lambda p: p.payment_date if p.payment_date else date.min)
        for i, payment in enumerate(self.payments, start=1):
            if payment.no_installment != i:
                payment.no_installment = i

    def __update_amount(self) -> None:
        '''Update amount if the last payment amount changed.'''
        last_payment = self.payments[-1] if self.payments else None
        if last_payment and last_payment.amount != self.amount:
            self.amount = last_payment.amount

    def to_dict(self, include_relationships: bool = False) -> dict:
        account = self.account.to_dict() if include_relationships else str(self.account.id)
        category = self.category.to_dict() if include_relationships else str(self.category.id)
        payments = []
        if include_relationships:
            payments = [payment.to_dict(include_relationships=include_relationships) for payment in self.payments]
        else:
            payments = [str(payment.id) for payment in self.payments]
        return {
            'id': str(self.id),
            'account': account,
            'title': self.title,
            'cc_name': self.cc_name,
            'acquired_at': self.acquired_at.isoformat(),
            'amount': float(self.amount.value),
            'first_payment_date': self.first_payment_date.isoformat(),
            'category': category,
            'payments': payments,
            'expense_type': self.expense_type.value,
            'status': self.status.value,
            'installments': self.installments,
        }
