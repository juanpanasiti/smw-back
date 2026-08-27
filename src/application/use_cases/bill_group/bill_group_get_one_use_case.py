from uuid import UUID

from ...dtos import BillGroupResponseDTO
from ...ports import BillGroupRepository
from .helpers import parse_bill_group


class BillGroupGetOneUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_group_id: UUID) -> BillGroupResponseDTO | None:
        bill_group = self.bill_group_repository.get_by_filter({'id': bill_group_id})
        if not bill_group:
            return None
        return parse_bill_group(bill_group)
