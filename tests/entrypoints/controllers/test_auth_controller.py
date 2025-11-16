import pytest
from uuid import uuid4
from unittest.mock import MagicMock

from src.entrypoints.controllers import AuthController
from src.application.ports import UserRepository
from src.application.dtos import LoginUserDTO, RegisterUserDTO, LoggedInUserDTO
from src.domain.auth.enums.role import Role
from src.entrypoints.exceptions.client_exceptions import Unauthorized, BadRequest, NotFound
from src.entrypoints.exceptions.server_exceptions import InternalServerError

# TODO: manejar fixtures para que devuelvan ok, o errores segun se necesite para el test
@pytest.fixture
def user_repository_mock() -> MagicMock:
    return MagicMock(spec=UserRepository)


@pytest.fixture
def controller(user_repository_mock: MagicMock) -> AuthController:
    return AuthController(user_repository=user_repository_mock)


@pytest.fixture
def login_dto() -> LoginUserDTO:
    return LoginUserDTO(username='testuser', password='secret')


@pytest.fixture
def register_dto() -> RegisterUserDTO:
    return RegisterUserDTO(
        username='newuser',
        email='newuser@example.com',
        password='secret',
        role=Role.FREE_USER,
        first_name='New',
        last_name='User',
    )


@pytest.fixture
def logged_in_dto() -> LoggedInUserDTO:
    return LoggedInUserDTO(
        id=uuid4(),
        username='testuser',
        email='test@example.com',
        role=Role.FREE_USER,
        access_token='token',
    )


# Use case fixtures

@pytest.fixture
def login_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = lambda creds: LoggedInUserDTO(
        id=uuid4(), username=creds.username, email='test@example.com', role=Role.FREE_USER, access_token='ok')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserLoginUseCase', uc_class)
    return uc_instance


@pytest.fixture
def login_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('Invalid email or password')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserLoginUseCase', uc_class)
    return uc_instance


@pytest.fixture
def login_use_case_exception(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = Exception('boom')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserLoginUseCase', uc_class)
    return uc_instance


@pytest.fixture
def register_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = lambda dto: LoggedInUserDTO(
        id=uuid4(), username=dto.username, email=dto.email, role=dto.role, access_token='ok')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserRegisterUseCase', uc_class)
    return uc_instance


@pytest.fixture
def register_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('invalid data')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserRegisterUseCase', uc_class)
    return uc_instance


@pytest.fixture
def renew_use_case_ok(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = lambda dto: LoggedInUserDTO(
        id=dto.id, username=dto.username, email=dto.email, role=dto.role, access_token='new')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserRenewTokenUseCase', uc_class)
    return uc_instance


@pytest.fixture
def renew_use_case_value_error(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    uc_instance: MagicMock = MagicMock()
    uc_instance.execute.side_effect = ValueError('User not found')
    uc_class: MagicMock = MagicMock(return_value=uc_instance)
    monkeypatch.setattr('src.entrypoints.controllers.auth_controller.UserRenewTokenUseCase', uc_class)
    return uc_instance


def test_login_success(controller: AuthController, login_dto: LoginUserDTO, login_use_case_ok: MagicMock) -> None:
    result = controller.login(login_dto)
    assert isinstance(result, LoggedInUserDTO)
    assert result.username == login_dto.username
    assert result.access_token != ''


def test_login_invalid_credentials(controller: AuthController, login_dto: LoginUserDTO, login_use_case_value_error: MagicMock) -> None:
    with pytest.raises(Unauthorized) as exc:
        controller.login(login_dto)
    assert exc.value.status_code == 401
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail.get('code') == 'LOGIN_INVALID_CREDENTIALS'


def test_login_unexpected_error(controller: AuthController, login_dto: LoginUserDTO, login_use_case_exception: MagicMock) -> None:
    with pytest.raises(InternalServerError) as exc:
        controller.login(login_dto)
    assert exc.value.status_code == 500


def test_register_success(controller: AuthController, register_dto: RegisterUserDTO, register_use_case_ok: MagicMock) -> None:
    result = controller.register(register_dto)
    assert isinstance(result, LoggedInUserDTO)
    assert result.username == register_dto.username


def test_register_bad_request(controller: AuthController, register_dto: RegisterUserDTO, register_use_case_value_error: MagicMock) -> None:
    with pytest.raises(BadRequest) as exc:
        controller.register(register_dto)
    assert exc.value.status_code == 400
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail.get('code') == 'REGISTER_BAD_REQUEST'


def test_renew_token_success(controller: AuthController, logged_in_dto: LoggedInUserDTO, renew_use_case_ok: MagicMock) -> None:
    result = controller.renew_token(logged_in_dto)
    assert isinstance(result, LoggedInUserDTO)
    assert result.access_token == 'new'


def test_renew_token_not_found(controller: AuthController, logged_in_dto: LoggedInUserDTO, renew_use_case_value_error: MagicMock) -> None:
    with pytest.raises(NotFound) as exc:
        controller.renew_token(logged_in_dto)
    assert exc.value.status_code == 404
    assert isinstance(exc.value.detail, dict)
    assert exc.value.detail.get('code') == 'USER_NOT_FOUND'
