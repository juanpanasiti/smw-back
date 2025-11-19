"""Refresh Token Repository Port"""
from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.application.ports.base_repository import BaseRepository
from src.domain.auth import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Port for RefreshToken Repository"""
    
    @abstractmethod
    def find_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Find a refresh token by its hash"""
        pass
    
    @abstractmethod
    def find_active_by_user(self, user_id: UUID) -> list[RefreshToken]:
        """Find all active (non-revoked, non-expired) refresh tokens for a user"""
        pass
    
    @abstractmethod
    def revoke_all_by_user(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user
        
        Returns the number of tokens revoked
        """
        pass
    
    @abstractmethod
    def delete_expired(self) -> int:
        """Delete all expired refresh tokens (cleanup operation)
        
        Returns the number of tokens deleted
        """
        pass
