
from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums import ADMIN_ROLES, ExpenseTypeEnum
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.expense_schemas_v2 import ExpenseResV2
from app.schemas.payment_schemas_v2 import UpdatePurchasePaymentReqV2
from app.services import PurchaseServiceV2


class PurchaseControllerV2:
    def __init__(self):
        self.__purchase_service = None

    @property
    def purchase_service(self):
        if self.__purchase_service is None:
            self.__purchase_service = PurchaseServiceV2()
        return self.__purchase_service

    @handle_exceptions
    def update(self, token: DecodedJWT, purchase_id: int, payment_id: int, payment: UpdatePurchasePaymentReqV2) -> ExpenseResV2:
        purchase_search_filter = {'id': purchase_id, 'type': ExpenseTypeEnum.PURCHASE.value}
        if token.role not in ADMIN_ROLES:
            purchase_search_filter['user_id'] = token.user_id
        expense_res = self.purchase_service.update(payment, payment_id, purchase_search_filter)
        if expense_res is None:
            raise ce.NotFound('Expense not found', 'EXPENSE_NOT_FOUND')
        

        return expense_res
