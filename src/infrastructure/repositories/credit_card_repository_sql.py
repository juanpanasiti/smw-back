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
        # Load expenses from the model and convert to domain entities
        from src.domain.expense import PurchaseFactory, SubscriptionFactory, PaymentFactory
        from src.domain.expense.enums import ExpenseType, PaymentStatus, ExpenseStatus
        
        expenses = []
        for expense_model in data.expenses:
            # Load payments for this expense
            payments = []
            for payment_model in expense_model.payments:
                payment = PaymentFactory.create(
                    id=payment_model.id,
                    expense_id=payment_model.expense_id,
                    amount=Amount(payment_model.amount),
                    no_installment=payment_model.no_installment,
                    status=PaymentStatus(payment_model.status),
                    payment_date=payment_model.payment_date,
                    is_last_payment=payment_model.is_last_payment,
                )
                payments.append(payment)
            # Convert expense model to domain entity using appropriate factory
            if expense_model.expense_type == ExpenseType.PURCHASE.value:
                expense = PurchaseFactory.create(
                    id=expense_model.id,
                    account_id=expense_model.account_id,
                    title=expense_model.title,
                    cc_name=expense_model.cc_name,
                    acquired_at=expense_model.acquired_at,
                    amount=Amount(expense_model.amount),
                    installments=expense_model.installments,
                    first_payment_date=expense_model.first_payment_date,
                    status=ExpenseStatus(expense_model.status),
                    category_id=expense_model.category_id,
                    payments=payments,  # Use real payments from database
                )
            elif expense_model.expense_type == ExpenseType.SUBSCRIPTION.value:
                expense = SubscriptionFactory.create(
                    id=expense_model.id,
                    account_id=expense_model.account_id,
                    title=expense_model.title,
                    cc_name=expense_model.cc_name,
                    acquired_at=expense_model.acquired_at,
                    amount=Amount(expense_model.amount),
                    installments=expense_model.installments,
                    first_payment_date=expense_model.first_payment_date,
                    status=ExpenseStatus(expense_model.status),
                    category_id=expense_model.category_id,
                    payments=payments,  # Use real payments from database
                )
            else:
                continue
            
            expenses.append(expense)
        
        return CreditCardFactory.create(
            id=data.id,  # Use inherited id from AccountModel
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
