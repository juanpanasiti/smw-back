from .base_repository import BaseRepository
from app.database.models.statement_item_model import StatementItemModel

class PurchasePaymentRepository(BaseRepository[StatementItemModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = StatementItemModel
        