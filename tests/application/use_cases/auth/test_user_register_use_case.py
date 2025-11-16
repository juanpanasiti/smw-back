from unittest.mock import MagicMock

import pytest

from src.application.use_cases.auth import UserRegisterUseCase
from src.application.ports import UserRepository
from src.application.dtos import RegisterUserDTO, LoggedInUserDTO
from src.application.helpers import security
from src.domain.auth import Role, User
from ....fixtures.auth_fixtures import user as user_fixture

@pytest.fixture
def register_dto(user_fixture: User) -> RegisterUserDTO:
    return RegisterUserDTO(
        username=user_fixture.username,
        email=user_fixture.email,
        password='secure_password',
        role=Role.FREE_USER,
        first_name=user_fixture.profile.first_name,
        last_name=user_fixture.profile.last_name,
    )

@pytest.fixture
def repo(user_fixture: User) -> UserRepository:
    repo: UserRepository = MagicMock(spec=UserRepository)
    user_fixture.encrypted_password = security.hash_password('secure_password')
    repo.create.return_value = user_fixture
    return repo

def test_user_register_use_case_success(register_dto: RegisterUserDTO, repo: UserRepository):
    use_case = UserRegisterUseCase(user_repository=repo)
    result = use_case.execute(register_dto)
    assert isinstance(result, LoggedInUserDTO), f'Expected LoggedInUserDTO, got {type(result)}'
    assert result.id is not None, 'Expected non-null user ID'
    assert result.username == register_dto.username, f'Expected username "{register_dto.username}", got {result.username}'
    assert result.email == register_dto.email, f'Expected email "{register_dto.email}", got {result.email}'
    assert result.role == Role.FREE_USER, f'Expected role {Role.FREE_USER}, got {result.role}'
    assert result.access_token is not None, 'Expected non-null access token'
    assert result.access_token != '', 'Expected non-empty access token'
    assert result.token_type == 'bearer', f'Expected token type "Bearer", got {result.token_type}'
