from .base_repository_old import BaseRepositoryOld
from app.database.models.profile_model import ProfileModel


class ProfileRepositoryOld(BaseRepositoryOld[ProfileModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ProfileModel
