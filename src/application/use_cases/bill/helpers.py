"""Helper functions for bill use cases."""
from src.domain.expense import Bill
from src.application.dtos import (
    BillResponseDTO,
    PaymentResponseDTO,
    UpcomingBillDTO,
)
from src.domain.expense.enums import PaymentStatus


def parse_bill(bill: Bill, account_alias: str = '') -> BillResponseDTO:
    """
    Convert a Bill domain entity to BillResponseDTO.
    
    Args:
        bill: Bill domain entity
        account_alias: Optional alias of the parent BillGroup
        
    Returns:
        BillResponseDTO with all computed values
    """
    payments = [
        PaymentResponseDTO(
            id=p.id,
            expense_id=p.expense_id,
            amount=p.amount.value,
            no_installment=p.no_installment,
            status=PaymentStatus(p.status) if isinstance(p.status, str) else p.status,
            payment_date=p.payment_date,
            is_last_payment=p.is_last_payment,
        )
        for p in bill.payments
    ]
    
    return BillResponseDTO(
        id=bill.id,
        account_id=bill.account_id,
        description=bill.description,
        amount=bill.amount.value,
        bill_date=bill.date,
        frequency=bill.frequency,
        next_bill_month=bill.next_bill_month,
        next_bill_year=bill.next_bill_year,
        next_bill_date_display=bill.next_bill_date_display,
        notes=bill.notes,
        total_amount=bill.total_amount.value,
        paid_amount=bill.paid_amount.value,
        pending_amount=bill.pending_amount.value,
        is_fully_paid=bill.is_fully_paid,
        payments=payments,
    )


def parse_upcoming_bill(bill: Bill, account_alias: str) -> UpcomingBillDTO:
    """
    Convert a Bill domain entity to UpcomingBillDTO for notifications.
    
    Args:
        bill: Bill domain entity
        account_alias: Alias of the parent BillGroup
        
    Returns:
        UpcomingBillDTO
    """
    return UpcomingBillDTO(
        id=bill.id,
        account_id=bill.account_id,
        account_alias=account_alias,
        description=bill.description,
        amount=bill.amount.value,
        frequency=bill.frequency,
        next_bill_month=bill.next_bill_month,
        next_bill_year=bill.next_bill_year,
        next_bill_date_display=bill.next_bill_date_display or '',
        notes=bill.notes,
    )
