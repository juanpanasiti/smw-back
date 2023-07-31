import logging
from typing import List

from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.credit_card_schemas import NewCreditCardReq, CreditCardReq, CreditCardRes
from app.services.credit_card_service import CreditCardService
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


class CreditCardController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__credit_card_service = None

    @property
    def credit_card_service(self) -> CreditCardService:
        if self.__credit_card_service is None:
            self.__credit_card_service = CreditCardService()
        return self.__credit_card_service

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    def create(self, user_id: int, new_credit_card: NewCreditCardReq) -> CreditCardRes:
        try:
            self.user_service.get_by_id(user_id)

            credit_card_data = CreditCardReq(
                user_id=user_id,
                **new_credit_card.model_dump(exclude_none=True),
            )

            return self.credit_card_service.create(credit_card_data)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_paginated(self, user_id: int, limit: int, offset: int) -> List[CreditCardRes]:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_many(limit, offset, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_by_id(self, user_id: int, cc_id: int) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.get_by_id(cc_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def update(self, user_id: int, cc_id: int, credit_card: CreditCardReq) -> CreditCardRes:
        try:
            search_filter = {'user_id': user_id}
            return self.credit_card_service.update(cc_id, credit_card, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_one(self, user_id: int, cc_id: int) -> None:
        try:
            search_filter = {'user_id': user_id}
            self.credit_card_service.delete(cc_id, search_filter)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)
