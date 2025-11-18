"""RefreshToken Domain Entity"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class RefreshToken:
    """Refresh Token Entity
    
    Represents an opaque refresh token used to obtain new access tokens.
    Tokens are stored hashed in the database for security.
    """
    id: UUID
    user_id: UUID
    token_hash: str  # SHA-256 hash of the token
    expires_at: datetime
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    device_info: Optional[str] = None  # User agent or device identifier
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @property
    def is_valid(self) -> bool:
        """Check if the refresh token is valid"""
        if self.revoked:
            return False
        if self.expires_at < datetime.now(timezone.utc):
            return False
        return True
    
    def revoke(self) -> None:
        """Revoke this refresh token"""
        self.revoked = True
        self.revoked_at = datetime.now(timezone.utc)
    
    @staticmethod
    def create(
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> 'RefreshToken':
        """Factory method to create a new RefreshToken"""
        return RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            created_at=datetime.now(timezone.utc),
        )
