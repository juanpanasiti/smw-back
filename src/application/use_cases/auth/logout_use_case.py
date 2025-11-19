"""Logout Use Case - Revoke a specific refresh token"""
from src.application.helpers import security
from src.application.ports import RefreshTokenRepository
from src.common.exceptions import UnauthorizedError


class LogoutUseCase:
    """Use case to revoke a specific refresh token (logout from one device)"""
    
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository
    
    def execute(self, refresh_token_str: str) -> None:
        """Revoke a specific refresh token
        
        Args:
            refresh_token_str: The refresh token to revoke
            
        Raises:
            UnauthorizedError: If refresh token is invalid
        """
        # Hash the provided refresh token
        token_hash = security.hash_token(refresh_token_str)
        
        # Find the refresh token in database
        refresh_token = self.refresh_token_repository.find_by_token_hash(token_hash)
        
        if not refresh_token:
            raise UnauthorizedError('Invalid refresh token')
        
        # Revoke the token
        refresh_token.revoke()
        
        # Save the updated token
        self.refresh_token_repository.update(refresh_token)
