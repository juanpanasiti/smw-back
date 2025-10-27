import logging

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import ExpenseCategoryModel
from src.domain.expense import ExpenseCategoryFactory, ExpenseCategory

logger = logging.getLogger(__name__)


class ExpenseCategoryRepositorySQL(BaseRepositorySQL[ExpenseCategoryModel, ExpenseCategory]):

    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['owner_id', 'name']
        return {k: v for k, v in params.items() if k in allowed}

    def _parse_model_to_entity(self, data: ExpenseCategoryModel) -> ExpenseCategory:
        return ExpenseCategoryFactory.create(
            id=data.id,
            owner_id=data.owner_id,
            name=data.name,
            description=data.description,
            is_income=data.is_income,
        )

    def _parse_entity_to_model(self, entity: ExpenseCategory) -> ExpenseCategoryModel:
        return ExpenseCategoryModel(
            id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            description=entity.description,
            is_income=entity.is_income,
        )
