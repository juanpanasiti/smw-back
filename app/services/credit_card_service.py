from app.database.models.credit_card_model import CreditCardModel
from app.repositories.credit_card_repository import CreditCardRepository
from app.schemas.credit_card_schemas import CreditCardRequest
from app.schemas.credit_card_schemas import CreditCardResponse
from .base_service import BaseService


class CreditCardService(BaseService[CreditCardModel, CreditCardRequest, CreditCardResponse, CreditCardRepository]):
    def __init__(self):
        super().__init__(CreditCardRepository)

    def _to_model(self, schema: CreditCardRequest) -> CreditCardModel:
        return super()._to_model(schema)
    
    def _to_schema(self, model: CreditCardModel) -> CreditCardResponse:
        return super()._to_schema(model)