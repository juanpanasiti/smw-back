from .base_repository import BaseRepository
from app.database.models.expense_model import ExpenseModel


class ExpenseRepository(BaseRepository[ExpenseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ExpenseModel
