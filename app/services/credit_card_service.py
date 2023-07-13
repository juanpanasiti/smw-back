import logging

from app.repositories.credit_card_repository import CreditCardRepository
from app.schemas.credit_card_schemas import CreditCardReq, CreditCardRes

logger = logging.getLogger(__name__)


class CreditCardService():
    def __init__(self) -> None:
        self.__repo = None

    @property
    def repo(self) -> CreditCardRepository:
        if self.__repo is None:
            self.__repo = CreditCardRepository()
        return self.__repo

    def create(self, new_credit_card: CreditCardReq) -> CreditCardRes:
        try:
            credit_card = self.repo.create(new_credit_card.model_dump())
            return CreditCardRes.model_validate(credit_card)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, limit: int, offset: int, search_filter: dict = {}):
        try:
            credit_cards = self.repo.get_many(limit, offset, search_filter)
            return [CreditCardRes.model_validate(cc) for cc in credit_cards]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
