from .base_repository_old import BaseRepositoryOld
from app.database.models.expense_model import ExpenseModel


class ExpenseRepositoryOld(BaseRepositoryOld[ExpenseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = ExpenseModel
