import logging

from app.repositories.user_repository_v1 import UserRepositoryV1
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.schemas.user_schemas_v1 import UserResV1, NewUserReqV1
from app.schemas.profile_schemas_v1 import ProfileReqV1
from app.repositories.profile_repository_v1 import ProfileRepositoryV1
from app.exceptions.repo_exceptions import UniqueFieldException

logger = logging.getLogger(__name__)


class UserServiceV1():
    def __init__(self) -> None:
        self.__repo = None
        self.__profile_repo = None

    @property
    def repo(self) -> UserRepositoryV1:
        if self.__repo is None:
            self.__repo = UserRepositoryV1()
        return self.__repo

    @property
    def profile_repo(self) -> ProfileRepositoryV1:
        if self.__profile_repo is None:
            self.__profile_repo = ProfileRepositoryV1()
        return self.__profile_repo

    def create(self, new_user: NewUserReqV1) -> UserResV1:
        try:
            user_registered = self.repo.create(new_user.model_dump())
            profile_req: ProfileReqV1 = self._get_profile_request(new_user, user_registered.id)
            new_profile = self.profile_repo.create(profile_req.model_dump())
            user_registered.profile = new_profile
            return UserResV1.model_validate(user_registered)
        except UniqueFieldException:
            logger.warning('Unique field violation for: ' + str(new_user))
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)

    def get_by_id(self, user_id: int) -> UserResV1:
        try:
            user_db = self.repo.get_by_id(user_id)
            return UserResV1.model_validate(user_db)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message, 'USER_NOT_FOUND')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def _get_profile_request(self, user_req: NewUserReqV1, user_id: int) -> ProfileReqV1:
        return ProfileReqV1(
            first_name=user_req.first_name,
            last_name=user_req.last_name,
            user_id=user_id,
        )
