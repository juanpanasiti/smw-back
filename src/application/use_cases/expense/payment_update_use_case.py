from uuid import UUID

from src.domain.expense import Payment, Purchase, Subscription
from src.domain.shared import Amount
from ...dtos import UpdatePaymentDTO, PaymentResponseDTO
from ...ports import PaymentRepository, ExpenseRepository
from .helpers import parse_payment


class PaymentUpdateUseCase:
    def __init__(self, payment_repository: PaymentRepository, expense_repository: ExpenseRepository):
        self.payment_repository = payment_repository
        self.expense_repository = expense_repository

    def execute(self, payment_id: UUID, payment_data: UpdatePaymentDTO) -> PaymentResponseDTO:
        payment = self.payment_repository.get_by_filter({'id': payment_id})
        if not payment:
            raise ValueError(f'Payment with ID {payment_id} not found')
        
        # Update payment fields
        payment.amount = Amount(payment_data.amount)
        payment.status = payment_data.status
        payment.payment_date = payment_data.payment_date
        
        # Update through the expense to trigger rebalance/reordering
        expense = self.expense_repository.get_by_filter({'id': payment.expense_id})
        if not expense:
            raise ValueError(f'Expense with ID {payment.expense_id} not found')
            
        if isinstance(expense, Purchase):
            # Use Purchase.update_payment which triggers rebalance
            expense.update_payment(payment)
        elif isinstance(expense, Subscription):
            # Use Subscription.update_payment which triggers reordering
            expense.update_payment(payment_id, payment)
        else:
            # For other expense types, update payment directly
            self.payment_repository.update(payment)
            return parse_payment(payment)
        
        # Save the entire expense (which includes updated payments)
        self.expense_repository.update(expense)
        # Get the updated payment from the expense
        updated_payment = next((p for p in expense.payments if p.id == payment_id), payment)
        return parse_payment(updated_payment)
