import logging
from typing import Generic
from typing import List
from typing import TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.database import db_conn
from app.database.models import BaseModel
from app.exceptions.repo_exceptions import DatabaseError
from app.exceptions.repo_exceptions import NotFoundError

ModelType = TypeVar('ModelType', bound=BaseModel)
logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelType]):
    DEFAULT_FILTER = {'is_deleted': False}

    def __init__(self, db: Session = db_conn.session) -> None:
        self.db = db
        self.model = ModelType

    def create(self, new_resource_dict: dict) -> ModelType:
        try:
            new_resource = self.model()
            for field in new_resource_dict.keys():
                setattr(new_resource, field, new_resource_dict[field])

            self.db.add(new_resource)
            self.db.commit()
            self.db.refresh(new_resource)
            return new_resource
        except IntegrityError as ie:
            self.db.rollback()
            raise DatabaseError(ie.args)

    def get_many(self, limit: int, offset: int, search_filter: dict = {}) -> List[ModelType]:
        search_filter = dict(**self.DEFAULT_FILTER, **search_filter)

        try:
            return self.db.query(self.model).filter_by(**search_filter).offset(offset).limit(limit).all()
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_one(self, search_filter: dict = {}) -> ModelType:
        filter = dict(**self.DEFAULT_FILTER)
        filter.update(search_filter)
        try:
            result = self.db.query(self.model).filter_by(**filter).first()
            if not result:
                raise NoResultFound(f'No resource found with this creiteria: {search_filter}')
            return result
        except NoResultFound as nf:
            logger.error(nf.args)
            raise NotFoundError(f'No resource found with this creiteria: {search_filter}')
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, resource_id: int) -> ModelType:
        try:
            return self.get_one({'id': resource_id})
        except NoResultFound as nf:
            logger.error(nf.args)
            raise NotFoundError(f'No resource found with id #{resource_id}')
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def update(self, new_data: dict, search_filter: dict = {}) -> ModelType:
        search_filter = dict(**self.DEFAULT_FILTER, **search_filter)
        try:
            resource_db = self.get_one(search_filter)
            for field in new_data.keys():
                setattr(resource_db, field, new_data[field])
            self.db.commit()
            return resource_db
        except NoResultFound as ex:
            logger.error(ex.args)
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{id}"'
            )
        except IntegrityError as err:
            logger.error(err.args)
            logger.error(f'Data with error: {str(new_data)}')
            self.db.rollback()
            raise err
        except Exception as ex:
            logger.critical(ex.args)
            self.db.rollback()
            raise ex

    def delete(self, resource_id: int) -> None:
        try:
            self.update({'is_deleted': True}, {'id': resource_id})
        except Exception as ex:
            logger.critical(ex.args)
            raise ex
