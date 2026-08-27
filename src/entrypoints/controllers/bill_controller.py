"""
BillController: Handles bill-related HTTP requests.

This controller acts as the entry point for bill operations,
delegating business logic to the application layer use cases.
"""
import logging
from uuid import UUID
from datetime import date

from src.application.dtos import (
    CreateBillDTO,
    UpdateBillDTO,
    UpdateBillNextDateDTO,
    BillResponseDTO,
    UpcomingBillDTO,
    PaginatedResponse,
)
from src.application.use_cases.bill import (
    BillCreateUseCase,
    BillGetOneUseCase,
    BillUpdateUseCase,
    BillUpdateNextDateUseCase,
    BillGetPaginatedUseCase,
    BillDeleteUseCase,
    BillGetUpcomingUseCase,
)
from src.application.ports import BillRepository, BillGroupRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se


logger = logging.getLogger(__name__)


class BillController:
    """
    Controller for bill operations.
    
    Handles CRUD operations for bills by coordinating
    between the presentation layer and application use cases.
    """

    def __init__(
        self, 
        bill_repository: BillRepository,
        bill_group_repository: BillGroupRepository
    ):
        """Initialize the controller with repository dependencies."""
        self._bill_repository: BillRepository = bill_repository
        self._bill_group_repository: BillGroupRepository = bill_group_repository

    def create_bill(self, bill_data: CreateBillDTO) -> BillResponseDTO:
        """
        Create a new bill.

        Args:
            bill_data: CreateBillDTO containing bill information

        Returns:
            BillResponseDTO with created bill information

        Raises:
            BadRequest: If bill data is invalid
            NotFound: If associated bill group is not found
        """
        try:
            logger.info(f'Creating bill: {bill_data.description}')
            use_case = BillCreateUseCase(self._bill_repository, self._bill_group_repository)
            result = use_case.execute(bill_data)
            logger.info(f'Bill created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            error_message = str(ex)
            if 'not found' in error_message.lower():
                logger.warning(f'Bill group not found: {ex}')
                raise ce.NotFound(error_message, 'BILL_GROUP_NOT_FOUND')
            logger.warning(f'Failed to create bill: {ex}')
            raise ce.BadRequest(error_message, 'CREATE_BILL_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating bill: {ex}')
            raise se.InternalServerError()

    def get_bill(self, bill_id: UUID) -> BillResponseDTO:
        """
        Retrieve a bill by its ID.

        Args:
            bill_id: UUID of the bill to retrieve

        Returns:
            BillResponseDTO with bill information

        Raises:
            NotFound: If bill is not found
        """
        try:
            logger.info(f'Retrieving bill with ID: {bill_id}')
            use_case = BillGetOneUseCase(self._bill_repository)
            result = use_case.execute(bill_id)
            if not result:
                raise ce.NotFound(f'Bill {bill_id} not found', 'BILL_NOT_FOUND')
            logger.info(f'Bill retrieved successfully: {bill_id}')
            return result
        except ce.NotFound:
            raise
        except Exception as ex:
            logger.error(f'Unexpected error retrieving bill {bill_id}: {ex}')
            raise se.InternalServerError()

    def update_bill(self, bill_id: UUID, bill_data: UpdateBillDTO) -> BillResponseDTO:
        """
        Update an existing bill.

        Args:
            bill_id: UUID of the bill to update
            bill_data: UpdateBillDTO containing updated information

        Returns:
            BillResponseDTO with updated bill information

        Raises:
            NotFound: If bill is not found
            BadRequest: If data is invalid
        """
        try:
            logger.info(f'Updating bill with ID: {bill_id}')
            use_case = BillUpdateUseCase(self._bill_repository)
            result = use_case.execute(bill_id, bill_data)
            if not result:
                raise ce.NotFound(f'Bill {bill_id} not found', 'BILL_NOT_FOUND')
            logger.info(f'Bill updated successfully: {bill_id}')
            return result
        except ce.NotFound:
            raise
        except ValueError as ex:
            logger.warning(f'Failed to update bill {bill_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_BILL_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating bill {bill_id}: {ex}')
            raise se.InternalServerError()

    def update_bill_next_date(self, bill_id: UUID, update_data: UpdateBillNextDateDTO) -> BillResponseDTO:
        """
        Update the next bill date for a bill.

        Args:
            bill_id: UUID of the bill to update
            update_data: UpdateBillNextDateDTO containing month and year

        Returns:
            BillResponseDTO with updated bill information

        Raises:
            NotFound: If bill is not found
            BadRequest: If data is invalid
        """
        try:
            logger.info(f'Updating next date for bill ID: {bill_id}')
            use_case = BillUpdateNextDateUseCase(self._bill_repository)
            result = use_case.execute(bill_id, update_data)
            if not result:
                raise ce.NotFound(f'Bill {bill_id} not found', 'BILL_NOT_FOUND')
            logger.info(f'Bill next date updated successfully: {bill_id}')
            return result
        except ce.NotFound:
            raise
        except ValueError as ex:
            logger.warning(f'Failed to update bill next date {bill_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_BILL_NEXT_DATE_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating bill next date {bill_id}: {ex}')
            raise se.InternalServerError()

    def delete_bill(self, bill_id: UUID) -> None:
        """
        Delete a bill.

        Args:
            bill_id: UUID of the bill to delete

        Raises:
            NotFound: If bill is not found
            BadRequest: If bill has paid payments
        """
        try:
            logger.info(f'Deleting bill with ID: {bill_id}')
            use_case = BillDeleteUseCase(self._bill_repository)
            use_case.execute(bill_id)
            logger.info(f'Bill deleted successfully: {bill_id}')
        except ValueError as ex:
            error_message = str(ex)
            if 'not found' in error_message.lower():
                logger.warning(f'Bill not found: {bill_id}')
                raise ce.NotFound(error_message, 'BILL_NOT_FOUND')
            logger.warning(f'Failed to delete bill {bill_id}: {ex}')
            raise ce.BadRequest(error_message, 'DELETE_BILL_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error deleting bill {bill_id}: {ex}')
            raise se.InternalServerError()

    def get_paginated_bills(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[BillResponseDTO]:
        """
        Retrieve a paginated list of bills.

        Args:
            filter: Dictionary with filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            PaginatedResponse containing bills and pagination metadata
        """
        try:
            logger.info(f'Retrieving paginated bills with limit={limit}, offset={offset}')
            use_case = BillGetPaginatedUseCase(self._bill_repository)
            result = use_case.execute(filter, limit, offset)
            logger.info(f'Retrieved {len(result.items)} bills')
            return result
        except ValueError as ex:
            logger.warning(f'Invalid pagination parameters: {ex}')
            raise ce.BadRequest(str(ex), 'PAGINATION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving paginated bills: {ex}')
            raise se.InternalServerError()

    def get_upcoming_bills(
        self, 
        owner_id: UUID, 
        year: int | None = None, 
        month: int | None = None
    ) -> list[UpcomingBillDTO]:
        """
        Retrieve upcoming bills for the specified period.

        Args:
            owner_id: UUID of the owner
            year: Year to check (default: current year)
            month: Month to check (default: current month)

        Returns:
            List of UpcomingBillDTO
        """
        try:
            if year is None:
                year = date.today().year
            if month is None:
                month = date.today().month
                
            logger.info(f'Retrieving upcoming bills for {month}/{year}')
            use_case = BillGetUpcomingUseCase(self._bill_repository, self._bill_group_repository)
            result = use_case.execute(owner_id, year, month)
            logger.info(f'Retrieved {len(result)} upcoming bills')
            return result
        except Exception as ex:
            logger.error(f'Unexpected error retrieving upcoming bills: {ex}')
            raise se.InternalServerError()
