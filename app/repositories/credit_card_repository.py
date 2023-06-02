from .base_repository import BaseRepository
from app.database.models.credit_card_model import CreditCardModel

class CreditCardRepository(BaseRepository[CreditCardModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardModel
        