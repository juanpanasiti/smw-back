from app.database.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserRequest
from app.schemas.user_schemas import UserResponse
from .base_service import BaseService


class UserService(BaseService[UserModel, UserRequest, UserResponse, UserRepository]):
    def __init__(self):
        super().__init__(UserRepository)

    def _to_model(self, schema: UserRequest) -> UserModel:
        return super()._to_model(schema)

    def _to_schema(self, model: UserModel) -> UserResponse:
        return super()._to_schema(model)
