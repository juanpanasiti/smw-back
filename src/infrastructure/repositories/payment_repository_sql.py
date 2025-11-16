import logging

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import PaymentModel
from src.domain.expense import PaymentFactory, Payment as PaymentEntity
from src.domain.expense.enums import PaymentStatus
from src.domain.shared import Amount

logger = logging.getLogger(__name__)


class PaymentRepositorySQL(BaseRepositorySQL[PaymentModel, PaymentEntity]):

    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed = ['expense_id', 'no_installment', 'status']
        return {k: v for k, v in params.items() if k in allowed}

    def _parse_model_to_entity(self, data: PaymentModel) -> PaymentEntity:
        return PaymentFactory.create(
            id=data.id,
            expense_id=data.expense_id,
            amount=Amount(data.amount),
            no_installment=data.no_installment,
            status=PaymentStatus(data.status) if not isinstance(data.status, PaymentStatus) else data.status,
            payment_date=data.payment_date,
            is_last_payment=data.is_last_payment,
        )

    def _parse_entity_to_model(self, entity: PaymentEntity) -> PaymentModel:
        return PaymentModel(
            id=entity.id,
            expense_id=entity.expense_id,
            amount=entity.amount.value if hasattr(entity.amount, 'value') else entity.amount,
            no_installment=entity.no_installment,
            status=entity.status.value if hasattr(entity.status, 'value') else entity.status,
            payment_date=entity.payment_date,
            is_last_payment=getattr(entity, 'is_last_payment', False),
        )
