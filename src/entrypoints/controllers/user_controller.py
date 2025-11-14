"""
UserController: Handles user-related HTTP requests.

This controller provides endpoints for users to view and update their own
information, including profile and preferences.
"""
import logging
from uuid import UUID

from src.application.dtos import UpdateUserDTO, UserResponseDTO
from src.application.use_cases.user import UserGetOneUseCase, UserUpdateUseCase
from src.application.ports.user_repository import UserRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se

logger = logging.getLogger(__name__)


class UserController:
    """Controller for user operations."""

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the controller.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def get_user(self, user_id: UUID) -> UserResponseDTO:
        """
        Get a user by ID.

        Args:
            user_id: The unique identifier of the user

        Returns:
            UserResponseDTO with user, profile, and preferences data

        Raises:
            NotFound: If user is not found
            InternalServerError: For unexpected errors
        """
        try:
            use_case = UserGetOneUseCase(self.user_repository)
            return use_case.execute(user_id)
        except ValueError as e:
            logger.warning(f'User not found: {e}')
            raise ce.NotFound(str(e))
        except Exception as e:
            logger.error(f'Error getting user: {e}', exc_info=True)
            raise se.InternalServerError('An error occurred while retrieving the user')

    def update_user(self, user_id: UUID, update_data: UpdateUserDTO) -> UserResponseDTO:
        """
        Update a user's information.

        Args:
            user_id: The unique identifier of the user
            update_data: DTO containing the fields to update

        Returns:
            UserResponseDTO with updated user data

        Raises:
            NotFound: If user is not found
            BadRequest: For validation errors
            InternalServerError: For unexpected errors
        """
        try:
            use_case = UserUpdateUseCase(self.user_repository)
            return use_case.execute(user_id, update_data)
        except ValueError as e:
            logger.warning(f'Error updating user: {e}')
            if 'not found' in str(e).lower():
                raise ce.NotFound(str(e))
            raise ce.BadRequest(str(e))
        except Exception as e:
            logger.error(f'Error updating user: {e}', exc_info=True)
            raise se.InternalServerError('An error occurred while updating the user')
