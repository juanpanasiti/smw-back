from abc import ABC
from uuid import UUID
from datetime import date

from ..shared import EntityBase
from ..shared import Amount
from ..account import Account
from .payment import Payment
from .enums import ExpenseType, ExpenseStatus
from .expense_category import ExpenseCategory as Category
from .exceptions import ExpenseNotImplementedOperation


class Expense(EntityBase, ABC):
    VALID_STATUS = {ExpenseStatus.ACTIVE, ExpenseStatus.PENDING, ExpenseStatus.FINISHED, ExpenseStatus.CANCELLED}

    def __init__(
        self,
        id: UUID,
        account: Account,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        expense_type: ExpenseType,
        installments: int,
        first_payment_date: date,
        status: ExpenseStatus,
        category: Category,
        payments: list[Payment],
    ):
        super().__init__(id)
        self.account = account
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
