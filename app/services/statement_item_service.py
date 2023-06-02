from app.database.models.statement_item_model import StatementItemModel
from app.repositories.statement_item_repository import StatementItemRepository
from app.schemas.statement_item_schemas import StatementItemRequest
from app.schemas.statement_item_schemas import StatementItemResponse
from .base_service import BaseService


class StatementItemService(BaseService[StatementItemModel, StatementItemRequest, StatementItemResponse, StatementItemRepository]):
    def __init__(self):
        super().__init__(StatementItemRepository)

    def _to_model(self, schema: StatementItemRequest) -> StatementItemModel:
        return super()._to_model(schema)
    
    def _to_schema(self, model: StatementItemModel) -> StatementItemResponse:
        return super()._to_schema(model)