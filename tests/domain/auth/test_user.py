from uuid import uuid4
from datetime import date

import pytest

from src.domain.auth import User, Role, Profile


@pytest.fixture
def user() -> User:
    return User(
        id=uuid4(),
        email='test@example.com',
        username='SomeUsername',
        encrypted_password='encrypted_password',
        role=Role.FREE_USER,
        profile=Profile(
            id=uuid4(),
            first_name='John',
            last_name='Doe',
            birthdate=date(1990, 1, 1),
            preferences=None,
        )
    )


def test_user_creation(user: User):
    assert user.username == 'SomeUsername'
    assert user.email == 'test@example.com'
    assert user.role == Role.FREE_USER
    assert user.profile.first_name == 'John'
    assert user.profile.last_name == 'Doe'
    assert user.profile.birthdate == date(1990, 1, 1)
    assert user.profile.preferences.monthly_spending_limit == 0.0


def test_to_dict(user: User):
    user_dict = user.to_dict()
    assert user_dict['id'] == str(user.id)
    assert user_dict['email'] == user.email
    assert user_dict['username'] == user.username
    assert user_dict['role'] == Role.FREE_USER.value
    assert user_dict['profile']['first_name'] == user.profile.first_name
    assert user_dict['profile']['last_name'] == user.profile.last_name
    assert user.profile.birthdate is not None
    assert user_dict['profile']['birthdate'] == user.profile.birthdate.isoformat()
    assert user_dict['profile']['preferences']['monthly_spending_limit'] == user.profile.preferences.monthly_spending_limit


def test_set_monthly_spending_limit(user: User):
    user.profile.set_monthly_spending_limit(100.0)
    assert user.profile.preferences.monthly_spending_limit == 100.0


def test_set_negative_monthly_spending_limit(user: User):
    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        user.profile.set_monthly_spending_limit(-50.0)
