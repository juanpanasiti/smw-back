from ...dtos import BillGroupResponseDTO, PaginatedResponse, Pagination
from ...ports import BillGroupRepository
from .helpers import parse_bill_group


class BillGroupGetPaginatedUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[BillGroupResponseDTO]:
        bill_groups = self.bill_group_repository.get_many_by_filter(filter, limit, offset)
        total = self.bill_group_repository.count_by_filter(filter)
        bill_groups_dto = [parse_bill_group(bill_group) for bill_group in bill_groups]
        pagination = Pagination(
            current_page=offset // limit + 1,
            total_pages=(total // limit) + 1 if total % limit != 0 else total // limit,
            total_items=total,
            per_page=limit,
        )
        return PaginatedResponse[BillGroupResponseDTO](
            items=bill_groups_dto,
            pagination=pagination,
        )
