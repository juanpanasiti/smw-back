from uuid import uuid4

from ...dtos import CreateBillDTO, BillResponseDTO
from ...ports import BillRepository, BillGroupRepository
from src.domain.expense import BillFactory, PaymentFactory
from src.domain.expense.enums import PaymentStatus
from src.domain.shared import Amount
from .helpers import parse_bill


class BillCreateUseCase:
    def __init__(
        self, 
        bill_repository: BillRepository,
        bill_group_repository: BillGroupRepository
    ):
        self.bill_repository = bill_repository
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_data: CreateBillDTO) -> BillResponseDTO:
        # Verify that the account is a BillGroup
        bill_group = self.bill_group_repository.get_by_filter({'id': bill_data.account_id})
        if not bill_group:
            raise ValueError(f'BillGroup with id {bill_data.account_id} not found')
        
        # Create payments from DTO
        payments = []
        for i, payment_data in enumerate(bill_data.payments):
            payment = PaymentFactory.create(
                id=uuid4(),
                expense_id=uuid4(),  # Will be updated after bill creation
                amount=Amount(payment_data.amount),
                no_installment=i + 1,
                status=PaymentStatus.UNCONFIRMED,
                payment_date=payment_data.payment_date,
                is_last_payment=(i == len(bill_data.payments) - 1),
            )
            payments.append(payment)
        
        # If no payments provided, create a default one
        if not payments:
            payment = PaymentFactory.create(
                id=uuid4(),
                expense_id=uuid4(),
                amount=Amount(bill_data.amount),
                no_installment=1,
                status=PaymentStatus.UNCONFIRMED,
                payment_date=bill_data.bill_date,
                is_last_payment=True,
            )
            payments.append(payment)
        
        bill = BillFactory.create(
            id=uuid4(),
            account_id=bill_data.account_id,
            description=bill_data.description,
            amount=Amount(bill_data.amount),
            date=bill_data.bill_date,
            frequency=bill_data.frequency,
            next_bill_month=bill_data.next_bill_month,
            next_bill_year=bill_data.next_bill_year,
            notes=bill_data.notes,
            payments=payments,
        )
        
        # Update payment expense_ids to match bill id
        for payment in bill.payments:
            payment.expense_id = bill.id
        
        new_bill = self.bill_repository.create(bill)
        return parse_bill(new_bill)
