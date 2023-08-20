from .base_repository import BaseRepository
from app.database.models.payment_model import PaymentModel


class PaymentRepository(BaseRepository[PaymentModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PaymentModel
