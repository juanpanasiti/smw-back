import pytest
from uuid import uuid4
from unittest.mock import MagicMock

from src.entrypoints.controllers import UserController
from src.application.dtos import UpdateUserDTO, UserResponseDTO, ProfileResponseDTO, PreferencesResponseDTO, UpdateProfileDTO
from src.entrypoints.exceptions.client_exceptions import NotFound, BadRequest
from src.entrypoints.exceptions.server_exceptions import InternalServerError
from src.domain.auth import Role


@pytest.fixture
def user_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def controller(user_repository: MagicMock) -> UserController:
    return UserController(user_repository)


@pytest.fixture
def user_response_dto() -> UserResponseDTO:
    preferences_dto = PreferencesResponseDTO(
        id=uuid4(),
        monthly_spending_limit=1000.0,
    )
    profile_dto = ProfileResponseDTO(
        id=uuid4(),
        first_name='John',
        last_name='Doe',
        birthdate='1990-01-01',
        preferences=preferences_dto,
    )
    return UserResponseDTO(
        id=uuid4(),
        username='johndoe',
        email='john@example.com',
        role=Role.FREE_USER,
        profile=profile_dto,
    )


def test_get_user_success(
    controller: UserController,
    user_response_dto: UserResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test successfully getting a user."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.return_value = user_response_dto
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserGetOneUseCase', use_case_class)

    # Act
    result = controller.get_user(user_response_dto.id)

    # Assert
    assert isinstance(result, UserResponseDTO)
    assert result.id == user_response_dto.id
    assert result.username == user_response_dto.username
    use_case_instance.execute.assert_called_once_with(user_response_dto.id)


def test_get_user_not_found(
    controller: UserController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test error when user is not found."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = ValueError('User not found')
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserGetOneUseCase', use_case_class)

    user_id = uuid4()

    # Act & Assert
    with pytest.raises(NotFound, match='User not found'):
        controller.get_user(user_id)


def test_get_user_internal_error(
    controller: UserController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test internal server error."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = Exception('Database error')
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserGetOneUseCase', use_case_class)

    user_id = uuid4()

    # Act & Assert
    with pytest.raises(InternalServerError):
        controller.get_user(user_id)


def test_update_user_success(
    controller: UserController,
    user_response_dto: UserResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test successfully updating a user."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.return_value = user_response_dto
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserUpdateUseCase', use_case_class)

    update_data = UpdateUserDTO(username='newusername')

    # Act
    result = controller.update_user(user_response_dto.id, update_data)

    # Assert
    assert isinstance(result, UserResponseDTO)
    use_case_instance.execute.assert_called_once_with(user_response_dto.id, update_data)


def test_update_user_not_found(
    controller: UserController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test error when user to update is not found."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = ValueError('User with id xyz not found')
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserUpdateUseCase', use_case_class)

    user_id = uuid4()
    update_data = UpdateUserDTO(username='newusername')

    # Act & Assert
    with pytest.raises(NotFound):
        controller.update_user(user_id, update_data)


def test_update_user_bad_request(
    controller: UserController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test bad request error."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = ValueError('Invalid birthdate format')
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserUpdateUseCase', use_case_class)

    user_id = uuid4()
    update_data = UpdateUserDTO(username='test')

    # Act & Assert
    with pytest.raises(BadRequest):
        controller.update_user(user_id, update_data)


def test_update_user_internal_error(
    controller: UserController,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test internal server error during update."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.side_effect = Exception('Database error')
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserUpdateUseCase', use_case_class)

    user_id = uuid4()
    update_data = UpdateUserDTO(username='newusername')

    # Act & Assert
    with pytest.raises(InternalServerError):
        controller.update_user(user_id, update_data)


def test_update_user_profile_only(
    controller: UserController,
    user_response_dto: UserResponseDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test updating only profile information."""
    # Arrange
    use_case_instance = MagicMock()
    use_case_instance.execute.return_value = user_response_dto
    use_case_class = MagicMock(return_value=use_case_instance)
    monkeypatch.setattr('src.entrypoints.controllers.user_controller.UserUpdateUseCase', use_case_class)

    update_data = UpdateUserDTO(
        profile=UpdateProfileDTO(
            first_name='Jane',
            last_name='Smith',
        )
    )

    # Act
    result = controller.update_user(user_response_dto.id, update_data)

    # Assert
    assert isinstance(result, UserResponseDTO)
    use_case_instance.execute.assert_called_once_with(user_response_dto.id, update_data)
