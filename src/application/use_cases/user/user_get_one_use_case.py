"""
UserGetOneUseCase: Retrieves a user by ID with profile and preferences.

This use case handles fetching a single user's information including
their profile and preferences data.
"""
import logging
from uuid import UUID

from src.application.ports.user_repository import UserRepository
from src.application.dtos import UserResponseDTO, ProfileResponseDTO, PreferencesResponseDTO
from src.domain.auth import User

logger = logging.getLogger(__name__)


class UserGetOneUseCase:
    """Use case for retrieving a user by their ID."""

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the use case.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> UserResponseDTO:
        """
        Retrieve a user by ID.

        Args:
            user_id: The unique identifier of the user

        Returns:
            UserResponseDTO with user, profile, and preferences data

        Raises:
            ValueError: If user is not found
        """
        user: User | None = self.user_repository.get_by_filter({'id': user_id})
        
        if not user:
            raise ValueError(f'User with id {user_id} not found')

        # Build preferences DTO
        preferences_dto = None
        if user.profile.preferences:
            preferences_dto = PreferencesResponseDTO(
                id=user.profile.preferences.id,
                monthly_spending_limit=user.profile.preferences.monthly_spending_limit,
            )

        # Build profile DTO
        profile_dto = ProfileResponseDTO(
            id=user.profile.id,
            first_name=user.profile.first_name,
            last_name=user.profile.last_name,
            birthdate=user.profile.birthdate.isoformat() if user.profile.birthdate else None,
            preferences=preferences_dto,
        )

        # Build user response DTO
        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            profile=profile_dto,
        )
