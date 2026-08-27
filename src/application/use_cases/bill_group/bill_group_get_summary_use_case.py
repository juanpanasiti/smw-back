from uuid import UUID

from ...dtos import BillGroupSummaryDTO
from ...ports import BillGroupRepository
from .helpers import parse_bill_group_summary


class BillGroupGetSummaryUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_group_id: UUID) -> BillGroupSummaryDTO | None:
        bill_group = self.bill_group_repository.get_by_filter({'id': bill_group_id})
        if not bill_group:
            return None
        return parse_bill_group_summary(bill_group)
