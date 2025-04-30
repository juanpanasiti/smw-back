import logging
from typing import List

from app.schemas.payment_schemas_v2 import NewPaymentReqV2, UpdatePaymentReqV2, PaymentResV2, PaymentListParamV2
from app.core.enums.payment_status_enum import PaymentStatusEnum as PaymentStatus
from app.repositories import PaymentRepository


logger = logging.getLogger(__name__)


class PaymentServiceV2:
    def __init__(self):
        self.__payment_repo = None

    @property
    def payment_repo(self):
        if self.__payment_repo is None:
            self.__payment_repo = PaymentRepository()
        return self.__payment_repo

    def create(self, new_payment: NewPaymentReqV2, status: PaymentStatus = PaymentStatus.UNCONFIRMED) -> PaymentResV2:
        new_payment_dict = new_payment.model_dump()
        new_payment_dict['status'] = status.value
        payment = self.payment_repo.create(new_payment_dict)
        return PaymentResV2(**payment)

    def get_list(self, user_id: int | None, expense_id: int | None, params: PaymentListParamV2) -> List[PaymentResV2]:
        params_dict = params.model_dump()
        if params.order_by is not None:
            params_dict['order_by'] = params.order_by.value
        if user_id is not None:
            params_dict['user_id'] = user_id
        if expense_id is not None:
            params_dict['expense_id'] = expense_id
        payments = self.payment_repo.get_many(**params_dict)
        [PaymentResV2(**payment) for payment in payments]

    def get_one(self, search_filter: dict) -> PaymentResV2:
        payment = self.payment_repo.get_one(search_filter)
        return PaymentResV2(**payment) if payment else None

    def update(self, payment: UpdatePaymentReqV2, search_filter: dict) -> PaymentResV2:
        new_data = payment.model_dump(exclude_none=True)
        updated_payment = self.payment_repo.update(new_data, search_filter)
        return PaymentResV2(**updated_payment)

    def delete(self, search_filter: dict) -> bool:
        return self.payment_repo.delete(search_filter)
