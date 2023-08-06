import logging

from typing import List

from app.repositories.credit_card_statement_repository import CreditCardStatementRepository as Repo
from app.schemas.credit_card_statement_schemas import NewCCStatementReq, CCStatementReq, CCStatementRes
from app.exceptions import repo_exceptions as re, client_exceptions as ce

logger = logging.getLogger(__name__)


class CreditCardStatementService():
    def __init__(self) -> None:
        self.__repo: Repo = None

    @property
    def repo(self) -> Repo:
        if self.__repo is None:
            self.__repo = Repo()
        return self.__repo

    def create(self, new_statement: CCStatementReq) -> CCStatementRes:
        try:
            created_statement = self.repo.create(new_statement.model_dump())
            return CCStatementRes.model_validate(created_statement)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, limit: int, offset: int, search_filter: dict = {}) -> List[CCStatementRes]:
        try:
            statements = self.repo.get_many(limit, offset, search_filter)
            return [CCStatementRes.model_validate(statement) for statement in statements]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, statement_id: int, search_filter: dict = {}) -> CCStatementRes:
        try:
            search_filter.update(id=statement_id)
            statement = self.repo.get_one(search_filter)
            return CCStatementRes.model_validate(statement)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, statement_id: int, statement: CCStatementReq, search_filter: dict = {}) -> CCStatementRes:
        try:
            search_filter.update(id=statement_id)
            updated_statement = self.repo.update(
                statement.model_dump(exclude_none=True), search_filter
            )
            return CCStatementRes.model_validate(updated_statement)
        except re.NotFoundError as err:
            ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def delete(self, statement_id: int, search_filter: dict = {}) -> None:
        try:
            search_filter.update(id=statement_id)
            self.repo.get_one(search_filter)
            self.repo.delete(statement_id)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
