"""Logout from all devices Use Case"""
from uuid import UUID

from src.application.ports import RefreshTokenRepository


class LogoutAllDevicesUseCase:
    """Use case to revoke all refresh tokens for a user (logout from all devices)"""
    
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository
    
    def execute(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user
        
        Args:
            user_id: The user's ID
            
        Returns:
            Number of tokens revoked
        """
        return self.refresh_token_repository.revoke_all_by_user(user_id)
