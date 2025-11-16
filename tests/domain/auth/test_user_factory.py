import pytest
from uuid import uuid4
from datetime import date

from src.domain.auth.user_factory import UserFactory
from src.domain.auth import User
from src.domain.auth.enums import Role


@pytest.fixture
def valid_user_data() -> dict:
    """Valid data for creating a user."""
    return {
        'id': uuid4(),
        'username': 'testuser',
        'email': 'test@example.com',
        'encrypted_password': 'encrypted_password_hash',
        'role': 'free_user',
        'profile': {
            'id': uuid4(),
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '1990-01-01',
            'preferences': {
                'id': uuid4(),
                'monthly_spending_limit': 1000.0,
            }
        }
    }


def test_create_user_success(valid_user_data: dict) -> None:
    """Test successful creation of a user."""
    user = UserFactory.create(**valid_user_data)
    assert isinstance(user, User)
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'


def test_create_user_invalid_id(valid_user_data: dict) -> None:
    """Test that invalid id raises ValueError."""
    valid_user_data['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='A valid UUID is required to create a User instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_invalid_username_empty(valid_user_data: dict) -> None:
    """Test that empty username raises ValueError."""
    valid_user_data['username'] = ''
    with pytest.raises(ValueError, match='A valid username is required to create a User instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_invalid_email_empty(valid_user_data: dict) -> None:
    """Test that empty email raises ValueError."""
    valid_user_data['email'] = ''
    with pytest.raises(ValueError, match='A valid email is required to create a User instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_invalid_encrypted_password_empty(valid_user_data: dict) -> None:
    """Test that empty encrypted_password raises ValueError."""
    valid_user_data['encrypted_password'] = ''
    with pytest.raises(ValueError, match='A valid encrypted_password is required to create a User instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_invalid_role(valid_user_data: dict) -> None:
    """Test that invalid role raises ValueError."""
    valid_user_data['role'] = 'invalid_role'
    with pytest.raises(ValueError, match='A valid role is required to create a User instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_profile_none(valid_user_data: dict) -> None:
    """Test that None profile raises ValueError."""
    valid_user_data['profile'] = None
    with pytest.raises(ValueError, match='Profile data is required to create a Profile instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_profile_invalid_id(valid_user_data: dict) -> None:
    """Test that invalid profile id raises ValueError."""
    valid_user_data['profile']['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='A valid UUID is required to create a Profile instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_profile_invalid_first_name_empty(valid_user_data: dict) -> None:
    """Test that empty first_name raises ValueError."""
    valid_user_data['profile']['first_name'] = ''
    with pytest.raises(ValueError, match='A valid first_name is required to create a Profile instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_profile_invalid_last_name_empty(valid_user_data: dict) -> None:
    """Test that empty last_name raises ValueError."""
    valid_user_data['profile']['last_name'] = ''
    with pytest.raises(ValueError, match='A valid last_name is required to create a Profile instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_preferences_invalid_id(valid_user_data: dict) -> None:
    """Test that invalid preferences id raises ValueError."""
    valid_user_data['profile']['preferences']['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='A valid UUID is required to create a Preferences instance'):
        UserFactory.create(**valid_user_data)


def test_create_user_preferences_invalid_monthly_spending_limit(valid_user_data: dict) -> None:
    """Test that invalid monthly_spending_limit defaults to 0.0."""
    valid_user_data['profile']['preferences']['monthly_spending_limit'] = 'not-a-number'
    user = UserFactory.create(**valid_user_data)
    assert user.profile.preferences.monthly_spending_limit == 0.0
