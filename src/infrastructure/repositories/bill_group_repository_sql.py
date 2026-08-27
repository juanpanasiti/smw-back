import logging

from sqlalchemy.orm import Query

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import BillGroupModel, AccountModel
from src.application.ports import BillGroupRepository
from src.domain.account import BillGroupFactory, BillGroup as BillGroupEntity
from src.domain.expense import BillFactory, PaymentFactory, BillFrequency
from src.domain.expense.enums import PaymentStatus, ExpenseType
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class BillGroupRepositorySQL(BaseRepositorySQL[BillGroupModel, BillGroupEntity], BillGroupRepository):
    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['owner_id', 'alias', 'is_enabled']
        return {k: v for k, v in params.items() if k in allowed}

    def _parse_model_to_entity(self, data: BillGroupModel) -> BillGroupEntity:
        """Convert BillGroupModel to BillGroup domain entity with all expenses."""
        expenses = []
        
        for expense_model in data.expenses:
            # Only load Bill expenses (not Purchase or Subscription)
            if expense_model.expense_type != ExpenseType.BILL.value:
                continue
            
            # Load payments for this bill
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
            
            # Convert expense model to Bill domain entity
            bill = BillFactory.create(
                id=expense_model.id,
                account_id=expense_model.account_id,
                description=expense_model.title,  # title maps to description
                amount=Amount(expense_model.amount),
                date=expense_model.acquired_at,  # acquired_at maps to date
                frequency=BillFrequency(expense_model.frequency) if expense_model.frequency else BillFrequency.MONTHLY,
                next_bill_month=expense_model.next_bill_month,
                next_bill_year=expense_model.next_bill_year,
                notes=expense_model.notes or '',
                payments=payments,
            )
            expenses.append(bill)
        
        return BillGroupFactory.create(
            id=data.id,  # Use inherited id from AccountModel
            owner_id=data.owner_id,
            alias=data.alias,
            is_enabled=data.is_enabled,
            expenses=expenses,
        )

    def _parse_entity_to_model(self, entity: BillGroupEntity) -> BillGroupModel:
        """Convert BillGroup domain entity to BillGroupModel."""
        return BillGroupModel(
            id=entity.id,
            account_id=entity.id,
            owner_id=entity.owner_id,
            alias=entity.alias,
            limit=0.0,  # BillGroups don't have limits
            is_enabled=entity.is_enabled,
        )

    def delete_by_filter(self, filter: dict) -> None:
        """
        Override delete to properly handle joined table inheritance.
        
        Deletes the Account record, which cascades to BillGroup due to FK constraint.
        """
        try:
            with self.session_factory() as session:
                # First, get the bill group to find its account_id
                bg_query: Query = session.query(BillGroupModel)
                bg_query = bg_query.filter_by(**filter)
                bill_group: BillGroupModel | None = bg_query.first()
                
                if not bill_group:
                    raise ValueError(f'No bill group found matching filter {filter}')
                
                # Delete the Account record (cascades to BillGroup via FK)
                account_query: Query = session.query(AccountModel)
                account_query = account_query.filter_by(id=bill_group.account_id)
                deleted_count: int = account_query.delete()
                
                if deleted_count == 0:
                    raise ValueError(f'No account found for bill group with filter {filter}')
                
                session.commit()
                logger.info(f'Successfully deleted bill group and its account with filter {filter}')
        except Exception as ex:
            logger.error(f'Error deleting bill group: {ex.args}')
            raise ex
