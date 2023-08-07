import logging

from app.schemas.user_schemas import UserRes
from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import server_exceptions as se
from app.exceptions import client_exceptions as ce
from app.services.user_service import UserService
from app.schemas.auth_schemas import DecodedJWT
from app.core.enums.role_enum import ADMIN_ROLES


logger = logging.getLogger(__name__)


class UserController():
    def __init__(self) -> None:
        self.__user_service = None

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    def get_info(self, token: DecodedJWT, user_id: int) -> UserRes:
        try:
            if token.user_id != user_id and token.role not in ADMIN_ROLES:
                raise ce.Forbidden('You have no permission to get this info.')

            return self.user_service.get_by_id(user_id)

        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)
