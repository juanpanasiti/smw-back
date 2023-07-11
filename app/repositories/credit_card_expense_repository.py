from .base_repository import BaseRepository
from app.database.models.credit_card_expense_model import CreditCardExpenseModel


class CreditCardExpenseRepository(BaseRepository[CreditCardExpenseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardExpenseModel
