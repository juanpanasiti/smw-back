from uuid import UUID
from datetime import date

from ..shared import Amount
from ..account.enums import AccountType
from .enums import PaymentStatus, ExpenseStatus, ExpenseType


class PeriodPayment:
    """
    Payment enriched with related Expense and Account data.
    
    This is a composite value object that aggregates data from Payment, Expense, and Account
    for efficient period-based queries and displays.
    """
    
    def __init__(
        self,
        # Payment data
        payment_id: UUID,
        amount: Amount,
        status: PaymentStatus,
        payment_date: date,
        no_installment: int,
        is_last_payment: bool,
        # Expense data
        expense_id: UUID,
        expense_title: str,
        expense_type: ExpenseType,
        expense_cc_name: str,
        expense_acquired_at: date,
        expense_installments: int,
        expense_status: ExpenseStatus,
        expense_category_name: str | None,
        # Account data
        account_id: UUID,
        account_alias: str,
        account_is_enabled: bool,
        account_type: AccountType,
    ):
        # Payment attributes
        self.payment_id = payment_id
        self.amount = amount
        self.status = status
        self.payment_date = payment_date
        self.no_installment = no_installment
        self.is_last_payment = is_last_payment
        
        # Expense attributes
        self.expense_id = expense_id
        self.expense_title = expense_title
        self.expense_type = expense_type
        self.expense_cc_name = expense_cc_name
        self.expense_acquired_at = expense_acquired_at
        self.expense_installments = expense_installments
        self.expense_status = expense_status
        self.expense_category_name = expense_category_name
        
        # Account attributes
        self.account_id = account_id
        self.account_alias = account_alias
        self.account_is_enabled = account_is_enabled
        self.account_type = account_type
    
    @property
    def is_final_status(self) -> bool:
        """Check if the payment status is final."""
        return self.status in {PaymentStatus.PAID, PaymentStatus.CANCELED}
    
    def to_dict(self) -> dict:
        """Convert the PeriodPayment instance to a dictionary representation."""
        return {
            # Payment data
            'payment_id': str(self.payment_id),
            'amount': self.amount.value,
            'status': self.status.value,
            'payment_date': self.payment_date.isoformat(),
            'no_installment': self.no_installment,
            'is_last_payment': self.is_last_payment,
            
            # Expense data
            'expense_id': str(self.expense_id),
            'expense_title': self.expense_title,
            'expense_type': self.expense_type.value,
            'expense_cc_name': self.expense_cc_name,
            'expense_acquired_at': self.expense_acquired_at.isoformat(),
            'expense_installments': self.expense_installments,
            'expense_status': self.expense_status.value,
            'expense_category_name': self.expense_category_name,
            
            # Account data
            'account_id': str(self.account_id),
            'account_alias': self.account_alias,
            'account_is_enabled': self.account_is_enabled,
            'account_type': self.account_type.value,
        }
