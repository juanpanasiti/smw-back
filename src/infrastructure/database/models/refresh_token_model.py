"""RefreshToken SQLAlchemy Model"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.base_model import BaseModel


class RefreshTokenModel(BaseModel):
    """Refresh Token Model
    
    Stores hashed refresh tokens for authentication.
    Supports revocation and device tracking.
    """
    __tablename__ = 'refresh_tokens'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256 hash
    expires_at = Column(DateTime, nullable=False, index=True)
    revoked = Column(Boolean, nullable=False, default=False, index=True)
    revoked_at = Column(DateTime, nullable=True)
    device_info = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    
    # Relationship
    user = relationship('UserModel', back_populates='refresh_tokens')
    
    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_user_valid_tokens', 'user_id', 'revoked', 'expires_at'),
    )
    
    def __repr__(self):
        return f'<RefreshTokenModel(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>'
