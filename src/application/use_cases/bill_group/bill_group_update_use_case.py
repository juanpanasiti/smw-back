from uuid import UUID

from ...dtos import UpdateBillGroupDTO, BillGroupResponseDTO
from ...ports import BillGroupRepository
from .helpers import parse_bill_group


class BillGroupUpdateUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_group_id: UUID, update_data: UpdateBillGroupDTO) -> BillGroupResponseDTO | None:
        bill_group = self.bill_group_repository.get_by_filter({'id': bill_group_id})
        if not bill_group:
            return None
        
        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        bill_group.update_from_dict(update_dict)
        
        updated_bill_group = self.bill_group_repository.update(bill_group)
        return parse_bill_group(updated_bill_group)
