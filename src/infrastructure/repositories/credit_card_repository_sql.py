import logging

from sqlalchemy.orm import Query

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import CreditCardModel, AccountModel
from src.application.ports import CreditCardRepository
from src.domain.account import CreditCardFactory, CreditCard as CreditCardEntity
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class CreditCardRepositorySQL(BaseRepositorySQL[CreditCardModel, CreditCardEntity], CreditCardRepository):
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

    def delete_by_filter(self, filter: dict) -> None:
        """
        Override delete to properly handle joined table inheritance.
        
        Deletes the Account record, which cascades to CreditCard due to FK constraint.
        """
        try:
            with self.session_factory() as session:
                # First, get the credit card to find its account_id
                cc_query: Query = session.query(CreditCardModel)
                cc_query = cc_query.filter_by(**filter)
                credit_card: CreditCardModel | None = cc_query.first()
                
                if not credit_card:
                    raise ValueError(f'No credit card found matching filter {filter}')
                
                # Delete the Account record (cascades to CreditCard via FK)
                account_query: Query = session.query(AccountModel)
                account_query = account_query.filter_by(id=credit_card.account_id)
                deleted_count: int = account_query.delete()
                
                if deleted_count == 0:
                    raise ValueError(f'No account found for credit card with filter {filter}')
                
                session.commit()
                logger.info(f'Successfully deleted credit card and its account with filter {filter}')
        except Exception as ex:
            logger.error(f'Error deleting credit card: {ex.args}')
            raise ex
