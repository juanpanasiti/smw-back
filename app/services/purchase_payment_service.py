from app.database.models.purchase_payment_model import PurchasePaymentModel
from app.repositories.purchase_payment_repository import PurchasePaymentRepository
from app.schemas.purchase_payment_schemas import PurchasePaymentRequest
from app.schemas.purchase_payment_schemas import PurchasePaymentResponse
from .base_service import BaseService


class PurchasePaymentService(BaseService[PurchasePaymentModel, PurchasePaymentRequest, PurchasePaymentResponse, PurchasePaymentRepository]):
    def __init__(self):
        super().__init__(PurchasePaymentRepository)

    def _to_model(self, schema: PurchasePaymentRequest) -> PurchasePaymentModel:
        return super()._to_model(schema)
    
    def _to_schema(self, model: PurchasePaymentModel) -> PurchasePaymentResponse:
        return super()._to_schema(model)