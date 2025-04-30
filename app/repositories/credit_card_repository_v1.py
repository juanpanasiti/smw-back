from .base_repository_v1 import BaseRepositoryV1
from app.database.models.credit_card_model import CreditCardModel


class CreditCardRepositoryV1(BaseRepositoryV1[CreditCardModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardModel
