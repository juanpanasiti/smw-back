"""
UserUpdateUseCase: Updates user information including profile and preferences.

This use case handles updating user data with support for partial updates.
All fields in the update DTO are optional.
"""
import logging
from uuid import UUID
from datetime import date

from src.application.ports.user_repository import UserRepository
from src.application.dtos import UpdateUserDTO, UserResponseDTO, ProfileResponseDTO, PreferencesResponseDTO
from src.application.helpers.security import hash_password
from src.domain.auth import User

logger = logging.getLogger(__name__)


class UserUpdateUseCase:
    """Use case for updating user information."""

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the use case.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def execute(self, user_id: UUID, update_data: UpdateUserDTO) -> UserResponseDTO:
        """
        Update a user's information.

        Args:
            user_id: The unique identifier of the user
            update_data: DTO containing the fields to update

        Returns:
            UserResponseDTO with updated user data

        Raises:
            ValueError: If user is not found or validation fails
        """
        # Fetch existing user
        user: User | None = self.user_repository.get_by_filter({'id': user_id})
        
        if not user:
            raise ValueError(f'User with id {user_id} not found')

        # Update user fields if provided
        if update_data.username is not None:
            user.username = update_data.username

        if update_data.email is not None:
            user.email = update_data.email

        if update_data.password is not None:
            user.encrypted_password = hash_password(update_data.password)

        # Update profile fields if provided
        if update_data.profile:
            if update_data.profile.first_name is not None:
                user.profile.first_name = update_data.profile.first_name

            if update_data.profile.last_name is not None:
                user.profile.last_name = update_data.profile.last_name

            if update_data.profile.birthdate is not None:
                try:
                    user.profile.birthdate = date.fromisoformat(update_data.profile.birthdate)
                except ValueError as e:
                    raise ValueError(f'Invalid birthdate format: {e}')

            # Update preferences if provided
            if update_data.profile.preferences:
                if update_data.profile.preferences.monthly_spending_limit is not None:
                    user.profile.preferences.monthly_spending_limit = update_data.profile.preferences.monthly_spending_limit

        # Save updated user
        updated_user = self.user_repository.update(user)

        # Build response DTOs
        preferences_dto = None
        if updated_user.profile.preferences:
            preferences_dto = PreferencesResponseDTO(
                id=updated_user.profile.preferences.id,
                monthly_spending_limit=updated_user.profile.preferences.monthly_spending_limit,
            )

        profile_dto = ProfileResponseDTO(
            id=updated_user.profile.id,
            first_name=updated_user.profile.first_name,
            last_name=updated_user.profile.last_name,
            birthdate=updated_user.profile.birthdate.isoformat() if updated_user.profile.birthdate else None,
            preferences=preferences_dto,
        )

        return UserResponseDTO(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            role=updated_user.role,
            profile=profile_dto,
        )
