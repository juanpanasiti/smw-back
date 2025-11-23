import logging
from datetime import date

from sqlalchemy.orm import Query, joinedload

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import ExpenseModel, PaymentModel, AccountModel
from src.domain.expense import (
    PurchaseFactory,
    SubscriptionFactory,
    PaymentFactory,
    PaymentStatus,
    ExpenseType,
    Expense as ExpenseEntity,
)
from src.application.ports import ExpenseRepository
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class ExpenseRepositorySQL(BaseRepositorySQL[ExpenseModel, ExpenseEntity], ExpenseRepository):
    def create(self, entity: ExpenseEntity) -> ExpenseEntity:
        try:
            with self.session_factory() as session:
                expense_model = self._parse_entity_to_model(entity)
                session.add(expense_model)
                session.flush()

                for payment in entity.payments:
                    payment_model = PaymentModel(
                        id=payment.id,
                        expense_id=expense_model.id,
                        amount=payment.amount.value if hasattr(payment.amount, 'value') else payment.amount,
                        no_installment=payment.no_installment,
                        status=payment.status.value if hasattr(payment.status, 'value') else payment.status,
                        payment_date=payment.payment_date,
                        is_last_payment=payment.is_last_payment,
                    )
                    session.add(payment_model)

                session.commit()

                created_expense = (
                    session.query(self.model)
                    .options(joinedload(ExpenseModel.payments))
                    .filter_by(id=expense_model.id)
                    .one()
                )
                return self._parse_model_to_entity(created_expense)
        except Exception as ex:
            logger.error(f'Error creating expense: {ex.args}')
            raise ex

    def update(self, entity: ExpenseEntity) -> ExpenseEntity:
        """
        Override update to also update associated payments.
        This is crucial for rebalancing payments when one is updated.
        """
        try:
            with self.session_factory() as session:
                # Update the expense itself
                expense_model = session.query(self.model).filter_by(id=entity.id).first()
                if not expense_model:
                    raise ValueError(f'Expense with id {entity.id} not found')
                
                # Update expense fields directly from entity attributes
                expense_model.title = entity.title
                expense_model.cc_name = entity.cc_name
                expense_model.acquired_at = entity.acquired_at
                expense_model.amount = entity.amount.value if hasattr(entity.amount, 'value') else entity.amount
                expense_model.expense_type = entity.expense_type.value if hasattr(entity.expense_type, 'value') else entity.expense_type
                expense_model.installments = entity.installments
                expense_model.first_payment_date = entity.first_payment_date
                expense_model.status = entity.status.value if hasattr(entity.status, 'value') else entity.status
                expense_model.account_id = entity.account_id
                expense_model.category_id = entity.category_id
                
                # Flush expense updates before deleting payments to avoid autoflush issues
                session.flush()
                
                # Update payments - delete old ones and create new ones to ensure sync
                session.query(PaymentModel).filter_by(expense_id=entity.id).delete()
                
                for payment in entity.payments:
                    payment_model = PaymentModel(
                        id=payment.id,
                        expense_id=entity.id,
                        amount=payment.amount.value if hasattr(payment.amount, 'value') else payment.amount,
                        no_installment=payment.no_installment,
                        status=payment.status.value if hasattr(payment.status, 'value') else payment.status,
                        payment_date=payment.payment_date,
                        is_last_payment=payment.is_last_payment,
                    )
                    session.add(payment_model)
                
                session.commit()
                
                # Reload with payments
                updated_expense = (
                    session.query(self.model)
                    .options(joinedload(ExpenseModel.payments))
                    .filter_by(id=entity.id)
                    .one()
                )
                return self._parse_model_to_entity(updated_expense)
        except Exception as ex:
            logger.error(f'Error updating expense: {ex.args}')
            raise ex

    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['account_id', 'category_id', 'expense_type', 'status', 'owner_id']
        return {k: v for k, v in params.items() if k in allowed}

    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[ExpenseEntity]:
        """
        Override to handle owner_id filtering which requires a JOIN with Account.
        """
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                
                # Handle owner_id separately with JOIN
                owner_id = filter.get('owner_id')
                if owner_id:
                    query = query.join(AccountModel, ExpenseModel.account_id == AccountModel.id)
                    query = query.filter(AccountModel.owner_id == owner_id)
                
                # Apply other filters
                if filter.get('order_by'):
                    query = query.order_by(self._get_order_by_params(filter))
                
                search_filter = self._get_filter_params(filter)
                # Remove owner_id from search_filter since we already handled it
                search_filter.pop('owner_id', None)
                
                # When we have a JOIN, we need to use filter() with explicit model reference
                # instead of filter_by() to avoid ambiguity
                if search_filter:
                    if owner_id:
                        # Use explicit filter with ExpenseModel when we have a JOIN
                        for key, value in search_filter.items():
                            query = query.filter(getattr(ExpenseModel, key) == value)
                    else:
                        # Use filter_by when there's no JOIN
                        query = query.filter_by(**search_filter)
                
                query = query.limit(limit)
                query = query.offset(offset)
                result_list: list[ExpenseModel] = query.all()
                return [self._parse_model_to_entity(item) for item in result_list]
        except Exception as ex:
            logger.error(f'Error in get_many_by_filter: {ex.args}')
            raise ex

    def count_by_filter(self, filter: dict = {}) -> int:
        """
        Override to handle owner_id filtering which requires a JOIN with Account.
        """
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                
                # Handle owner_id separately with JOIN
                owner_id = filter.get('owner_id')
                if owner_id:
                    query = query.join(AccountModel, ExpenseModel.account_id == AccountModel.id)
                    query = query.filter(AccountModel.owner_id == owner_id)
                
                search_filter = self._get_filter_params(filter)
                # Remove owner_id from search_filter since we already handled it
                search_filter.pop('owner_id', None)
                
                # When we have a JOIN, we need to use filter() with explicit model reference
                # instead of filter_by() to avoid ambiguity
                if search_filter:
                    if owner_id:
                        # Use explicit filter with ExpenseModel when we have a JOIN
                        for key, value in search_filter.items():
                            query = query.filter(getattr(ExpenseModel, key) == value)
                    else:
                        # Use filter_by when there's no JOIN
                        query = query.filter_by(**search_filter)
                
                return query.count()
        except Exception as ex:
            logger.error(f'Error in count_by_filter: {ex.args}')
            raise ex

    def _parse_model_to_entity(self, data: ExpenseModel):
        # choose factory by expense_type
        factory = PurchaseFactory if data.expense_type == ExpenseType.PURCHASE.value else SubscriptionFactory
        payments = [
            PaymentFactory.create(
                id=p.id,
                expense_id=p.expense_id,
                amount=Amount(p.amount),
                no_installment=p.no_installment,
                status=PaymentStatus(p.status) if not isinstance(p.status, PaymentStatus) else p.status,
                payment_date=p.payment_date,
                is_last_payment=p.is_last_payment,
            )
            for p in (data.payments or [])
        ]
        return factory.create(
            id=data.id,
            account_id=data.account_id,
            title=data.title,
            cc_name=data.cc_name,
            acquired_at=data.acquired_at,
            amount=Amount(data.amount),
            installments=data.installments,
            first_payment_date=data.first_payment_date,
            category_id=data.category_id,
            payments=payments,
        )

    def _parse_entity_to_model(self, entity: ExpenseEntity) -> ExpenseModel:
        # minimal mapping; payments handled in PaymentRepository
        return ExpenseModel(
            id=entity.id,
            title=entity.title,
            cc_name=entity.cc_name,
            acquired_at=entity.acquired_at,
            amount=entity.amount.value if hasattr(entity.amount, 'value') else entity.amount,
            expense_type=entity.expense_type.value if hasattr(entity.expense_type, 'value') else entity.expense_type,
            installments=entity.installments,
            first_payment_date=entity.first_payment_date,
            status=entity.status.value if hasattr(entity.status, 'value') else entity.status,
            spent_type=getattr(entity, 'spent_type', None),
            account_id=entity.account_id,
            category_id=entity.category_id,
        )

    def delete_by_filter(self, filter: dict) -> None:
        """
        Override delete to handle payments cascade deletion.
        First deletes all associated payments, then deletes the expense.
        """
        try:
            with self.session_factory() as session:
                # Find the expense
                expense = session.query(self.model).filter_by(**filter).first()
                if not expense:
                    raise ValueError(f'No expense found matching filter {filter}')
                
                # Delete associated payments first
                session.query(PaymentModel).filter_by(expense_id=expense.id).delete()
                
                # Now delete the expense
                session.delete(expense)
                session.commit()
        except Exception as ex:
            logger.error(f'Error deleting expense: {ex.args}')
            raise ex
