import logging

from app.exceptions.base_http_exception import BaseHTTPException
from app.exceptions import server_exceptions as se
from app.schemas.expense_schemas import ExepenseListResponse
from app.services.credit_card_service import CreditCardService
from app.services.expense_service import ExpenseService

logger = logging.getLogger(__name__)


class ExpenseController():
    def __init__(self) -> None:
        self.__credit_card_service = None
        self.__expense_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

    @property
    def expense_service(self) -> ExpenseService:
        if self.__expense_service is None:
            self.__expense_service = ExpenseService()
        return self.__expense_service
   
    def get_all(self, user_id: int) -> ExepenseListResponse:
        try:
            response = ExepenseListResponse()
            credit_cards = self.credit_card_service.get_many(search_filter={'user_id': user_id})

            for credit_card in credit_cards:
                response.purchases.extend(self.expense_service.get_many_purchases(search_filter={'credit_card_id': credit_card.id}))
                response.subscriptions.extend(self.expense_service.get_many_subscriptions(search_filter={'credit_card_id': credit_card.id}))

            return response
        except BaseHTTPException as ex:
            logger.error(f'Error getting expenses for user {user_id}: {ex.description}')
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)
