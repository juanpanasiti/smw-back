from ...dtos import BillResponseDTO, PaginatedResponse, Pagination
from ...ports import BillRepository
from .helpers import parse_bill


class BillGetPaginatedUseCase:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[BillResponseDTO]:
        bills = self.bill_repository.get_many_by_filter(filter, limit, offset)
        total = self.bill_repository.count_by_filter(filter)
        bills_dto = [parse_bill(bill) for bill in bills]
        pagination = Pagination(
            current_page=offset // limit + 1,
            total_pages=(total // limit) + 1 if total % limit != 0 else total // limit,
            total_items=total,
            per_page=limit,
        )
        return PaginatedResponse[BillResponseDTO](
            items=bills_dto,
            pagination=pagination,
        )
