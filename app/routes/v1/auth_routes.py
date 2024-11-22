import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.auth_controller import AuthController
from app.core.enums.role_enum import ALL_ROLES
from app.dependencies.auth_dependencies import has_permission
from app.exceptions.client_exceptions import BadRequest
from app.schemas.user_schemas_old import UserRes
from app.schemas.auth_schemas import LoginUser, RegisterUser, TokenResponse
from app.schemas.user_schemas_old import UserRes
from app.schemas.auth_schemas import DecodedJWT

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/auth')
controller = AuthController()


@router.post(
    '/register',
    status_code=201,
    responses={
        201: {'description': 'User registered'},
        400: {'description': BadRequest.description},
    }
)
async def register_user(new_user: RegisterUser) -> TokenResponse:
    return controller.register(new_user)


@router.post(
    '/login',
    responses={
    }
)
async def login_user(credentials: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    return controller.login(LoginUser(username=credentials.username, password=credentials.password))


@router.get(
    '/token',
    responses={
        200: {'description': 'Token renewed and user info obtained'},
        401: {'description': 'User not authenticated'},
    }
)
async def renew_token(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
) -> TokenResponse:
    return controller.get_user_info(token.user_id)
