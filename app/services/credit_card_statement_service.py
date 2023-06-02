from app.database.models.credit_card_statement_model import CreditCardStatementModel as CCStatementModel
from app.repositories.credit_card_statement_repository import CreditCardStatementRepository as CCStatementRepo
from app.schemas.credit_card_statement_schemas import CreditCardStatementRequest as CCStatementRequest
from app.schemas.credit_card_statement_schemas import CreditCardStatementResponse as CCStatementResponse
from .base_service import BaseService


class CreditCardStatementService(BaseService[CCStatementModel, CCStatementRequest, CCStatementResponse, CCStatementRepo]):
    def __init__(self):
        super().__init__(CCStatementRepo)

    def _to_model(self, schema: CCStatementRequest) -> CCStatementModel:
        return super()._to_model(schema)
    
    def _to_schema(self, model: CCStatementModel) -> CCStatementResponse:
        return super()._to_schema(model)