import logging

from app.core.jwt import jwt_manager
from app.core.enums.user_status_enum import UserStatusEnum
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import LoginUser
from app.exceptions.repo_exceptions import NotFoundError
from app.exceptions.client_exceptions import Unauthorized
from app.exceptions.server_exceptions import InternalServerError

logger = logging.getLogger(__name__)


class AuthService():
    def __init__(self) -> None:
        self.__user_repo = None

    @property
    def user_repo(self) -> UserRepository:
        if self.__user_repo is None:
            self.__user_repo = UserRepository()
        return self.__user_repo

    def login(self, credentials: LoginUser) -> str:
        try:
            user = self.user_repo.get_one({'username': credentials.username})
            if user.status == UserStatusEnum.BANNED:
                raise Unauthorized(f'User {user.username} is banned.')
            if not user.check_password(credentials.password):
                raise Unauthorized('Error on username/password')
            payload = {
                'user_id': str(user.id),
                'role': user.role,
            }
            token = jwt_manager.encode(payload)
            return token
        except NotFoundError:
            logger.warn(f'User "{credentials.username}" not found')
            raise Unauthorized('Error on username/password')
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()
