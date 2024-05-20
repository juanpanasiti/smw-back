import logging

from app.repositories.credit_card_repository import CreditCardRepository
from app.schemas.credit_card_schemas import CreditCardReq, CreditCardRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce


logger = logging.getLogger(__name__)


class CreditCardService():
    def __init__(self) -> None:
        self.__repo: CreditCardRepository = None

    @property
    def repo(self) -> CreditCardRepository:
        if self.__repo is None:
            self.__repo = CreditCardRepository()
        return self.__repo

    def create(self, new_credit_card: CreditCardReq) -> CreditCardRes:
        try:
            self._check_main_credit_card(new_credit_card)
            credit_card = self.repo.create(new_credit_card.model_dump())
            return CreditCardRes.model_validate(credit_card)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, limit: int | None = None, offset: int | None = None, search_filter: dict = {}):
        try:
            credit_cards = self.repo.get_many(limit, offset, search_filter)
            return [CreditCardRes.model_validate(cc) for cc in credit_cards]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, cc_id: int, search_filter: dict = {}) -> CreditCardRes:
        try:
            search_filter.update(id=cc_id)
            credit_card = self.repo.get_one(search_filter)
            return CreditCardRes.model_validate(credit_card)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, cc_id: int, credit_card: CreditCardReq, search_filter: dict = {}) -> CreditCardReq:
        try:
            search_filter.update(id=cc_id)
            self._check_main_credit_card(credit_card)
            updated_cc = self.repo.update(credit_card.model_dump(exclude_none=True), search_filter)
            return CreditCardRes.model_validate(updated_cc)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, cc_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(id=cc_id)
            self.repo.get_one(search_filter)
            self.repo.delete(cc_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
        
    def _check_main_credit_card(self, credit_card: CreditCardReq):
        if credit_card.main_credit_card_id is not None:
            main_cc = self.get_by_id(credit_card.main_credit_card_id)
            credit_card.limit = main_cc.limit
            credit_card.next_closing_date = main_cc.next_closing_date
            credit_card.next_expiring_date = main_cc.next_expiring_date
