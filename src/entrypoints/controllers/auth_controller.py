"""
AuthController: Handles authentication-related HTTP requests.

This controller acts as the entry point for authentication operations,
delegating business logic to the application layer use cases.
"""
import logging

from src.application.dtos import LoginUserDTO, RegisterUserDTO, LoggedInUserDTO
from src.application.use_cases.auth import (
    UserLoginUseCase,
    UserRegisterUseCase,
    UserRenewTokenUseCase,
)
from src.application.ports import UserRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se


logger = logging.getLogger(__name__)


class AuthController:
    """
    Controller for authentication operations.
    
    Handles login, registration, and token renewal by coordinating
    between the presentation layer and application use cases.
    """

    def __init__(self, user_repository: UserRepository):
        """Initialize the controller with repository dependencies.

        Repository dependency is mandatory and must be provided via DI.
        """
        self._user_repository: UserRepository = user_repository

    def login(self, credentials: LoginUserDTO) -> LoggedInUserDTO:
        """
        Authenticate a user with username and password.

        Args:
            credentials: LoginUserDTO containing username and password

        Returns:
            LoggedInUserDTO with user information and access token

        Raises:
            ValueError: If credentials are invalid
        """
        try:
            logger.info(f'Login attempt for user: {credentials.username}')
            use_case = UserLoginUseCase(self._user_repository)
            result = use_case.execute(credentials)
            logger.info(f'User {credentials.username} logged in successfully')
            return result
        except ValueError as ex:
            logger.warning(f'Failed login attempt for user {credentials.username}: {ex}')
            raise ce.Unauthorized(str(ex), 'LOGIN_INVALID_CREDENTIALS')
        except Exception as ex:
            logger.error(f'Unexpected error during login for user {credentials.username}: {ex}')
            raise se.InternalServerError()

    def register(self, user_data: RegisterUserDTO) -> LoggedInUserDTO:
        """
        Register a new user in the system.

        Args:
            user_data: RegisterUserDTO containing user registration information

        Returns:
            LoggedInUserDTO with created user information and access token

        Raises:
            ValueError: If user data is invalid or user already exists
        """
        try:
            logger.info(f'Registration attempt for user: {user_data.username}')
            use_case = UserRegisterUseCase(self._user_repository)
            result = use_case.execute(user_data)
            logger.info(f'User {user_data.username} registered successfully')
            return result
        except ValueError as ex:
            logger.warning(f'Failed registration for user {user_data.username}: {ex}')
            raise ce.BadRequest(str(ex), 'REGISTER_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error during registration for user {user_data.username}: {ex}')
            raise se.InternalServerError()

    def renew_token(self, current_user: LoggedInUserDTO) -> LoggedInUserDTO:
        """
        Renew the access token for an authenticated user.

        Args:
            current_user: LoggedInUserDTO with current user information

        Returns:
            LoggedInUserDTO with refreshed access token

        Raises:
            ValueError: If user is not found
        """
        try:
            logger.info(f'Token renewal for user ID: {current_user.id}')
            use_case = UserRenewTokenUseCase(self._user_repository)
            result = use_case.execute(current_user)
            logger.info(f'Token renewed successfully for user ID: {current_user.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed token renewal for user ID {current_user.id}: {ex}')
            # Map common errors to NotFound; adjust mapping if business rules change
            raise ce.NotFound(str(ex), 'USER_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error during token renewal for user ID {current_user.id}: {ex}')
            raise se.InternalServerError()
