"""Helper functions for bill group use cases."""
from src.domain.account import BillGroup
from src.domain.expense import Bill
from src.application.dtos import (
    BillGroupResponseDTO,
    BillGroupSummaryDTO,
    BillResponseDTO,
    PaymentResponseDTO,
)
from src.domain.expense.enums import PaymentStatus


def parse_bill_group(bill_group: BillGroup) -> BillGroupResponseDTO:
    """
    Convert a BillGroup domain entity to BillGroupResponseDTO.
    
    Args:
        bill_group: BillGroup domain entity
        
    Returns:
        BillGroupResponseDTO with all computed values
    """
    return BillGroupResponseDTO(
        id=bill_group.id,
        owner_id=bill_group.owner_id,
        alias=bill_group.alias,
        is_enabled=bill_group.is_enabled,
        total_expenses_count=bill_group.total_expenses_count,
        total_bills_count=bill_group.total_bills_count,
        pending_bills_count=bill_group.pending_bills_count,
        used_limit=bill_group.used_limit.value,
        estimated_monthly_cost=bill_group.estimated_monthly_cost.value,
        total_paid_this_year=bill_group.total_paid_this_year.value,
    )


def parse_bill_group_summary(bill_group: BillGroup) -> BillGroupSummaryDTO:
    """
    Convert a BillGroup domain entity to BillGroupSummaryDTO with grouped data.
    
    Args:
        bill_group: BillGroup domain entity
        
    Returns:
        BillGroupSummaryDTO with grouped bills by frequency
    """
    # Count bills by frequency
    bills_by_frequency_count = {
        freq: len(bills) for freq, bills in bill_group.bills_by_frequency.items()
    }
    
    return BillGroupSummaryDTO(
        id=bill_group.id,
        alias=bill_group.alias,
        is_enabled=bill_group.is_enabled,
        total_bills=bill_group.total_bills_count,
        pending_bills=bill_group.pending_bills_count,
        estimated_monthly_cost=bill_group.estimated_monthly_cost.value,
        total_paid_this_year=bill_group.total_paid_this_year.value,
        bills_by_frequency=bills_by_frequency_count,
    )


def parse_bill(bill: Bill) -> BillResponseDTO:
    """
    Convert a Bill domain entity to BillResponseDTO.
    
    Args:
        bill: Bill domain entity
        
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
        date=bill.date,
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
