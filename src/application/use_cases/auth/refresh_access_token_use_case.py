"""Refresh Access Token Use Case"""
from typing import Optional

from src.application.dtos import RefreshTokenRequestDTO, RefreshTokenResponseDTO
from src.application.helpers import security
from src.application.ports import UserRepository, RefreshTokenRepository
from src.common.exceptions import UnauthorizedError


class RefreshAccessTokenUseCase:
    """Use case to refresh access token using refresh token"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
    
    def execute(
        self,
        request: RefreshTokenRequestDTO,
        ip_address: Optional[str] = None
    ) -> RefreshTokenResponseDTO:
        """Refresh access token
        
        Args:
            request: Refresh token request with token string
            ip_address: Optional IP address for tracking
            
        Returns:
            New access and refresh tokens
            
        Raises:
            UnauthorizedError: If refresh token is invalid or expired
        """
        # Hash the provided refresh token
        token_hash = security.hash_token(request.refresh_token)
        
        # Find the refresh token in database
        refresh_token = self.refresh_token_repository.find_by_token_hash(token_hash)
        
        if not refresh_token:
            raise UnauthorizedError('Invalid refresh token')
        
        # Validate the refresh token
        if not refresh_token.is_valid:
            raise UnauthorizedError('Refresh token is expired or revoked')
        
        # Get the user
        user = self.user_repository.get_by_filter({'id': refresh_token.user_id})
        if not user:
            raise UnauthorizedError('User not found')
        
        # Create new access token
        access_token = security.create_access_token(user)
        
        # Optionally: Rotate refresh token (create new one and revoke old)
        # For now, we keep the same refresh token
        
        return RefreshTokenResponseDTO(
            access_token=access_token,
            refresh_token=request.refresh_token  # Return same refresh token
        )
