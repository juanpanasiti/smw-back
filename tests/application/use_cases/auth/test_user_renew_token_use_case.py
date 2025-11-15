from unittest.mock import MagicMock

import pytest

from src.application.use_cases.auth import UserRenewTokenUseCase
from src.application.ports import UserRepository
from src.application.dtos import LoggedInUserDTO
from src.application.helpers import security
from src.domain.auth import Role, User
from ....fixtures.auth_fixtures import user as user_fixture


@pytest.fixture
def logged_in_dto(user_fixture: User) -> LoggedInUserDTO:
    return LoggedInUserDTO(
        id=user_fixture.id,
        username=user_fixture.username,
        email=user_fixture.email,
        role=user_fixture.role,
        access_token='existing_token'
    )


@pytest.fixture
def repo(user_fixture: User) -> UserRepository:
    repo: UserRepository = MagicMock(spec=UserRepository)
    repo.get_by_filter.return_value = user_fixture
    return repo


def test_user_renew_token_use_case_success(logged_in_dto: LoggedInUserDTO, repo: UserRepository):
    use_case = UserRenewTokenUseCase(user_repository=repo)
    result = use_case.execute(logged_in_dto)
    assert isinstance(
        result, LoggedInUserDTO), f'Expected LoggedInUserDTO, got {type(result)}'
    assert result.id == logged_in_dto.id, 'Expected user ID to match'
    assert result.username == logged_in_dto.username, 'Expected username to match'
    assert result.email == logged_in_dto.email, 'Expected email to match'
    assert result.role == logged_in_dto.role, 'Expected role to match'
    assert result.access_token != logged_in_dto.access_token, 'Expected access token to be renewed'


def test_user_renew_token_use_case_user_not_found(logged_in_dto: LoggedInUserDTO):
    repo: UserRepository = MagicMock(spec=UserRepository)
    repo.get_by_filter.return_value = None
    use_case = UserRenewTokenUseCase(user_repository=repo)
    with pytest.raises(ValueError, match='User not found'):
        use_case.execute(logged_in_dto)
