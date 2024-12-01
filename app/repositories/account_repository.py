from .base_repository import BaseRepository
from app.database.models import AccountModel


class AccountRepository(BaseRepository[AccountModel]):

    def _get_filter_params(self, params = ...):
        return {}

    def __init__(self) -> None:
        super().__init__()
        self.model = AccountModel
