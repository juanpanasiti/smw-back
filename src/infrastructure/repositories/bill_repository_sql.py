import logging
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Query, joinedload

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import ExpenseModel, PaymentModel, AccountModel
from src.domain.expense import (
    BillFactory,
    PaymentFactory,
    PaymentStatus,
    ExpenseType,
    BillFrequency,
    Bill as BillEntity,
)
from src.application.ports import BillRepository
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class BillRepositorySQL(BaseRepositorySQL[ExpenseModel, BillEntity], BillRepository):
    """Repository for Bill expenses (stored in expenses table with expense_type='bill')."""

    def create(self, entity: BillEntity) -> BillEntity:
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
                    session.query(ExpenseModel)
                    .options(joinedload(ExpenseModel.payments))
                    .filter_by(id=expense_model.id)
                    .one()
                )
                return self._parse_model_to_entity(created_expense)
        except Exception as ex:
            logger.error(f'Error creating bill: {ex.args}')
            raise ex

    def update(self, entity: BillEntity) -> BillEntity:
        """Update a Bill and its associated payments."""
        try:
            with self.session_factory() as session:
                expense_model = session.query(ExpenseModel).filter_by(id=entity.id).first()
                if not expense_model:
                    raise ValueError(f'Bill with id {entity.id} not found')
                
                # Update bill fields
                expense_model.title = entity.description
                expense_model.acquired_at = entity.date
                expense_model.amount = entity.amount.value if hasattr(entity.amount, 'value') else entity.amount
                expense_model.frequency = entity.frequency.value
                expense_model.next_bill_month = entity.next_bill_month
                expense_model.next_bill_year = entity.next_bill_year
                expense_model.notes = entity.notes
                
                # Flush before deleting payments
                session.flush()
                
                # Update payments - delete old ones and create new ones
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
                    session.query(ExpenseModel)
                    .options(joinedload(ExpenseModel.payments))
                    .filter_by(id=entity.id)
                    .one()
                )
                return self._parse_model_to_entity(updated_expense)
        except Exception as ex:
            logger.error(f'Error updating bill: {ex.args}')
            raise ex

    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['account_id', 'frequency', 'owner_id']
        return {k: v for k, v in params.items() if k in allowed}

    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[BillEntity]:
        """
        Override to handle owner_id filtering and ensure only Bill expenses are returned.
        """
        try:
            with self.session_factory() as session:
                query: Query = session.query(ExpenseModel)
                
                # Only get Bill expenses
                query = query.filter(ExpenseModel.expense_type == ExpenseType.BILL.value)
                
                # Handle owner_id separately with JOIN
                owner_id = filter.get('owner_id')
                if owner_id:
                    query = query.join(AccountModel, ExpenseModel.account_id == AccountModel.id)
                    query = query.filter(AccountModel.owner_id == owner_id)
                
                # Apply other filters
                search_filter = self._get_filter_params(filter)
                search_filter.pop('owner_id', None)
                
                if search_filter:
                    for key, value in search_filter.items():
                        query = query.filter(getattr(ExpenseModel, key) == value)
                
                query = query.options(joinedload(ExpenseModel.payments))
                query = query.order_by(ExpenseModel.acquired_at.desc())
                query = query.limit(limit)
                query = query.offset(offset)
                
                result_list: list[ExpenseModel] = query.all()
                return [self._parse_model_to_entity(item) for item in result_list]
        except Exception as ex:
            logger.error(f'Error in get_many_by_filter: {ex.args}')
            raise ex

    def count_by_filter(self, filter: dict = {}) -> int:
        """Override to handle owner_id filtering and ensure only Bill expenses are counted."""
        try:
            with self.session_factory() as session:
                query: Query = session.query(ExpenseModel)
                
                # Only count Bill expenses
                query = query.filter(ExpenseModel.expense_type == ExpenseType.BILL.value)
                
                owner_id = filter.get('owner_id')
                if owner_id:
                    query = query.join(AccountModel, ExpenseModel.account_id == AccountModel.id)
                    query = query.filter(AccountModel.owner_id == owner_id)
                
                search_filter = self._get_filter_params(filter)
                search_filter.pop('owner_id', None)
                
                if search_filter:
                    for key, value in search_filter.items():
                        query = query.filter(getattr(ExpenseModel, key) == value)
                
                return query.count()
        except Exception as ex:
            logger.error(f'Error in count_by_filter: {ex.args}')
            raise ex

    def get_upcoming_bills(
        self,
        owner_id: UUID,
        year: int | None = None,
        month: int | None = None
    ) -> list[BillEntity]:
        """Get bills with next_bill_month/year matching the given period."""
        try:
            with self.session_factory() as session:
                query: Query = session.query(ExpenseModel)
                query = query.filter(ExpenseModel.expense_type == ExpenseType.BILL.value)
                
                if year is not None:
                    query = query.filter(ExpenseModel.next_bill_year == year)
                if month is not None:
                    query = query.filter(ExpenseModel.next_bill_month == month)
                
                query = query.join(AccountModel, ExpenseModel.account_id == AccountModel.id)
                query = query.filter(AccountModel.owner_id == str(owner_id))
                
                query = query.options(joinedload(ExpenseModel.payments))
                
                result_list: list[ExpenseModel] = query.all()
                return [self._parse_model_to_entity(item) for item in result_list]
        except Exception as ex:
            logger.error(f'Error in get_upcoming_bills: {ex.args}')
            raise ex

    def _parse_model_to_entity(self, data: ExpenseModel) -> BillEntity:
        """Convert ExpenseModel to Bill domain entity."""
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
        
        return BillFactory.create(
            id=data.id,
            account_id=data.account_id,
            description=data.title,  # title maps to description
            amount=Amount(data.amount),
            date=data.acquired_at,  # acquired_at maps to date
            frequency=BillFrequency(data.frequency) if data.frequency else BillFrequency.MONTHLY,
            next_bill_month=data.next_bill_month,
            next_bill_year=data.next_bill_year,
            notes=data.notes or '',
            payments=payments,
        )

    def _parse_entity_to_model(self, entity: BillEntity) -> ExpenseModel:
        """Convert Bill domain entity to ExpenseModel."""
        return ExpenseModel(
            id=entity.id,
            title=entity.description,  # description maps to title
            cc_name='',  # Bills don't have cc_name, use empty string
            acquired_at=entity.date,  # date maps to acquired_at
            amount=entity.amount.value if hasattr(entity.amount, 'value') else entity.amount,
            expense_type=ExpenseType.BILL.value,
            installments=1,  # Bills are typically single payment
            first_payment_date=entity.date,  # Use same date
            status='active',  # Default status
            spent_type=None,
            account_id=entity.account_id,
            category_id=None,  # Bills don't have categories
            frequency=entity.frequency.value,
            next_bill_month=entity.next_bill_month,
            next_bill_year=entity.next_bill_year,
            notes=entity.notes,
        )

    def delete_by_filter(self, filter: dict) -> None:
        """Delete a bill and its associated payments."""
        try:
            with self.session_factory() as session:
                expense = session.query(ExpenseModel).filter_by(**filter).first()
                if not expense:
                    raise ValueError(f'No bill found matching filter {filter}')
                
                # Verify it's a Bill expense
                if expense.expense_type != ExpenseType.BILL.value:
                    raise ValueError(f'Expense {filter} is not a Bill')
                
                # Delete associated payments first
                session.query(PaymentModel).filter_by(expense_id=expense.id).delete()
                
                # Delete the expense
                session.delete(expense)
                session.commit()
        except Exception as ex:
            logger.error(f'Error deleting bill: {ex.args}')
            raise ex
