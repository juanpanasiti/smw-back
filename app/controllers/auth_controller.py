import logging

from app.schemas.auth_schemas import LoginUser, RegisterUser, TokenResponse
from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import server_exceptions as se
from app.services.user_service_old import UserServiceOld
from app.services.auth_service import AuthService


logger = logging.getLogger(__name__)


class AuthController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__auth_service = None

    @property
    def user_service(self) -> UserServiceOld:
        if self.__user_service is None:
            self.__user_service = UserServiceOld()
        return self.__user_service

    @property
    def auth_service(self) -> AuthService:
        if self.__auth_service is None:
            self.__auth_service = AuthService()
        return self.__auth_service

    def register(self, new_user: RegisterUser) -> TokenResponse:
        try:
            logger.debug(f'Try to register new user {new_user.username}')
            return self.auth_service.register(new_user)
        except BaseHTTPException as ex:
            logger.error(f'Error registering new user {new_user.username}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.critical(f'Critical error registering new user {new_user.username}: {ex.args}')
            raise se.InternalServerError(ex.args, 'REGISTER_UNHANDLED_ERROR')
        
    def login(self, credentials: LoginUser)-> TokenResponse:
        try:
            return self.auth_service.login(credentials)
        except BaseHTTPException as ex:
            logger.error(f'Error logging in user {credentials.username}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.critical(f'Critical error logging in user {credentials.username}: {ex.args}')
            raise se.InternalServerError(ex.args, 'LOGIN_UNHANDLED_ERROR')
        
    def get_user_info(self, user_id: int)-> TokenResponse:
        try:
            user = self.user_service.get_by_id(user_id)
            return self.auth_service.get_token(user)
        except BaseHTTPException as ex:
            logger.error(f'Error getting user info {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.critical(f'Critical error getting user info {user_id}: {ex.args}')
            raise se.InternalServerError(ex.args, 'GET_USER_INFO_UNHANDLED_ERROR')
