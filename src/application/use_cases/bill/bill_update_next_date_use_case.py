from uuid import UUID

from ...dtos import UpdateBillNextDateDTO, BillResponseDTO
from ...ports import BillRepository
from .helpers import parse_bill


class BillUpdateNextDateUseCase:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self, bill_id: UUID, update_data: UpdateBillNextDateDTO) -> BillResponseDTO | None:
        bill = self.bill_repository.get_by_filter({'id': bill_id})
        if not bill:
            return None
        
        # Use the domain method to set next bill date
        bill.set_next_bill_date(
            month=update_data.next_bill_month,
            year=update_data.next_bill_year
        )
        
        updated_bill = self.bill_repository.update(bill)
        return parse_bill(updated_bill)
