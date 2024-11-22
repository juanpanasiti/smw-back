from .base_repository_old import BaseRepositoryOld
from app.database.models.payment_model import PaymentModel


class PaymentRepositoryOld(BaseRepositoryOld[PaymentModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PaymentModel
