from uuid import UUID

from ...dtos import BillResponseDTO
from ...ports import BillRepository
from .helpers import parse_bill


class BillGetOneUseCase:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self, bill_id: UUID) -> BillResponseDTO | None:
        bill = self.bill_repository.get_by_filter({'id': bill_id})
        if not bill:
            return None
        return parse_bill(bill)
