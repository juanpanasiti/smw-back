from datetime import datetime, timedelta, timezone
from typing import Optional

from src.application.dtos import LoginUserDTO, LoggedInUserDTO
from src.application.helpers import security
from src.application.ports import UserRepository, RefreshTokenRepository
from src.config import settings
from src.domain.auth import RefreshToken


class UserLoginUseCase:
    def __init__(
        self, 
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    def execute(
        self, 
        user_data: LoginUserDTO, 
        ip_address: Optional[str] = None
    ) -> LoggedInUserDTO:
        # Authenticate user
        filter = {'username': user_data.username}
        user = self.user_repository.get_by_filter(filter)
        if not user or not security.verify_password(user_data.password, user.encrypted_password):
            raise ValueError('Invalid username or password')
        
        # Create access token
        access_token = security.create_access_token(user)
        
        # Generate refresh token
        refresh_token_str = security.generate_refresh_token()
        token_hash = security.hash_token(refresh_token_str)
        
        # Calculate expiration
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Create refresh token entity
        refresh_token_entity = RefreshToken.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=user_data.device_info,
            ip_address=ip_address
        )
        
        # Save refresh token to database
        self.refresh_token_repository.create(refresh_token_entity)
        
        return LoggedInUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            access_token=access_token,
            refresh_token=refresh_token_str  # Return the plain token to the user
        )

