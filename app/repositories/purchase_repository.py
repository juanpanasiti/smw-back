from .base_repository import BaseRepository
from app.database.models.purchase_model import PurchaseModel

class PurchaseRepository(BaseRepository[PurchaseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PurchaseModel
        