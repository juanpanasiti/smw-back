"""RefreshToken Repository SQL Implementation"""
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session, sessionmaker

from src.application.ports import RefreshTokenRepository
from src.domain.auth import RefreshToken
from src.infrastructure.database.models import RefreshTokenModel
from src.infrastructure.database import db_conn


class RefreshTokenRepositorySQL(RefreshTokenRepository):
    """SQL implementation of RefreshTokenRepository"""
    
    def __init__(self, session_factory: sessionmaker = db_conn.SessionLocal):
        self.session_factory = session_factory
    
    def create(self, entity: RefreshToken) -> RefreshToken:
        """Create a new refresh token"""
        with self.session_factory() as db:
            model = RefreshTokenModel(
                id=entity.id,
                user_id=entity.user_id,
                token_hash=entity.token_hash,
                expires_at=entity.expires_at,
                revoked=entity.revoked,
                revoked_at=entity.revoked_at,
                device_info=entity.device_info,
                ip_address=entity.ip_address,
            )
            db.add(model)
            db.commit()
            db.refresh(model)
            return self._to_domain(model)
    
    def get_by_id(self, entity_id: UUID) -> Optional[RefreshToken]:
        """Get a refresh token by ID"""
        with self.session_factory() as db:
            model = db.query(RefreshTokenModel).filter(RefreshTokenModel.id == entity_id).first()
            return self._to_domain(model) if model else None
    
    def update(self, entity: RefreshToken) -> RefreshToken:
        """Update a refresh token"""
        with self.session_factory() as db:
            model = db.query(RefreshTokenModel).filter(RefreshTokenModel.id == entity.id).first()
            if not model:
                raise ValueError(f"RefreshToken with id {entity.id} not found")
            
            model.revoked = entity.revoked
            model.revoked_at = entity.revoked_at
            
            db.commit()
            db.refresh(model)
            return self._to_domain(model)
    
    def delete(self, entity_id: UUID) -> None:
        """Delete a refresh token"""
        with self.session_factory() as db:
            model = db.query(RefreshTokenModel).filter(RefreshTokenModel.id == entity_id).first()
            if model:
                db.delete(model)
                db.commit()
    
    def count_by_filter(self, filter: dict) -> int:
        """Count refresh tokens by filter"""
        with self.session_factory() as db:
            return db.query(RefreshTokenModel).filter_by(**filter).count()
    
    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[RefreshToken]:
        """Get multiple refresh tokens by filter with pagination"""
        with self.session_factory() as db:
            models = db.query(RefreshTokenModel).filter_by(**filter).limit(limit).offset(offset).all()
            return [self._to_domain(model) for model in models]
    
    def get_by_filter(self, filter: dict) -> Optional[RefreshToken]:
        """Get a single refresh token by filter"""
        with self.session_factory() as db:
            model = db.query(RefreshTokenModel).filter_by(**filter).first()
            return self._to_domain(model) if model else None
    
    def delete_by_filter(self, filter: dict) -> None:
        """Delete refresh tokens by filter"""
        with self.session_factory() as db:
            db.query(RefreshTokenModel).filter_by(**filter).delete(synchronize_session=False)
            db.commit()
    
    def find_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Find a refresh token by its hash"""
        with self.session_factory() as db:
            model = db.query(RefreshTokenModel).filter(
                RefreshTokenModel.token_hash == token_hash
            ).first()
            return self._to_domain(model) if model else None
    
    def find_active_by_user(self, user_id: UUID) -> list[RefreshToken]:
        """Find all active refresh tokens for a user"""
        with self.session_factory() as db:
            models = db.query(RefreshTokenModel).filter(
                and_(
                    RefreshTokenModel.user_id == user_id,
                    RefreshTokenModel.revoked == False,
                    RefreshTokenModel.expires_at > datetime.now(timezone.utc)
                )
            ).all()
            return [self._to_domain(model) for model in models]
    
    def revoke_all_by_user(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user"""
        with self.session_factory() as db:
            result = db.query(RefreshTokenModel).filter(
                and_(
                    RefreshTokenModel.user_id == user_id,
                    RefreshTokenModel.revoked == False
                )
            ).update({
                'revoked': True,
                'revoked_at': datetime.now(timezone.utc)
            }, synchronize_session=False)
            
            db.commit()
            return result
    
    def delete_expired(self) -> int:
        """Delete all expired refresh tokens"""
        with self.session_factory() as db:
            result = db.query(RefreshTokenModel).filter(
                RefreshTokenModel.expires_at < datetime.now(timezone.utc)
            ).delete(synchronize_session=False)
            
            db.commit()
            return result
    
    def _to_domain(self, model: RefreshTokenModel) -> RefreshToken:
        """Convert model to domain entity"""
        # Ensure datetimes are timezone-aware
        expires_at = model.expires_at
        if expires_at and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        revoked_at = model.revoked_at
        if revoked_at and revoked_at.tzinfo is None:
            revoked_at = revoked_at.replace(tzinfo=timezone.utc)
        
        created_at = model.created_at
        if created_at and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=expires_at,
            revoked=model.revoked,
            revoked_at=revoked_at,
            device_info=model.device_info,
            ip_address=model.ip_address,
            created_at=created_at,
        )
