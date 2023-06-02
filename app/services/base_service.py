from typing import Callable
from typing import Generic
from typing import List
from typing import TypeVar
from uuid import UUID

from ..database.models import BaseModel
from ..repositories.base_repository import BaseRepository
from app.exceptions.client_exceptions import BadRequest
from app.exceptions.client_exceptions import NotFound
from app.exceptions.repo_exceptions import DatabaseError
from app.exceptions.repo_exceptions import NotFoundError

InputSchemaType = TypeVar('InputSchemaType')
OutputSchemaType = TypeVar('OutputSchemaType')
ModelType = TypeVar('ModelType', bound=BaseModel)
RepoType = TypeVar('RepoType', bound=BaseRepository)


class BaseService(Generic[ModelType, InputSchemaType, OutputSchemaType, RepoType]):
    def __init__(self, RepoClass: Callable):
        self.repo: RepoType = RepoClass()

    def create(self, new_resource_schema: InputSchemaType) -> OutputSchemaType:
        try:
            new_resource_model = self._to_model(new_resource_schema)
            self.repo.create(new_resource_model)

            return self._to_schema(new_resource_model)
        except DatabaseError as dbe:
            # TODO: logger for the error
            raise BadRequest(dbe.message)

    def get_all(self, limit: int = 10, offset: int = 0, search_filter: dict = None) -> List[OutputSchemaType]:
        resource_list = self.repo.get_all(limit, offset, search_filter)

        return [self._to_schema(model_resource) for model_resource in resource_list]

    def get_by_id(self, id: UUID) -> OutputSchemaType:
        try:
            return self._to_schema(self.repo.get_by_id(id))
        except NotFoundError as err:
            raise NotFound('; '.join(err.args))

    def update(self, id: UUID, resource: InputSchemaType) -> OutputSchemaType:
        resource_model = self._to_model(resource)
        resource_model.id = id
        response_model = self.repo.update(resource_model)
        return self._to_schema(response_model)

    def delete(self, id: UUID) -> None:
        try:
            self.repo.delete(id)
            return
        except NotFoundError as err:
            raise NotFound('; '.join(err.args))

    def _to_schema(self, model: ModelType) -> OutputSchemaType:
        raise NotImplementedError(
            'This method must be implemented in subclasses')

    def _to_model(self, schema: InputSchemaType) -> ModelType:
        raise NotImplementedError(
            'This method must be implemented in subclasses')
