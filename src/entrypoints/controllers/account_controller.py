"""
AccountController: Handles credit card-related HTTP requests.

This controller acts as the entry point for credit card operations,
delegating business logic to the application layer use cases.
"""
import logging
from uuid import UUID

from src.application.dtos import (
    CreateCreditCardDTO,
    UpdateCreditCardDTO,
    CreditCardResponseDTO,
    PaginatedResponse,
)
from src.application.use_cases.account import (
    CreditCardCreateUseCase,
    CreditCardGetOneUseCase,
    CreditCardUpdateUseCase,
    CreditCardGetPaginatedUseCase,
    CreditCardDeleteUseCase,
)
from src.application.ports import CreditCardRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se
from src.common.exceptions import RepoNotFoundError


logger = logging.getLogger(__name__)


class AccountController:
    """
    Controller for credit card operations.
    
    Handles CRUD operations for credit cards by coordinating
    between the presentation layer and application use cases.
    """

    def __init__(self, credit_card_repository: CreditCardRepository):
        """Initialize the controller with repository dependencies.

        Repository dependency is mandatory and must be provided via DI.
        """
        self._credit_card_repository: CreditCardRepository = credit_card_repository

    def create_credit_card(self, credit_card_data: CreateCreditCardDTO) -> CreditCardResponseDTO:
        """
        Create a new credit card.

        Args:
            credit_card_data: CreateCreditCardDTO containing credit card information

        Returns:
            CreditCardResponseDTO with created credit card information

        Raises:
            ValueError: If credit card data is invalid
        """
        try:
            logger.info(f'Creating credit card with alias: {credit_card_data.alias}')
            use_case = CreditCardCreateUseCase(self._credit_card_repository)
            result = use_case.execute(credit_card_data)
            logger.info(f'Credit card created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create credit card: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_CREDIT_CARD_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating credit card: {ex}')
            raise se.InternalServerError()

    def get_credit_card(self, credit_card_id: UUID) -> CreditCardResponseDTO:
        """
        Retrieve a credit card by its ID.

        Args:
            credit_card_id: UUID of the credit card to retrieve

        Returns:
            CreditCardResponseDTO with credit card information

        Raises:
            RepoNotFoundError: If credit card is not found
        """
        try:
            logger.info(f'Retrieving credit card with ID: {credit_card_id}')
            use_case = CreditCardGetOneUseCase(self._credit_card_repository)
            result = use_case.execute(credit_card_id)
            logger.info(f'Credit card retrieved successfully: {credit_card_id}')
            return result
        
        except RepoNotFoundError as ex:
            logger.warning(f'Credit card not found: {credit_card_id}')
            raise ce.NotFound(str(ex), 'CREDIT_CARD_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving credit card {credit_card_id}: {ex}')
            raise se.InternalServerError()

    def update_credit_card(self, credit_card_id: UUID, credit_card_data: UpdateCreditCardDTO) -> CreditCardResponseDTO:
        """
        Update an existing credit card.

        Args:
            credit_card_id: UUID of the credit card to update
            credit_card_data: UpdateCreditCardDTO containing updated information

        Returns:
            CreditCardResponseDTO with updated credit card information

        Raises:
            ValueError: If credit card is not found or data is invalid
        """
        try:
            logger.info(f'Updating credit card with ID: {credit_card_id}')
            use_case = CreditCardUpdateUseCase(self._credit_card_repository)
            result = use_case.execute(credit_card_id, credit_card_data)
            logger.info(f'Credit card updated successfully: {credit_card_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to update credit card {credit_card_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_CREDIT_CARD_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating credit card {credit_card_id}: {ex}')
            raise se.InternalServerError()

    def delete_credit_card(self, credit_card_id: UUID) -> None:
        """
        Delete a credit card.

        Args:
            credit_card_id: UUID of the credit card to delete

        Raises:
            ValueError: If credit card is not found
        """
        try:
            logger.info(f'Deleting credit card with ID: {credit_card_id}')
            use_case = CreditCardDeleteUseCase(self._credit_card_repository)
            use_case.execute(credit_card_id)
            logger.info(f'Credit card deleted successfully: {credit_card_id}')
        except ValueError as ex:
            logger.warning(f'Failed to delete credit card {credit_card_id}: {ex}')
            raise ce.NotFound(str(ex), 'CREDIT_CARD_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error deleting credit card {credit_card_id}: {ex}')
            raise se.InternalServerError()

    def get_paginated_credit_cards(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[CreditCardResponseDTO]:
        """
        Retrieve a paginated list of credit cards.

        Args:
            filter: Dictionary with filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            PaginatedResponse containing credit cards and pagination metadata

        Raises:
            ValueError: If filter parameters are invalid
        """
        try:
            logger.info(f'Retrieving paginated credit cards with limit={limit}, offset={offset}')
            use_case = CreditCardGetPaginatedUseCase(self._credit_card_repository)
            result = use_case.execute(filter, limit, offset)
            logger.info(f'Retrieved {len(result.items)} credit cards')
            return result
        except ValueError as ex:
            logger.warning(f'Invalid pagination parameters: {ex}')
            raise ce.BadRequest(str(ex), 'PAGINATION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving paginated credit cards: {ex}')
            raise se.InternalServerError()
