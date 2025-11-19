from uuid import UUID

from ..shared import Amount
from ..account import Account
from .payment import Payment
from .expense import Expense
from .period_payment import PeriodPayment


class PeriodPaymentFactory:
    """Factory for creating PeriodPayment instances from Payment, Expense, and Account."""
    
    @staticmethod
    def create_from_entities(
        payment: Payment,
        expense: Expense,
        account: Account,
        category_name: str | None = None,
    ) -> PeriodPayment:
        """
        Create a PeriodPayment from Payment, Expense, and Account entities.
        
        Args:
            payment: Payment entity
            expense: Expense entity associated with the payment
            account: Account entity associated with the expense
            category_name: Optional category name (None if no category)
            
        Returns:
            PeriodPayment instance with aggregated data
        """
        return PeriodPayment(
            # Payment data
            payment_id=payment.id,
            amount=payment.amount,
            status=payment.status,
            payment_date=payment.payment_date,
            no_installment=payment.no_installment,
            is_last_payment=payment.is_last_payment,
            
            # Expense data
            expense_id=expense.id,
            expense_title=expense.title,
            expense_type=expense.expense_type,
            expense_cc_name=expense.cc_name,
            expense_acquired_at=expense.acquired_at,
            expense_installments=expense.installments,
            expense_status=expense.status,
            expense_category_name=category_name,
            
            # Account data
            account_id=account.id,
            account_alias=account.alias,
            account_is_enabled=account.is_enabled,
            account_type=account.account_type,
        )
    
    @staticmethod
    def create(**kwargs) -> PeriodPayment:
        """
        Create a PeriodPayment from a dictionary.
        
        Args:
            **kwargs: Dictionary with all PeriodPayment attributes
            
        Returns:
            PeriodPayment instance
        """
        from .enums import PaymentStatus, ExpenseStatus, ExpenseType
        from ..account.enums import AccountType
        from datetime import date
        
        return PeriodPayment(
            # Payment data
            payment_id=UUID(kwargs['payment_id']),
            amount=Amount(kwargs['amount']),
            status=PaymentStatus(kwargs['status']),
            payment_date=date.fromisoformat(kwargs['payment_date']) if isinstance(kwargs['payment_date'], str) else kwargs['payment_date'],
            no_installment=kwargs['no_installment'],
            is_last_payment=kwargs['is_last_payment'],
            
            # Expense data
            expense_id=UUID(kwargs['expense_id']),
            expense_title=kwargs['expense_title'],
            expense_type=ExpenseType(kwargs['expense_type']),
            expense_cc_name=kwargs['expense_cc_name'],
            expense_acquired_at=date.fromisoformat(kwargs['expense_acquired_at']) if isinstance(kwargs['expense_acquired_at'], str) else kwargs['expense_acquired_at'],
            expense_installments=kwargs['expense_installments'],
            expense_status=ExpenseStatus(kwargs['expense_status']),
            expense_category_name=kwargs.get('expense_category_name'),
            
            # Account data
            account_id=UUID(kwargs['account_id']),
            account_alias=kwargs['account_alias'],
            account_is_enabled=kwargs['account_is_enabled'],
            account_type=AccountType(kwargs['account_type']),
        )
