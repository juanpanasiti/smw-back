from .base_repository_v1 import BaseRepositoryV1
from app.database.models.user_model import UserModel
from app.exceptions.repo_exceptions import MatchPasswordException


class UserRepositoryV1(BaseRepositoryV1[UserModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = UserModel

    def check_password(self, user:UserModel, password:str) -> None:
        if not user.check_password(password):
            raise MatchPasswordException()
