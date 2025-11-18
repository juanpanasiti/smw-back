from unittest.mock import MagicMock

import pytest

from src.application.use_cases.auth import UserLoginUseCase
from src.application.ports import UserRepository, RefreshTokenRepository
from src.application.dtos import LoginUserDTO, LoggedInUserDTO
from src.application.helpers import security
from src.domain.auth import Role, User
from ....fixtures.auth_fixtures import user as user_fixture


@pytest.fixture
def login_dto(user_fixture: User) -> LoginUserDTO:
    return LoginUserDTO(
        username=user_fixture.username,
        password='secure_password',
    )


@pytest.fixture
def repo(user_fixture: User) -> UserRepository:
    repo: UserRepository = MagicMock(spec=UserRepository)
    user_fixture.encrypted_password = security.hash_password('secure_password')
    repo.get_by_filter.return_value = user_fixture
    return repo


@pytest.fixture
def refresh_token_repo() -> RefreshTokenRepository:
    repo: RefreshTokenRepository = MagicMock(spec=RefreshTokenRepository)
    # Mock the create method to return the entity that was passed
    repo.create.side_effect = lambda entity: entity
    return repo


def test_user_login_use_case_success(login_dto: LoginUserDTO, repo: UserRepository, refresh_token_repo: RefreshTokenRepository):
    use_case = UserLoginUseCase(user_repository=repo, refresh_token_repository=refresh_token_repo)
    result = use_case.execute(login_dto)
    assert isinstance(result, LoggedInUserDTO), f'Expected LoggedInUserDTO, got {type(result)}'
    assert result.id is not None, 'Expected non-null user ID'
    assert result.username == login_dto.username, f'Expected username "{login_dto.username}", got {result.username}'
    assert result.role == Role.FREE_USER, f'Expected role {Role.FREE_USER}, got {result.role}'
    assert result.access_token is not None, 'Expected non-null access token'
    assert result.access_token != '', 'Expected non-empty access token'
    assert result.token_type == 'bearer', f'Expected token type "Bearer", got {result.token_type}'
    assert result.refresh_token is not None, 'Expected non-null refresh token'
    assert result.refresh_token != '', 'Expected non-empty refresh token'


def test_user_login_use_case_invalid_username(login_dto: LoginUserDTO, refresh_token_repo: RefreshTokenRepository):
    repo: UserRepository = MagicMock(spec=UserRepository)
    repo.get_by_filter.return_value = None  # Simulate user not found
    use_case = UserLoginUseCase(user_repository=repo, refresh_token_repository=refresh_token_repo)
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(login_dto)
    assert str(
        exc_info.value) == "Invalid username or password", f'Expected ValueError with message "Invalid username or password", got "{str(exc_info.value)}"'


def test_user_login_use_case_invalid_password(login_dto: LoginUserDTO, repo: UserRepository, refresh_token_repo: RefreshTokenRepository):
    login_dto.password = 'wrong_password'  # Simulate wrong password
    use_case = UserLoginUseCase(user_repository=repo, refresh_token_repository=refresh_token_repo)
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(login_dto)
    assert str(
        exc_info.value) == "Invalid username or password", f'Expected ValueError with message "Invalid username or password", got "{str(exc_info.value)}"'
