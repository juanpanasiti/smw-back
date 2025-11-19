from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos import LoginUserDTO, RegisterUserDTO, LoggedInUserDTO, DecodedJWT
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import AuthController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import UserRepositorySQL
from src.infrastructure.repositories.refresh_token_repository_sql import RefreshTokenRepositorySQL
from src.infrastructure.database.models import UserModel
from src.infrastructure.database import db_conn

router = APIRouter(prefix='/auth')
controller = AuthController(
    user_repository=UserRepositorySQL(
        model=UserModel,
        session_factory=db_conn.SessionLocal,
    ),
    refresh_token_repository=RefreshTokenRepositorySQL(
        session_factory=db_conn.SessionLocal
    )
)

@router.post('/oauth')
def login_oauth(credentials: OAuth2PasswordRequestForm = Depends()) -> LoggedInUserDTO:
    data = LoginUserDTO(username=credentials.username, password=credentials.password)
    return controller.login(data)

@router.post('/login')
def login(data: LoginUserDTO) -> LoggedInUserDTO:
    return controller.login(data)


@router.post('/register')
def register(data: RegisterUserDTO) -> LoggedInUserDTO:
    return controller.register(data)


@router.post('/refresh')
def refresh_access_token(authorization: str = Header(...)) -> dict:
    """
    Refresh access token using refresh token.
    
    Send the refresh token in the Authorization header as: Bearer <refresh_token>
    
    Returns:
        New access token and the same refresh token
    """
    # Extract token from "Bearer <token>" format
    if not authorization.startswith('Bearer '):
        raise ValueError('Invalid authorization header format')
    
    refresh_token = authorization.replace('Bearer ', '', 1)
    return controller.refresh_access_token(refresh_token)


@router.post('/renew-token')
def renew_token(token: DecodedJWT = Depends(has_permission(ALL_ROLES))) -> LoggedInUserDTO:
    """Renew authentication token for logged-in user."""
    logged_in_user = LoggedInUserDTO(
        id=token.user_id,
        username='',  # Will be populated by use case from database
        email=token.email,
        role=token.role,
    )
    return controller.renew_token(logged_in_user)
