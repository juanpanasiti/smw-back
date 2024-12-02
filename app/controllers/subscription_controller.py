from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums import ADMIN_ROLES, ExpenseTypeEnum
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.payment_schemas import NewSubscriptionPaymentReq, UpdateSubscriptionPaymentReq, PaymentRes
from app.services import SubscriptionService


class SubscriptionController:
    def __init__(self):
        self.__subscription_service = None

    @property
    def subscription_service(self):
        if self.__subscription_service is None:
            self.__subscription_service = SubscriptionService()
        return self.__subscription_service

    @handle_exceptions
    def create(self, token: DecodedJWT, subscription_id: int, payment: NewSubscriptionPaymentReq) -> PaymentRes:
        subscription_search_filter = {'id': subscription_id, 'type': ExpenseTypeEnum.SUBSCRIPTION.value}
        if token.role not in ADMIN_ROLES:
            subscription_search_filter['user_id'] = token.user_id
        return self.subscription_service.create(payment, subscription_search_filter)

    @handle_exceptions
    def update(self, subscription_id: int, payment_id: int, payment: UpdateSubscriptionPaymentReq) -> PaymentRes:
        updated_payment = self.subscription_service.update(payment, payment_id, subscription_id)
        if updated_payment is None:
            raise ce.NotFound('Payment not found')
        return updated_payment

    @handle_exceptions
    def delete(self,subscription_id: int, payment_id: int) -> None:
        was_deleted = self.subscription_service.delete(payment_id, subscription_id)
        if not was_deleted:
            raise ce.NotFound('Credit card not found')
        