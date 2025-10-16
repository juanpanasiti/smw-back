import logging
from typing import TypeVar, Generic
from abc import abstractmethod

from sqlalchemy.exc import IntegrityError
# from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import sessionmaker, Query, Session
from sqlalchemy import desc, text

from src.application.ports import BaseRepository
from src.domain.shared import EntityBase
from ..database import db_conn
from ..database.models import BaseModel
# from app.exceptions.repo_exceptions import DatabaseError, UniqueFieldException

ModelType = TypeVar('ModelType', bound=BaseModel)
EntityType = TypeVar('EntityType', bound=EntityBase)
logger = logging.getLogger(__name__)


class BaseRepositorySQL(BaseRepository[EntityType], Generic[ModelType, EntityType]):
    VALID_ORDER_BY_FIELDS = ['id', 'created_at', 'updated_at']

    def __init__(self, model: type[ModelType], session_factory: sessionmaker = db_conn.SessionLocal) -> None:
        self.session_factory: sessionmaker[Session] = session_factory
        self.model: type[ModelType] = model

    def count_by_filter(self, filter: dict = {}) -> int:
        try:
            with self.session_factory() as session:
                count = session.query(self.model).filter_by(**filter).count()
                return count
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def create(self, entity: EntityType) -> EntityType:
        try:
            with self.session_factory() as session:
                new_resource: BaseModel = self._parse_entity_to_model(entity)
                session.add(new_resource)
                session.commit()
                session.refresh(new_resource)
                return self._parse_model_to_entity(new_resource)
        # except UniqueViolation as uv:
        #     logger.error(f'{self.model} - create - {uv.args} - New resource: {entity.to_dict()}')
        #     raise UniqueFieldException(uv.args)
        # except IntegrityError as ie:
        #     logger.error(f'{self.model} - create - {ie.args}')
        #     raise DatabaseError(ie.args)
        except Exception as ex:
            logger.critical(f'{self.model} - create - {ex.args}')
            raise ex

    def get_many_by_filter(self, filter: dict, limit: int, offset: int) -> list[EntityType]:
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                if filter.get('order_by'):
                    query = query.order_by(self._get_order_by_params(filter))
                search_filter = self._get_filter_params(filter)
                if search_filter:
                    query = query.filter_by(**search_filter)
                query = query.limit(limit)
                query = query.offset(offset)
                result_list: list[ModelType] = query.all()
                return [self._parse_model_to_entity(item) for item in result_list]
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_by_filter(self, filter: dict) -> EntityType | None:
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                query = query.filter_by(**filter)
                result: ModelType | None = query.first()
                return self._parse_model_to_entity(result) if result else None
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def update(self, entity: EntityType) -> EntityType:
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                query = query.filter_by(id=entity.id)
                existing_data: ModelType | None = query.first()
                if not existing_data:
                    raise ValueError(f'No record found with id {entity.id}')
                for field, value in entity.to_dict().items():
                    if isinstance(value, dict):
                        continue
                    setattr(existing_data, field, value)
                session.commit()
                return self._parse_model_to_entity(existing_data)
        except IntegrityError as err:
            logger.error(err.args)
            logger.error(f'Data with error: {str(entity.to_dict())}')
            raise err
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def delete_by_filter(self, filter: dict) -> None:
        try:
            with self.session_factory() as session:
                query: Query = session.query(self.model)
                query = query.filter_by(**filter)
                deleted_count: int = query.delete()
                if deleted_count == 0:
                    raise ValueError(f'No records found matching filter {filter}')
                session.commit()
        except Exception as ex:
            logger.critical(ex.args)
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

    @abstractmethod
    def _parse_model_to_entity(self, data: ModelType) -> EntityType:
        pass

    @abstractmethod
    def _parse_entity_to_model(self, entity: EntityType) -> ModelType:
        pass
