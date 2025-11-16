import pytest
from uuid import uuid4
from datetime import date
from unittest.mock import MagicMock

from src.application.use_cases.user import UserUpdateUseCase
from src.application.dtos import UpdateUserDTO, UpdateProfileDTO, UpdatePreferencesDTO, UserResponseDTO
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


def test_user_update_use_case_update_username(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test updating only the username."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(username='newusername')

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert isinstance(result, UserResponseDTO)
    assert sample_user.username == 'newusername'
    user_repository.update.assert_called_once_with(sample_user)


def test_user_update_use_case_update_email(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test updating only the email."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(email='newemail@example.com')

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.email == 'newemail@example.com'
    user_repository.update.assert_called_once()


def test_user_update_use_case_update_password(
    user_repository: MagicMock,
    sample_user: User,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test updating the password."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    
    # Mock hash_password
    mock_hash = MagicMock(return_value='new_hashed_password')
    monkeypatch.setattr('src.application.use_cases.user.user_update_use_case.hash_password', mock_hash)
    
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(password='newpassword123')

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.encrypted_password == 'new_hashed_password'
    mock_hash.assert_called_once_with('newpassword123')
    user_repository.update.assert_called_once()


def test_user_update_use_case_update_profile_name(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test updating profile name."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(
        profile=UpdateProfileDTO(
            first_name='Jane',
            last_name='Smith',
        )
    )

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.profile.first_name == 'Jane'
    assert sample_user.profile.last_name == 'Smith'
    user_repository.update.assert_called_once()


def test_user_update_use_case_update_birthdate(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test updating birthdate."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(
        profile=UpdateProfileDTO(birthdate='1995-05-15')
    )

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.profile.birthdate == date(1995, 5, 15)
    user_repository.update.assert_called_once()


def test_user_update_use_case_invalid_birthdate_format(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test error with invalid birthdate format."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(
        profile=UpdateProfileDTO(birthdate='invalid-date')
    )

    # Act & Assert
    with pytest.raises(ValueError, match='Invalid birthdate format'):
        use_case.execute(sample_user.id, update_data)


def test_user_update_use_case_update_preferences(
    user_repository: MagicMock,
    sample_user: User,
) -> None:
    """Test updating preferences."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(
        profile=UpdateProfileDTO(
            preferences=UpdatePreferencesDTO(monthly_spending_limit=2000.0)
        )
    )

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.profile.preferences.monthly_spending_limit == 2000.0
    user_repository.update.assert_called_once()


def test_user_update_use_case_user_not_found(
    user_repository: MagicMock,
) -> None:
    """Test error when user is not found."""
    # Arrange
    user_repository.get_by_filter.return_value = None
    use_case = UserUpdateUseCase(user_repository)
    user_id = uuid4()
    update_data = UpdateUserDTO(username='newusername')

    # Act & Assert
    with pytest.raises(ValueError, match=f'User with id {user_id} not found'):
        use_case.execute(user_id, update_data)


def test_user_update_use_case_update_multiple_fields(
    user_repository: MagicMock,
    sample_user: User,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test updating multiple fields at once."""
    # Arrange
    user_repository.get_by_filter.return_value = sample_user
    user_repository.update.return_value = sample_user
    
    mock_hash = MagicMock(return_value='new_hashed')
    monkeypatch.setattr('src.application.use_cases.user.user_update_use_case.hash_password', mock_hash)
    
    use_case = UserUpdateUseCase(user_repository)
    update_data = UpdateUserDTO(
        username='newusername',
        email='newemail@test.com',
        password='newpass',
        profile=UpdateProfileDTO(
            first_name='Jane',
            last_name='Smith',
            birthdate='1995-05-15',
            preferences=UpdatePreferencesDTO(monthly_spending_limit=1500.0)
        )
    )

    # Act
    result = use_case.execute(sample_user.id, update_data)

    # Assert
    assert sample_user.username == 'newusername'
    assert sample_user.email == 'newemail@test.com'
    assert sample_user.encrypted_password == 'new_hashed'
    assert sample_user.profile.first_name == 'Jane'
    assert sample_user.profile.last_name == 'Smith'
    assert sample_user.profile.birthdate == date(1995, 5, 15)
    assert sample_user.profile.preferences.monthly_spending_limit == 1500.0
    user_repository.update.assert_called_once()
