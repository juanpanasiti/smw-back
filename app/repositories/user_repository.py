from .base_repository import BaseRepository
from app.database.models.user_model import UserModel

class UserRepository(BaseRepository[UserModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = UserModel
