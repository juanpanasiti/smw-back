
from src.domain.expense import Payment, Expense
from ...dtos import ExpenseResponseDTO, PaymentResponseDTO


def parse_expense(expense: Expense) -> ExpenseResponseDTO:
    return ExpenseResponseDTO(
        id=expense.id,
        account_id=expense.account_id,
        title=expense.title,
        cc_name=expense.cc_name,
        acquired_at=expense.acquired_at,
        amount=expense.amount.value,
        expense_type=expense.expense_type,
        installments=expense.installments,
        first_payment_date=expense.first_payment_date,
        status=expense.status,
        category_id=expense.category_id,
        payments=[parse_payment(payment) for payment in expense.payments],
        is_one_time_payment=expense.is_one_time_payment,
        paid_amount=expense.paid_amount.value,
        pending_installments=expense.pending_installments,
        done_installments=expense.done_installments,
        pending_financing_amount=expense.pending_financing_amount.value,
        pending_amount=expense.pending_amount.value,
    )


def parse_payment(payment: Payment) -> PaymentResponseDTO:
    return PaymentResponseDTO(
        id=payment.id,
        expense_id=payment.expense_id,
        amount=payment.amount.value,
        no_installment=payment.no_installment,
        status=payment.status,
        payment_date=payment.payment_date,
        is_last_payment=payment.is_last_payment,
    )
