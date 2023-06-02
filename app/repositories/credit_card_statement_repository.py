from .base_repository import BaseRepository
from app.database.models.credit_card_statement_model import CreditCardStatementModel

class CreditCardStatementRepository(BaseRepository[CreditCardStatementModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardStatementModel
        