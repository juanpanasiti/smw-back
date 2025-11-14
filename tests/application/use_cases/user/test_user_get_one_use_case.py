import pytest
from uuid import uuid4
from datetime import date
from unittest.mock import MagicMock

from src.application.use_cases.user import UserGetOneUseCase
from src.application.dtos import UserResponseDTO
from src.domain.auth import User, Profile, Preferences, Role


@pytest.fixture
def user_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def sample_user() -> User:
    preferences = Preferences(
        id=uuid4(),
        monthly_spending_limit=1000.0,
    )
    profile = Profile(
        id=uuid4(),
        first_name='John',
        last_name='Doe',
        birthdate=date(1990, 1, 1),
        preferences=preferences,
    )
    return User(
        id=uuid4(),
        username='johndoe',
        email='john@example.com',
        encrypted_password='hashed_password',
        role=Role.FREE_USER,
        profile=profile,
    )


def test_user_get_one_use_case_success(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test successfully retrieving a user by ID."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    use_case = UserGetOneUseCase(user_repository)

    # Act
    result = use_case.execute(sample_user.id)

    # Assert
    assert isinstance(result, UserResponseDTO)
    assert result.id == sample_user.id
    assert result.username == sample_user.username
    assert result.email == sample_user.email
    assert result.role == sample_user.role
    assert result.profile.first_name == sample_user.profile.first_name
    assert result.profile.last_name == sample_user.profile.last_name
    if sample_user.profile.birthdate:
        assert result.profile.birthdate == sample_user.profile.birthdate.isoformat()
    assert result.profile.preferences is not None
    assert result.profile.preferences.monthly_spending_limit == 1000.0
    user_repository.get_by_filter.assert_called_once_with({'id': sample_user.id})


def test_user_get_one_use_case_user_not_found(
    user_repository: MagicMock,
) -> None:
    """Test error when user is not found."""
    # Arrange
    user_repository.get_by_filter.return_value = None
    use_case = UserGetOneUseCase(user_repository)
    user_id = uuid4()

    # Act & Assert
    with pytest.raises(ValueError, match=f'User with id {user_id} not found'):
        use_case.execute(user_id)


def test_user_get_one_use_case_without_birthdate(
    user_repository: MagicMock,
) -> None:
    """Test retrieving a user without birthdate."""
    # Arrange
    preferences = Preferences(id=uuid4(), monthly_spending_limit=500.0)
    profile = Profile(
        id=uuid4(),
        first_name='Jane',
        last_name='Smith',
        birthdate=None,
        preferences=preferences,
    )
    user = User(
        id=uuid4(),
        username='janesmith',
        email='jane@example.com',
        encrypted_password='hashed_password',
        role=Role.FREE_USER,
        profile=profile,
    )
    user_repository.get_by_filter.return_value = user
    use_case = UserGetOneUseCase(user_repository)

    # Act
    result = use_case.execute(user.id)

    # Assert
    assert result.profile.birthdate is None
