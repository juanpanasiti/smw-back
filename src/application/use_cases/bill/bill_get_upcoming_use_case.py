from uuid import UUID
from datetime import date

from ...dtos import UpcomingBillDTO
from ...ports import BillRepository, BillGroupRepository
from .helpers import parse_upcoming_bill


class BillGetUpcomingUseCase:
    def __init__(
        self, 
        bill_repository: BillRepository,
        bill_group_repository: BillGroupRepository
    ):
        self.bill_repository = bill_repository
        self.bill_group_repository = bill_group_repository

    def execute(self, owner_id: UUID, year: int | None = None, month: int | None = None) -> list[UpcomingBillDTO]:
        """
        Get upcoming bills for the specified period.
        
        Args:
            owner_id: UUID of the owner
            year: Year to check (default: current year)
            month: Month to check (default: current month)
            
        Returns:
            List of UpcomingBillDTO
        """
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month
        
        # Get all bills for this owner with matching next_bill_month/year
        upcoming_bills = self.bill_repository.get_upcoming_bills(
            owner_id=owner_id,
            year=year,
            month=month
        )
        
        # Get all bill groups for mapping aliases
        bill_groups = self.bill_group_repository.get_many_by_filter(
            {'owner_id': owner_id}, 
            limit=100, 
            offset=0
        )
        bill_group_aliases = {str(bg.id): bg.alias for bg in bill_groups}
        
        result = []
        for bill in upcoming_bills:
            account_alias = bill_group_aliases.get(str(bill.account_id), 'Unknown')
            result.append(parse_upcoming_bill(bill, account_alias))
        
        return result
