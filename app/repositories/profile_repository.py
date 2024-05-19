from .base_repository import BaseRepository
from app.database.models.profile_model import ProfileModel


class ProfileRepository(BaseRepository[ProfileModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ProfileModel
