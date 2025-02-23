from .base_repository import BaseRepository
from app.database.models import ExpenseCategoryModel


class ExpenseCategoryRepository(BaseRepository[ExpenseCategoryModel]):

    def __init__(self) -> None:
        super().__init__()
        self.model = ExpenseCategoryModel

    def _get_filter_params(self, params=...) -> dict:
        user_id = params.get('user_id')
        filter_params = {}
        if user_id is not None:
            filter_params['user_id'] = user_id

        return filter_params
