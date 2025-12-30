"""RefreshToken Domain Entity"""
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.shared import EntityBase


@dataclass
class RefreshToken(EntityBase):
    """Refresh Token Entity

    Represents an opaque refresh token used to obtain new access tokens.
    Tokens are stored hashed in the database for security.
    """
    id: UUID
    user_id: UUID
    token_hash: str  # SHA-256 hash of the token
    expires_at: datetime
    revoked: bool = False
    revoked_at: datetime | None = None
    device_info: str | None = None  # User agent or device identifier
    ip_address: str | None = None
    created_at: datetime | None = None

    @property
    def is_expired(self) -> bool:
        """Check if the refresh token is expired"""
        return self.expires_at < datetime.now(timezone.utc)

    @property
    def is_revoked(self) -> bool:
        """Check if the refresh token is revoked"""
        return self.revoked

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
        device_info: str | None = None,
        ip_address: str | None = None,
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

    def to_dict(self, *args, **kwargs) -> dict:
        """Convert the RefreshToken to a dictionary representation"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'token_hash': self.token_hash,
            'expires_at': self.expires_at.isoformat(),
            'revoked': self.revoked,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None,
            'device_info': self.device_info,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
