import logging

from app.repositories.user_repository import UserRepository
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.schemas.user_schemas import UserRes, NewUserReq

logger = logging.getLogger(__name__)


class UserService():
    def __init__(self) -> None:
        self.__repo = None

    @property
    def repo(self) -> UserRepository:
        if self.__repo is None:
            self.__repo = UserRepository()
        return self.__repo

    def create(self, new_user: NewUserReq) -> UserRes:
        try:
            user_registered = self.repo.create(new_user.model_dump())
            return UserRes.model_validate(user_registered)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)

    def get_by_id(self, user_id: int) -> UserRes:
        try:
            user_db = self.repo.get_by_id(user_id)
            return UserRes.model_validate(user_db)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
