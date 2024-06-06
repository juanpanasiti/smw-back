from .base_repository import BaseRepository
from app.database.models.user_model import UserModel
from app.exceptions.repo_exceptions import MatchPasswordException


class UserRepository(BaseRepository[UserModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = UserModel

    def check_password(self, user:UserModel, password:str) -> None:
        if not user.check_password(password):
            raise MatchPasswordException()
