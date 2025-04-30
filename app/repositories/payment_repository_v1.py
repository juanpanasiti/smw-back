from .base_repository_v1 import BaseRepositoryV1
from app.database.models.payment_model import PaymentModel


class PaymentRepositoryV1(BaseRepositoryV1[PaymentModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PaymentModel
