"""
BillGroupController: Handles bill group-related HTTP requests.

This controller acts as the entry point for bill group operations,
delegating business logic to the application layer use cases.
"""
import logging
from uuid import UUID

from src.application.dtos import (
    CreateBillGroupDTO,
    UpdateBillGroupDTO,
    BillGroupResponseDTO,
    BillGroupSummaryDTO,
    PaginatedResponse,
)
from src.application.use_cases.bill_group import (
    BillGroupCreateUseCase,
    BillGroupGetOneUseCase,
    BillGroupUpdateUseCase,
    BillGroupGetPaginatedUseCase,
    BillGroupDeleteUseCase,
    BillGroupGetSummaryUseCase,
)
from src.application.ports import BillGroupRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se


logger = logging.getLogger(__name__)


class BillGroupController:
    """
    Controller for bill group operations.
    
    Handles CRUD operations for bill groups by coordinating
    between the presentation layer and application use cases.
    """

    def __init__(self, bill_group_repository: BillGroupRepository):
        """Initialize the controller with repository dependencies."""
        self._bill_group_repository: BillGroupRepository = bill_group_repository

    def create_bill_group(self, bill_group_data: CreateBillGroupDTO) -> BillGroupResponseDTO:
        """
        Create a new bill group.

        Args:
            bill_group_data: CreateBillGroupDTO containing bill group information

        Returns:
            BillGroupResponseDTO with created bill group information

        Raises:
            BadRequest: If bill group data is invalid
        """
        try:
            logger.info(f'Creating bill group with alias: {bill_group_data.alias}')
            use_case = BillGroupCreateUseCase(self._bill_group_repository)
            result = use_case.execute(bill_group_data)
            logger.info(f'Bill group created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create bill group: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_BILL_GROUP_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating bill group: {ex}')
            raise se.InternalServerError()

    def get_bill_group(self, bill_group_id: UUID) -> BillGroupResponseDTO:
        """
        Retrieve a bill group by its ID.

        Args:
            bill_group_id: UUID of the bill group to retrieve

        Returns:
            BillGroupResponseDTO with bill group information

        Raises:
            NotFound: If bill group is not found
        """
        try:
            logger.info(f'Retrieving bill group with ID: {bill_group_id}')
            use_case = BillGroupGetOneUseCase(self._bill_group_repository)
            result = use_case.execute(bill_group_id)
            if not result:
                raise ce.NotFound(f'Bill group {bill_group_id} not found', 'BILL_GROUP_NOT_FOUND')
            logger.info(f'Bill group retrieved successfully: {bill_group_id}')
            return result
        except ce.NotFound:
            raise
        except Exception as ex:
            logger.error(f'Unexpected error retrieving bill group {bill_group_id}: {ex}')
            raise se.InternalServerError()

    def update_bill_group(self, bill_group_id: UUID, bill_group_data: UpdateBillGroupDTO) -> BillGroupResponseDTO:
        """
        Update an existing bill group.

        Args:
            bill_group_id: UUID of the bill group to update
            bill_group_data: UpdateBillGroupDTO containing updated information

        Returns:
            BillGroupResponseDTO with updated bill group information

        Raises:
            NotFound: If bill group is not found
            BadRequest: If data is invalid
        """
        try:
            logger.info(f'Updating bill group with ID: {bill_group_id}')
            use_case = BillGroupUpdateUseCase(self._bill_group_repository)
            result = use_case.execute(bill_group_id, bill_group_data)
            if not result:
                raise ce.NotFound(f'Bill group {bill_group_id} not found', 'BILL_GROUP_NOT_FOUND')
            logger.info(f'Bill group updated successfully: {bill_group_id}')
            return result
        except ce.NotFound:
            raise
        except ValueError as ex:
            logger.warning(f'Failed to update bill group {bill_group_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_BILL_GROUP_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating bill group {bill_group_id}: {ex}')
            raise se.InternalServerError()

    def delete_bill_group(self, bill_group_id: UUID) -> None:
        """
        Delete a bill group.

        Args:
            bill_group_id: UUID of the bill group to delete

        Raises:
            NotFound: If bill group is not found
            BadRequest: If bill group has pending bills
        """
        try:
            logger.info(f'Deleting bill group with ID: {bill_group_id}')
            use_case = BillGroupDeleteUseCase(self._bill_group_repository)
            use_case.execute(bill_group_id)
            logger.info(f'Bill group deleted successfully: {bill_group_id}')
        except ValueError as ex:
            error_message = str(ex)
            if 'not found' in error_message.lower():
                logger.warning(f'Bill group not found: {bill_group_id}')
                raise ce.NotFound(error_message, 'BILL_GROUP_NOT_FOUND')
            logger.warning(f'Failed to delete bill group {bill_group_id}: {ex}')
            raise ce.BadRequest(error_message, 'DELETE_BILL_GROUP_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error deleting bill group {bill_group_id}: {ex}')
            raise se.InternalServerError()

    def get_paginated_bill_groups(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[BillGroupResponseDTO]:
        """
        Retrieve a paginated list of bill groups.

        Args:
            filter: Dictionary with filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            PaginatedResponse containing bill groups and pagination metadata
        """
        try:
            logger.info(f'Retrieving paginated bill groups with limit={limit}, offset={offset}')
            use_case = BillGroupGetPaginatedUseCase(self._bill_group_repository)
            result = use_case.execute(filter, limit, offset)
            logger.info(f'Retrieved {len(result.items)} bill groups')
            return result
        except ValueError as ex:
            logger.warning(f'Invalid pagination parameters: {ex}')
            raise ce.BadRequest(str(ex), 'PAGINATION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving paginated bill groups: {ex}')
            raise se.InternalServerError()

    def get_bill_group_summary(self, bill_group_id: UUID) -> BillGroupSummaryDTO:
        """
        Retrieve a summary of a bill group.

        Args:
            bill_group_id: UUID of the bill group

        Returns:
            BillGroupSummaryDTO with summary information

        Raises:
            NotFound: If bill group is not found
        """
        try:
            logger.info(f'Retrieving bill group summary for ID: {bill_group_id}')
            use_case = BillGroupGetSummaryUseCase(self._bill_group_repository)
            result = use_case.execute(bill_group_id)
            if not result:
                raise ce.NotFound(f'Bill group {bill_group_id} not found', 'BILL_GROUP_NOT_FOUND')
            logger.info(f'Bill group summary retrieved successfully: {bill_group_id}')
            return result
        except ce.NotFound:
            raise
        except Exception as ex:
            logger.error(f'Unexpected error retrieving bill group summary {bill_group_id}: {ex}')
            raise se.InternalServerError()
