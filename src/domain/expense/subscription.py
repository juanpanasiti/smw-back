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
            self.calculate_payments()
    # TODO: Revisar metodos en comun con Purchase para moverlos a la clase base Expense
    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the subscription.'
        total_pending = sum(payment.amount.value for payment in self.payments if payment.status == PaymentStatus.CONFIRMED)
        return Amount(total_pending)

    @property
    def pending_financing_amount(self) -> Amount:
        'A suscription has not financing amounts.'
        return Amount(0)

    def calculate_payments(self) -> None:
        payment = Payment(
            id=uuid4(),
            expense=self,
            amount=self.amount,
            no_installment=1,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=self.first_payment_date
        )
        self.payments.append(payment)

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

    def update_payment(self, payment_id: UUID, payment: Payment) -> None:
        for i, payment in enumerate(self.payments):
            if payment.id == payment_id:
                self.payments[i] = payment
                self.__sort_payments_by_date()
                self.__update_amount()
                return
        raise PaymentNotFoundInExpenseException(f'Payment with ID {payment_id} not found in subscription {self.title}.')

    def get_next_payment(self, factor: Amount = Amount(1.0), is_simulated: bool = False) -> Payment:
        if factor.value <= 0:
            raise ValueError('Factor must be greater than zero')
        last_payment_date = self.payments[-1].payment_date if self.payments else None
        next_payment_date = date_helpers.add_months_to_date(last_payment_date, 1) if last_payment_date else self.acquired_at
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
