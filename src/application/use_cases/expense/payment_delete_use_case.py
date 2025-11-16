from uuid import UUID

from src.domain.expense import Subscription
from ...ports import PaymentRepository, ExpenseRepository


class PaymentDeleteUseCase:
    def __init__(self, payment_repository: PaymentRepository, expense_repository: ExpenseRepository):
        self.payment_repository = payment_repository
        self.expense_repository = expense_repository

    def execute(self, payment_id: UUID) -> None:
        payment = self.payment_repository.get_by_filter({'id': payment_id})
        if not payment:
            raise ValueError(f'Payment with ID {payment_id} not found')
        
        # Get the expense to update domain fields (like installments for subscriptions)
        expense = self.expense_repository.get_by_filter({'id': payment.expense_id})
        if not expense:
            raise ValueError(f'Expense with ID {payment.expense_id} not found')
        
        # For subscriptions, use domain method to maintain consistency
        if isinstance(expense, Subscription):
            expense.remove_payment(payment_id)
            self.expense_repository.update(expense)
        else:
            # For other expense types, delete directly
            self.payment_repository.delete_by_filter({'id': payment_id})
