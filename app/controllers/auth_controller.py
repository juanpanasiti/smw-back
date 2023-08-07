import logging

# from app.core.jwt
from app.schemas.user_schemas import UserRes
from app.schemas.auth_schemas import LoginUser, RegisterUser, TokenResponse
from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.services.user_service import UserService
from app.services.auth_service import AuthService


logger = logging.getLogger(__name__)


class AuthController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__auth_service = None

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def auth_service(self) -> AuthService:
        if self.__auth_service is None:
            self.__auth_service = AuthService()
        return self.__auth_service

    def register(self, new_user: RegisterUser) -> UserRes:
        try:
            logger.debug(f'Try to register new user {new_user.username}')
            return self.user_service.create(new_user)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            raise se.InternalServerError(ex.args)
        
    def login(self, credentials: LoginUser)-> TokenResponse:
        try:
            token = self.auth_service.login(credentials)
            return TokenResponse(access_token=token)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            raise se.InternalServerError(ex.args)
        
    def get_user_info(self, user_id: int)-> UserRes:
        try:
            user = self.user_service.get_by_id(user_id)
            return user
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            raise se.InternalServerError(ex.args)
