from ...dtos import LoginUserDTO, LoggedInUserDTO
from ...helpers import security
from ...ports import UserRepository


class UserRenewTokenUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_data: LoggedInUserDTO) -> LoggedInUserDTO:
        filter = {'id': user_data.id}
        user = self.user_repository.get_by_filter(filter)
        if not user:
            raise ValueError("User not found")
        access_token = security.create_access_token(user)
        return LoggedInUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            access_token=access_token
        )
