from ...dtos import LoginUserDTO, LoggedInUserDTO
from ...helpers import security
from ...ports import UserRepository


class UserLoginUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_data: LoginUserDTO) -> LoggedInUserDTO:
        filter = {'username': user_data.username}
        user = self.user_repository.get_by_filter(filter)
        if not user or not security.verify_password(user_data.password, user.encrypted_password):
            raise ValueError('Invalid email or password')
        access_token = security.create_access_token(user)
        return LoggedInUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            access_token=access_token
        )
