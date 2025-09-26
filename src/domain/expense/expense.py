from abc import ABC
from uuid import UUID
from datetime import date

from ..shared import EntityBase, Amount, Month, Year
from .enums import ExpenseType, ExpenseStatus
from .expense_category import ExpenseCategory as Category
from .exceptions import ExpenseNotImplementedOperation
from .payment import Payment


class Expense(EntityBase, ABC):
    VALID_STATUS = {ExpenseStatus.ACTIVE, ExpenseStatus.PENDING, ExpenseStatus.FINISHED, ExpenseStatus.CANCELLED}

    def __init__(
        self,
        id: UUID,
        account_id: UUID,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        expense_type: ExpenseType,
        installments: int,
        first_payment_date: date,
        status: ExpenseStatus,
        category: Category,
        payments: list['Payment'],
    ):
        super().__init__(id)
        self.account_id = account_id
        self.title = title
        self.cc_name = cc_name
        self.acquired_at = acquired_at
        self.amount = amount
        self.expense_type = expense_type
        self.installments = installments
        self.first_payment_date = first_payment_date
        self.status = status
        self.category = category
        self.payments = payments if payments is not None else []

    @property
    def is_one_time_payment(self) -> bool:
        'Check if the payment is a one-time payment.'
        if self.expense_type != ExpenseType.PURCHASE:
            return False
        return self.installments == 1

    @property
    def paid_amount(self) -> Amount:
        raise ExpenseNotImplementedOperation(f'"paid_amount()" is not implemented for "{self.expense_type.value}" expenses.')

    @property
    def pending_installments(self) -> int:
        raise ExpenseNotImplementedOperation(f'"pending_installments()" is not implemented for "{self.expense_type.value}" expenses.')

    @property
    def done_installments(self) -> int:
        raise ExpenseNotImplementedOperation(f'"done_installments()" is not implemented for "{self.expense_type.value}" expenses.')

    @property
    def pending_financing_amount(self) -> Amount:
        raise ExpenseNotImplementedOperation(f'"pending_financing_amount()" is not implemented for "{self.expense_type.value}" expenses.    ')

    @property
    def pending_amount(self) -> Amount:
        raise ExpenseNotImplementedOperation(f'"pending_amount()" is not implemented for "{self.expense_type.value}" expenses.')

    def calculate_payments(self) -> None:
        raise ExpenseNotImplementedOperation(f'"calculate_payments()" is not implemented for "{self.expense_type.value}" expenses.')

    def get_payments(self, month: Month | None = None, year: Year | None = None) -> list['Payment']:
        'Get all payments for this expense in a given month and year.'
        if (month is None and year is not None) or (month is not None and year is None):
            raise ValueError('Both month and year must be provided together or both must be None')
        payments = []
        for payment in self.payments:
            if (month is None or payment.payment_date.month == month) and (year is None or payment.payment_date.year == year):
                payments.append(payment)
        return payments
