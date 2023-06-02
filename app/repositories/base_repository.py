import logging
from typing import Generic
from typing import List
from typing import TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..database import db_conn
from ..database.models import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)
logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session = db_conn.session) -> None:
        self.db = db
        self.model = ModelType
        self.DEFAULT_FILTER = {'is_deleted': False}

    def create(self, new_resource: ModelType) -> None:
        try:
            self.db.add(new_resource)
            self.db.commit()
            self.db.refresh(new_resource)
        except IntegrityError as ie:
            logger.error(ie.args)
            raise ie
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_all(self, limit: int, offset: int, search_filter: dict = None) -> List[ModelType]:
        if search_filter is None:
            search_filter = self.DEFAULT_FILTER
        else:
            search_filter.update(self.DEFAULT_FILTER)
        try:
            return self.db.query(self.model).filter_by(**search_filter).offset(offset).limit(limit).all()
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_one_by_filter(self, search_filter: dict = None) -> ModelType | None:
        if search_filter is None:
            search_filter = self.DEFAULT_FILTER
        else:
            search_filter.update(self.DEFAULT_FILTER)
        try:
            return self.db.query(self.model).filter_by(**search_filter).first()
        except NoResultFound as nf:
            logger.error(nf.args)
            return None
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_by_id(self, id: int, search_filter: dict = None) -> ModelType:
        if search_filter is None:
            search_filter = self.DEFAULT_FILTER

        query = self.db.query(self.model).filter_by(id=id, **search_filter)
        try:
            return query.one()
        except NoResultFound as nf:
            logger.error(nf.args)
            raise nf
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def get_list_by_filter(self, search_filter: dict) -> List[ModelType]:
        query = self.db.query(self.model).filter_by(**search_filter)
        try:
            return query.all()
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def update(self, new_data: ModelType, search_filter: dict = None) -> ModelType:
        if search_filter is None:
            search_filter = self.DEFAULT_FILTER
        try:
            current_resource: ModelType = self.db.query(
                self.model).filter_by(id=new_data.id, **search_filter).one()
            current_resource.update_data(new_data)
            self.db.commit()
            return current_resource
        except NoResultFound as nf:
            logger.error(nf.args)
            raise nf
        except Exception as ex:
            logger.critical(ex.args)
            raise ex

    def delete(self, id: int) -> None:

        try:
            resource = self.get_by_id(id)
            if resource:
                resource.is_deleted = True
                self.update(resource)
        except Exception as ex:
            logger.critical(ex.args)
            raise ex
