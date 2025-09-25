from uuid import uuid4

from src.domain.auth import UserFactory
from ...dtos import RegisterUserDTO, LoggedInUserDTO
from ...helpers import security
from ...ports import UserRepository


class UserRegisterUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_data: RegisterUserDTO) -> LoggedInUserDTO:
        user_dict = self.__get_user_dict(user_data)
        user = UserFactory.create(**user_dict)
        user = self.user_repository.create(user)
        access_token = security.create_access_token(user)
        return LoggedInUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            access_token=access_token
        )

    def __get_user_dict(self, user_data: RegisterUserDTO) -> dict:
        return {
            'id': uuid4(),
            'username': user_data.username,
            'email': user_data.email,
            'encrypted_password': security.hash_password(user_data.password),
            'role': user_data.role.value,
            'profile': self.__get_profile_dict(user_data)
        }

    def __get_profile_dict(self, user_data: RegisterUserDTO) -> dict:
        return {
            'id': uuid4(),
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'birthdate': None,
            'preferences': None,
        }
