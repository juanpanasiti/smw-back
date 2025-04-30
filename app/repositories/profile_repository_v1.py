from .base_repository_v1 import BaseRepositoryV1
from app.database.models.profile_model import ProfileModel


class ProfileRepositoryV1(BaseRepositoryV1[ProfileModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ProfileModel
