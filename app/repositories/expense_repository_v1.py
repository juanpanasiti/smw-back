from .base_repository_v1 import BaseRepositoryV1
from app.database.models.expense_model import ExpenseModel


class ExpenseRepositoryV1(BaseRepositoryV1[ExpenseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ExpenseModel
