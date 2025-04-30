import logging

from app.schemas.payment_schemas_v2 import NewSubscriptionPaymentReqV2, UpdateSubscriptionPaymentReqV2, PaymentResV2
from app.core.enums import PaymentStatusEnum as PaymentStatus
from app.repositories import ExpenseRepository, PaymentRepository


logger = logging.getLogger(__name__)


class SubscriptionServiceV2:
    def __init__(self):
        self.__expense_repo = None
        self.__payment_repo = None

    @property
    def expense_repo(self):
        if self.__expense_repo is None:
            self.__expense_repo = ExpenseRepository()
        return self.__expense_repo

    @property
    def payment_repo(self):
        if self.__payment_repo is None:
            self.__payment_repo = PaymentRepository()
        return self.__payment_repo

    def create(self, payment: NewSubscriptionPaymentReqV2, subscription_search_filter: dict) -> PaymentResV2:
        payment_dict = payment.model_dump()
        payment_dict['expense_id'] = subscription_search_filter['id']
        payment_dict['status'] = PaymentStatus.UNCONFIRMED
        payment_dict['no_installment'] = self.__get_next_no_installment(subscription_search_filter['id'])

        new_payment_dict = self.payment_repo.create(payment_dict)
        self.expense_repo.update({'amount': payment.amount}, subscription_search_filter)
        return PaymentResV2(**new_payment_dict)

    def update(self, payment: UpdateSubscriptionPaymentReqV2, payment_id: int, subscription_id) -> PaymentResV2 | None:
        payment_dict = payment.model_dump(exclude_none=True)
        search_filter = {'id': payment_id, 'expense_id': subscription_id}
        updated_payment_dict = self.payment_repo.update(payment_dict, search_filter)
        if payment.amount is not None:
            self.expense_repo.update({'amount': payment.amount}, {'id': subscription_id})
        return PaymentResV2(**updated_payment_dict) if updated_payment_dict else None

    def delete(self, payment_id: int, subscription_id: int) -> bool:
        search_filter = {'id': payment_id, 'expense_id': subscription_id}
        return self.payment_repo.delete(search_filter)

    def __get_next_no_installment(self, subscription_id: int) -> int:
        search_filter = {
            'expense_id': subscription_id,
            'limit': 1,
            'order_by': 'no_installment',
            'order': 'desc'
        }
        payments = self.payment_repo.get_many(**search_filter)
        if not payments:
            return 1

        return max(payment['no_installment'] for payment in payments)
