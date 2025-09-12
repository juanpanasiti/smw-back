from abc import ABC
from uuid import UUID
from datetime import date

from ..shared import EntityBase
from ..shared import Amount
from ..account import Account
from .payment import Payment
from .enums import ExpenseType, ExpenseStatus
from .expense_category import ExpenseCategory as Category


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
