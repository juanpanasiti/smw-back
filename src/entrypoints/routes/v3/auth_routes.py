from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos import LoginUserDTO, RegisterUserDTO, LoggedInUserDTO, DecodedJWT
from src.domain.auth.enums.role import ALL_ROLES
from src.entrypoints.controllers import AuthController
from src.entrypoints.dependencies.auth_dependencies import has_permission
from src.infrastructure.repositories import UserRepositorySQL
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix='/auth')
controller = AuthController(user_repository=UserRepositorySQL(UserModel))

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
