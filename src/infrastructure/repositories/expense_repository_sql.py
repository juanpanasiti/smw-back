import logging
from datetime import date

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import ExpenseModel, PaymentModel
from src.domain.expense import (
    PurchaseFactory,
    SubscriptionFactory,
    ExpenseType,
    Expense as ExpenseEntity,
)
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class ExpenseRepositorySQL(BaseRepositorySQL[ExpenseModel, ExpenseEntity]):
    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['account_id', 'category_id', 'expense_type', 'status']
        return {k: v for k, v in params.items() if k in allowed}

    def _parse_model_to_entity(self, data: ExpenseModel):
        # choose factory by expense_type
        factory = PurchaseFactory if data.expense_type == ExpenseType.PURCHASE.value else SubscriptionFactory
        payments = [
            {
                'id': p.id,
                'expense_id': p.expense_id,
                'amount': p.amount,
                'no_installment': p.no_installment,
                'status': p.status,
                'payment_date': p.payment_date,
                'is_last_payment': p.is_last_payment,
            }
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
