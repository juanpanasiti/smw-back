
from app.exceptions import handle_exceptions
from app.exceptions import client_exceptions as ce
from app.core.enums import ADMIN_ROLES, ExpenseTypeEnum
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.expense_schemas import ExpenseRes
from app.schemas.payment_schemas import UpdatePurchasePaymentReq
from app.services import PurchaseService


class PurchaseController:
    def __init__(self):
        self.__purchase_service = None

    @property
    def purchase_service(self):
        if self.__purchase_service is None:
            self.__purchase_service = PurchaseService()
        return self.__purchase_service

    @handle_exceptions
    def update(self, token: DecodedJWT, purchase_id: int, payment_id: int, payment: UpdatePurchasePaymentReq) -> ExpenseRes:
        purchase_search_filter = {'id': purchase_id, 'type': ExpenseTypeEnum.PURCHASE.value}
        if token.role not in ADMIN_ROLES:
            purchase_search_filter['user_id'] = token.user_id
        expense_res = self.purchase_service.update(payment, payment_id, purchase_search_filter)
        if expense_res is None:
            raise ce.NotFound('Expense not found')
        

        return expense_res
