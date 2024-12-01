from .base_repository import BaseRepository
from app.database.models import ExpenseModel
from app.core.enums import SortableExpenseFieldsEnum


class ExpenseRepository(BaseRepository[ExpenseModel]):
    VALID_ORDER_BY_FIELDS: list[str] = [field.value for field in SortableExpenseFieldsEnum]

    def __init__(self) -> None:
        super().__init__()
        self.model = ExpenseModel

    def _get_filter_params(self, params=...) -> dict:
        user_id = params.get('user_id')
        account_id = params.get('account_id')
        filter_params = {}
        if user_id is not None:
            filter_params['user_id'] = user_id
        if account_id is not None:
            filter_params['account_id'] = account_id
        
        return filter_params
