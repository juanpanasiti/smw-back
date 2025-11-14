"""
User API routes.

Provides endpoints for users to view and update their own information.
"""
from uuid import UUID
from fastapi import APIRouter, Depends

from src.application.dtos import UpdateUserDTO, UserResponseDTO, DecodedJWT
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import UserController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import UserRepositorySQL
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix='/users', tags=['users'])
controller = UserController(user_repository=UserRepositorySQL(UserModel))


@router.get('/{user_id}')
def get_user(
    user_id: UUID,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> UserResponseDTO:
    """
    Get user information by ID.
    
    Returns user data including profile and preferences (password excluded).
    Users can only access their own information.
    """
    # TODO: Add authorization check to ensure user can only access their own data
    # For now, any authenticated user can access any user's data
    return controller.get_user(user_id)


@router.put('/{user_id}')
def update_user(
    user_id: UUID,
    update_data: UpdateUserDTO,
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> UserResponseDTO:
    """
    Update user information.
    
    All fields are optional. Updates user data including profile and preferences.
    Users can only update their own information.
    """
    # TODO: Add authorization check to ensure user can only update their own data
    # For now, any authenticated user can update any user's data
    return controller.update_user(user_id, update_data)
