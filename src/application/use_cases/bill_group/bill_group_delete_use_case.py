from uuid import UUID

from ...ports import BillGroupRepository


class BillGroupDeleteUseCase:
    def __init__(self, bill_group_repository: BillGroupRepository):
        self.bill_group_repository = bill_group_repository

    def execute(self, bill_group_id: UUID) -> bool:
        """
        Delete a bill group by ID.
        
        Args:
            bill_group_id: UUID of the bill group to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If bill group not found
        """
        bill_group = self.bill_group_repository.get_by_filter({'id': bill_group_id})
        if not bill_group:
            raise ValueError(f'Bill group with id {bill_group_id} not found')
        
        # Check if there are pending bills
        if bill_group.pending_bills_count > 0:
            raise ValueError(f'Cannot delete bill group with {bill_group.pending_bills_count} pending bills')
        
        self.bill_group_repository.delete_by_filter({'id': bill_group_id})
        return True
