from uuid import UUID

from ...ports import BillRepository


class BillDeleteUseCase:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self, bill_id: UUID) -> bool:
        """
        Delete a bill by ID.
        
        Args:
            bill_id: UUID of the bill to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If bill not found or has paid payments
        """
        bill = self.bill_repository.get_by_filter({'id': bill_id})
        if not bill:
            raise ValueError(f'Bill with id {bill_id} not found')
        
        # Check if there are paid payments
        if bill.paid_amount.value > 0:
            raise ValueError('Cannot delete a bill with paid payments')
        
        self.bill_repository.delete_by_filter({'id': bill_id})
        return True
