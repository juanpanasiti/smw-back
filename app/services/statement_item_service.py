import logging

from typing import List

from app.exceptions import repo_exceptions as re, client_exceptions as ce
from app.repositories.statement_item_repository import StatementItemRepository as Repo
from app.schemas.statement_item_schemas import StatementItemRes, StatementItemReq

logger = logging.getLogger(__name__)


class StatementItemService():
    def __init__(self) -> None:
        self.__repo: Repo = None

    @property
    def repo(self) -> Repo:
        if self.__repo is None:
            self.__repo = Repo()
        return self.__repo
    
    def create(self, new_item:StatementItemReq)-> StatementItemRes:
        try:
            created_item = self.repo.create(new_item.model_dump())
            return StatementItemRes.model_validate(created_item)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def get_many(self, limit: int, offset: int, search_filter: dict = {}) -> List[StatementItemRes]:
        try:
            installments = self.repo.get_many(limit, offset, search_filter)
            return [StatementItemRes.model_validate(installment) for installment in installments]
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex
        
    
    def get_by_id(self, item_id: int, search_filter: dict = {}) -> StatementItemRes:
        try:
            search_filter.update(id=item_id)
            statement = self.repo.get_one(search_filter)
            return StatementItemRes.model_validate(statement)
        except re.NotFoundError as err:
            raise ce.NotFound(err.message)
        except Exception as ex:
            logger.error(type(ex))
            logger.critical(ex.args)
            raise ex

    def update(self, item_id: int, item: StatementItemReq, search_filter: dict = {}) -> StatementItemRes:
        try:
            search_filter.update(id=item_id)
            updated_item = self.repo.update(
                item.model_dump(exclude_none=True), search_filter
            )
            return StatementItemRes.model_validate(updated_item)
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
