import logging
from typing import List

from app.repositories.payment_repository import PaymentRepository as PaymentRepo
from app.schemas.payment_schemas import PaymentReq, PaymentRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce

logger = logging.getLogger(__name__)


class PaymentService():
    def __init__(self) -> None:
        self.__repo: PaymentRepo = None

    @property
    def repo(self) -> PaymentRepo:
        if self.__repo is None:
            self.__repo = PaymentRepo()
        return self.__repo

    def create(self, new_payment: PaymentReq) -> PaymentRes:
        try:
            payment_dict = new_payment.model_dump()
            payment = self.repo.create(payment_dict)
            return PaymentRes.model_validate(payment)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, limit: int, offset: int, search_filter: dict = {}) -> List[PaymentRes]:
        try:
            payments = self.repo.get_many(limit, offset, search_filter)
            return [PaymentRes.model_validate(payment) for payment in payments]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, payment_id: int, search_filter: dict = {}) -> PaymentRes:
        try:
            search_filter.update(id=payment_id)
            payment = self.repo.get_one(search_filter)
            return PaymentRes.model_validate(payment)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, payment_id: int, payment: PaymentReq, search_filter: dict = {}) -> PaymentRes:
        try:
            search_filter.update(id=payment_id)
            updated_payment = self.repo.update(
                payment.model_dump(exclude_none=True), search_filter)
            return PaymentRes.model_validate(updated_payment)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, payment_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(id=payment_id)
            self.repo.get_one(search_filter)
            self.repo.delete(payment_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
