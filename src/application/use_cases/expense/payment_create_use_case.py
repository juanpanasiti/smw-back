from uuid import uuid4

from src.domain.expense import Payment, Subscription
from src.domain.expense.enums import PaymentStatus
from src.domain.shared import Amount
from ...dtos import CreatePaymentDTO, PaymentResponseDTO
from ...ports import PaymentRepository, ExpenseRepository
from .helpers import parse_payment


class PaymentCreateUseCase:
    def __init__(self, payment_repository: PaymentRepository, expense_repository: ExpenseRepository | None = None):
        self.payment_repository = payment_repository
        self.expense_repository = expense_repository

    def execute(self, payment_data: CreatePaymentDTO) -> PaymentResponseDTO:
        # Validate that the expense exists
        if not self.expense_repository:
            raise ValueError('ExpenseRepository is required for creating payments')
        
        expense = self.expense_repository.get_by_filter({'id': payment_data.expense_id})
        if not expense:
            raise ValueError(f'Expense with ID {payment_data.expense_id} not found')
        
        # Create the payment entity
        payment = Payment(
            id=uuid4(),
            expense_id=payment_data.expense_id,
            amount=Amount(payment_data.amount),
            no_installment=1,  # Will be recalculated by subscription if needed
            status=PaymentStatus.UNCONFIRMED,
            payment_date=payment_data.payment_date,
            is_last_payment=False,
        )
        
        # If it's a subscription, use the domain method to add payment
        # This ensures proper ordering and no_installment calculation
        if isinstance(expense, Subscription):
            expense.add_new_payment(payment)
            # Save the entire subscription with reordered payments
            self.expense_repository.update(expense)
            # Get the payment from the updated subscription
            updated_payment = next((p for p in expense.payments if p.id == payment.id), payment)
            return parse_payment(updated_payment)
        else:
            # For other expense types, create directly
            self.payment_repository.create(payment)
            return parse_payment(payment)
