import logging
from typing import Generic
from typing import List
from typing import TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy import desc, text

from app.database import db_conn
from app.database.models import BaseModel
from app.exceptions.repo_exceptions import DatabaseError
from app.exceptions.repo_exceptions import UniqueFieldException
from app.exceptions.repo_exceptions import NotFoundError

ModelType = TypeVar('ModelType', bound=BaseModel)
logger = logging.getLogger(__name__)


class BaseRepositoryV1(Generic[ModelType]):
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
        except UniqueViolation as uv:
            raise UniqueFieldException(uv.args)
        except IntegrityError as ie:
            self.db.rollback()
            raise DatabaseError(ie.args)

    def get_many(self, limit: int | None = None, offset: int | None = None, search_filter: dict = {}, order_by:str = 'id', order_asc: bool = True) -> List[ModelType]:
        try:
            order_field = text(order_by) if order_asc else desc(text(order_by))
            query = self.db.query(self.model).order_by(order_field).filter_by(**search_filter)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            return query.all()
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_one(self, search_filter: dict = {}) -> ModelType:
        try:
            result = self.db.query(self.model).filter_by(
                **search_filter).first()
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
            resource_db = self.get_one({'id': resource_id})
            self.db.delete(resource_db)
            self.db.commit()
        except NoResultFound as ex:
            logger.error(ex.args)
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{id}"'
            )
        except Exception as ex:
            logger.critical(ex.args)
            self.db.rollback()
            raise ex
