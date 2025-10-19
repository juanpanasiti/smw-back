import logging

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import CreditCardModel
from src.domain.account import CreditCardFactory, CreditCard as CreditCardEntity
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class CreditCardRepositorySQL(BaseRepositorySQL[CreditCardModel, CreditCardEntity]):
    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['owner_id', 'alias']
        return {k: v for k, v in params.items() if k in allowed}

    def _parse_model_to_entity(self, data: CreditCardModel) -> CreditCardEntity:
        # domain factory expects a list of Expense instances; when loading from DB we can provide an empty list
        expenses = []
        return CreditCardFactory.create(
            id=data.account_id,
            owner_id=data.owner_id,
            alias=data.alias,
            limit=Amount(data.limit),
            is_enabled=data.is_enabled,
            main_credit_card_id=data.main_credit_card_id,
            next_closing_date=data.next_closing_date,
            next_expiring_date=data.next_expiring_date,
            financing_limit=Amount(data.financing_limit),
            expenses=expenses,
        )

    def _parse_entity_to_model(self, entity: CreditCardEntity):
        # expects entity to have simple attributes; expenses will be stored as relations elsewhere
        return CreditCardModel(
            id=entity.id,
            account_id=entity.id,
            owner_id=entity.owner_id,
            alias=entity.alias,
            limit=entity.limit.value if hasattr(entity.limit, 'value') else entity.limit,
            is_enabled=entity.is_enabled,
            main_credit_card_id=entity.main_credit_card_id,
            next_closing_date=entity.next_closing_date,
            next_expiring_date=entity.next_expiring_date,
            financing_limit=entity.financing_limit.value if hasattr(entity.financing_limit, 'value') else entity.financing_limit,
        )
