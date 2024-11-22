from .base_repository_old import BaseRepositoryOld
from app.database.models.credit_card_model import CreditCardModel


class CreditCardRepositoryOld(BaseRepositoryOld[CreditCardModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = CreditCardModel
