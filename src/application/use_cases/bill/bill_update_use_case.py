from uuid import UUID

from ...dtos import UpdateBillDTO, BillResponseDTO
from ...ports import BillRepository
from src.domain.shared import Amount
from .helpers import parse_bill


class BillUpdateUseCase:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self, bill_id: UUID, update_data: UpdateBillDTO) -> BillResponseDTO | None:
        bill = self.bill_repository.get_by_filter({'id': bill_id})
        if not bill:
            return None
        
        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Handle Amount conversion
        if 'amount' in update_dict:
            update_dict['amount'] = Amount(update_dict['amount'])
        
        # Map bill_date to date for entity
        if 'bill_date' in update_dict:
            update_dict['date'] = update_dict.pop('bill_date')
        
        bill.update_from_dict(update_dict)
        
        updated_bill = self.bill_repository.update(bill)
        return parse_bill(updated_bill)
