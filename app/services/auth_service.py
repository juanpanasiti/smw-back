import logging

from app.core.jwt import jwt_manager
from app.core.enums.user_status_enum import UserStatusEnum
from app.repositories.user_repository_v1 import UserRepositoryV1
from app.schemas.auth_schemas import LoginUser, TokenResponse, RegisterUser
from app.schemas.user_schemas_v1 import UserResV1
from app.exceptions.repo_exceptions import NotFoundError, MatchPasswordException
from app.exceptions.client_exceptions import Unauthorized
from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions.server_exceptions import InternalServerError
from app.services.user_service_v1 import UserServiceV1

logger = logging.getLogger(__name__)


class AuthService():
    def __init__(self) -> None:
        self.__user_service = None
        self.__user_repo = None

    @property
    def user_service(self) -> UserServiceV1:
        if self.__user_service is None:
            self.__user_service = UserServiceV1()
        return self.__user_service

    @property
    def user_repo(self) -> UserRepositoryV1:
        if self.__user_repo is None:
            self.__user_repo = UserRepositoryV1()
        return self.__user_repo

    def register(self, new_user: RegisterUser) -> TokenResponse:
        try:
            user = self.user_service.create(new_user)
            return self.get_token(user)
        except BaseHTTPException as ex:
            logger.warning(ex.description)
            raise ex
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError('Error on register', 'REGISTER_UNHANDLED_ERROR')

    def login(self, credentials: LoginUser) -> TokenResponse:
        try:
            user = self.user_repo.get_one({'username': credentials.username})
            if user.status == UserStatusEnum.BANNED:
                raise Unauthorized(f'User {user.username} is banned.', 'LOGIN_USER_BANNED')
            self.user_repo.check_password(user, credentials.password)
            response = TokenResponse.model_validate(user)
            response.access_token = self.__get_user_token(user.id, user.role)
            return response
        except NotFoundError:
            logger.warning(f'User "{credentials.username}" not found')
            raise Unauthorized('Error on username/password', 'USER_OR_PASS_ERROR')
        except MatchPasswordException:
            logger.warning(f'User "{credentials.username}" wrong password')
            raise Unauthorized('Error on username/password', 'USER_OR_PASS_ERROR')
        except BaseHTTPException as ex:
            logger.warning(ex.description)
            raise ex
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError('Error on login', 'LOGIN_UNHANDLED_ERROR')

    def get_token(self, user: UserResV1) -> TokenResponse:
        token = self.__get_user_token(user.id, user.role)
        return TokenResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            profile=user.profile,
            created_at=user.created_at,
            updated_at=user.updated_at,
            access_token=token,
        )

    def __get_user_token(self, user_id, user_role) -> str:
        payload = {
            'user_id': str(user_id),
            'role': user_role,
        }
        return jwt_manager.encode(payload)
