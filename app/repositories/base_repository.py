import logging
from typing import Generic, List, TypeVar
from abc import ABC, abstractmethod

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session, Query
from sqlalchemy import desc, text

from app.database import db_conn
from app.database.models import BaseModel
from app.exceptions.repo_exceptions import DatabaseError, UniqueFieldException

ModelType = TypeVar('ModelType', bound=BaseModel)
logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelType], ABC):
    VALID_ORDER_BY_FIELDS = ['id', 'created_at', 'updated_at']

    def __init__(self, db: Session = db_conn.session) -> None:
        self.db = db
        self.model = ModelType

    def count(self, search_filter: dict = {}) -> int:
        try:
            count = self.db.query(self.model).filter_by(**search_filter).count()
            return count
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def create(self, new_resource_dict: dict) -> dict:
        try:
            new_resource: BaseModel = self.model()
            for field in new_resource_dict.keys():
                setattr(new_resource, field, new_resource_dict[field])

            self.db.add(new_resource)
            self.db.commit()
            self.db.refresh(new_resource)
            return new_resource.to_dict()
        except UniqueViolation as uv:
            logger.error(f'{self.model} - create - {uv.args} - New resource: {new_resource_dict}')
            raise UniqueFieldException(uv.args)
        except IntegrityError as ie:
            logger.error(f'{self.model} - create - {ie.args}')
            self.db.rollback()
            raise DatabaseError(ie.args)
        except Exception as ex:
            logger.critical(f'{self.model} - create - {ex.args}')
            self.db.rollback()
            raise ex

    def get_many(self, **kwargs) -> list[dict]:
        try:
            limit = kwargs.get('limit')
            offset = kwargs.get('offset')
            query: Query = self.db.query(self.model)
            if kwargs.get('order_by'):
                query = query.order_by(self._get_order_by_params(kwargs))
            search_filter = self._get_filter_params(kwargs)
            if search_filter:
                query = query.filter_by(**search_filter)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            result_list: List[ModelType] = query.all()
            return [result.to_dict() for result in result_list]
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_one(self, search_filter: dict, include_relationships: bool = False):
        try:
            query: Query = self.db.query(self.model)
            query = query.filter_by(**search_filter)
            result: ModelType = query.first()
            return result.to_dict(include_relationships) if result is not None else None
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def update(self, new_data: dict, search_filter: dict) -> dict | None:
        try:
            query: Query = self.db.query(self.model)
            query = query.filter_by(**search_filter)
            resource_db: ModelType = query.first()
            if resource_db is None:
                return None
            for field in new_data.keys():
                setattr(resource_db, field, new_data[field])
            self.db.commit()
            return resource_db.to_dict()
        except IntegrityError as err:
            logger.error(err.args)
            logger.error(f'Data with error: {str(new_data)}')
            self.db.rollback()
            raise err
        except Exception as ex:
            logger.critical(ex.args)
            self.db.rollback()
            raise ex

    def delete(self, search_filter: dict) -> bool:
        try:
            query: Query = self.db.query(self.model)
            query = query.filter_by(**search_filter)
            deleted_count: int = query.delete()
            if deleted_count == 0:
                return False
            
            self.db.commit()
            return True
        except Exception as ex:
            logger.critical(ex.args)
            self.db.rollback()
            raise ex

    def _get_order_by_params(self, params: dict = {}):
        order_by = params.get('order_by')
        order_asc = params.get('order_asc')

        if order_by is None:
            order_by = 'id'
        if order_asc is None:
            order_asc = True

        if order_by not in self.VALID_ORDER_BY_FIELDS:
            raise ValueError(f'Invalid order_by field: {order_by}')

        return text(order_by) if order_asc else desc(text(order_by))

    @abstractmethod
    def _get_filter_params(self, params: dict = {}) -> dict:
        pass
