import logging

from app.repositories.user_repository_old import UserRepositoryOld
from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.schemas.user_schemas_old import UserRes, NewUserReq
from app.schemas.profile_schemas_old import ProfileReq
from app.repositories.profile_repository_old import ProfileRepositoryOld
from app.exceptions.repo_exceptions import UniqueFieldException

logger = logging.getLogger(__name__)


class UserServiceOld():
    def __init__(self) -> None:
        self.__repo = None
        self.__profile_repo = None

    @property
    def repo(self) -> UserRepositoryOld:
        if self.__repo is None:
            self.__repo = UserRepositoryOld()
        return self.__repo

    @property
    def profile_repo(self) -> ProfileRepositoryOld:
        if self.__profile_repo is None:
            self.__profile_repo = ProfileRepositoryOld()
        return self.__profile_repo

    def create(self, new_user: NewUserReq) -> UserRes:
        try:
            user_registered = self.repo.create(new_user.model_dump())
            profile_req: ProfileReq = self._get_profile_request(new_user, user_registered.id)
            new_profile = self.profile_repo.create(profile_req.model_dump())
            user_registered.profile = new_profile
            return UserRes.model_validate(user_registered)
        except UniqueFieldException:
            logger.warning('Unique field violation for: ' + str(new_user))
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)

    def get_by_id(self, user_id: int) -> UserRes:
        try:
            user_db = self.repo.get_by_id(user_id)
            return UserRes.model_validate(user_db)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message, 'USER_NOT_FOUND')
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def _get_profile_request(self, user_req: NewUserReq, user_id: int) -> ProfileReq:
        return ProfileReq(
            first_name=user_req.first_name,
            last_name=user_req.last_name,
            user_id=user_id,
        )
