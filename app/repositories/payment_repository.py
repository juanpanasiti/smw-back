from .base_repository import BaseRepository
from app.database.models import PaymentModel
from app.core.enums import SortablePaymentFieldsEnum


class PaymentRepository(BaseRepository[PaymentModel]):
    VALID_ORDER_BY_FIELDS: list[str] = [field.value for field in SortablePaymentFieldsEnum]

    def __init__(self) -> None:
        super().__init__()
        self.model = PaymentModel

    def _get_filter_params(self, params=...) -> dict:
        user_id = params.get('user_id')
        filter_params = {}
        if user_id is not None:
            filter_params['user_id'] = user_id
        return filter_params
