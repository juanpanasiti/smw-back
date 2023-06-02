from .base_repository import BaseRepository
from app.database.models.purchase_payment_model import PurchasePaymentModel

class PurchasePaymentRepository(BaseRepository[PurchasePaymentModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PurchasePaymentModel
        