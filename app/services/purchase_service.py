from app.database.models.purchase_model import PurchaseModel
from app.repositories.purchase_repository import PurchaseRepository
from app.schemas.purchase_schemas import PurchaseRequest
from app.schemas.purchase_schemas import PurchaseResponse
from .base_service import BaseService


class PurchaseService(BaseService[PurchaseModel, PurchaseRequest, PurchaseResponse, PurchaseRepository]):
    def __init__(self):
        super().__init__(PurchaseRepository)

    def _to_model(self, schema: PurchaseRequest) -> PurchaseModel:
        return super()._to_model(schema)
    
    def _to_schema(self, model: PurchaseModel) -> PurchaseResponse:
        return super()._to_schema(model)