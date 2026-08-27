from uuid import uuid4

from ...dtos import CreateBillGroupDTO, BillGroupResponseDTO
from ...ports import BillGroupRepository
from src.domain.account import BillGroupFactory
from .helpers import parse_bill_group


class BillGroupCreateUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_group_data: CreateBillGroupDTO) -> BillGroupResponseDTO:
        bill_group = BillGroupFactory.create(
            id=uuid4(),
            owner_id=bill_group_data.owner_id,
            alias=bill_group_data.alias,
            is_enabled=bill_group_data.is_enabled,
            expenses=[],
        )
        new_bill_group = self.bill_group_repository.create(bill_group)
        return parse_bill_group(new_bill_group)
