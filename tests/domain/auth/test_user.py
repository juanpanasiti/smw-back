from datetime import date

import pytest

from src.domain.auth import User, Role
from ...fixtures.auth_fixtures import user as user_fixture


def test_user_creation(user_fixture: User):
    assert user_fixture.username == 'SomeUsername'
    assert user_fixture.email == 'test@example.com'
    assert user_fixture.role == Role.FREE_USER
    assert user_fixture.profile.first_name == 'John'
    assert user_fixture.profile.last_name == 'Doe'
    assert user_fixture.profile.birthdate == date(1990, 1, 1)
    assert user_fixture.profile.preferences.monthly_spending_limit == 0.0


def test_to_dict(user_fixture: User):
    user_dict = user_fixture.to_dict()
    assert user_dict['id'] == str(user_fixture.id)
    assert user_dict['email'] == user_fixture.email
    assert user_dict['username'] == user_fixture.username
    assert user_dict['role'] == Role.FREE_USER.value
    assert user_dict['profile']['first_name'] == user_fixture.profile.first_name
    assert user_dict['profile']['last_name'] == user_fixture.profile.last_name
    assert user_fixture.profile.birthdate is not None
    assert user_dict['profile']['birthdate'] == user_fixture.profile.birthdate.isoformat()
    assert user_dict['profile']['preferences']['monthly_spending_limit'] == user_fixture.profile.preferences.monthly_spending_limit


def test_set_monthly_spending_limit(user_fixture: User):
    user_fixture.profile.set_monthly_spending_limit(100.0)
    assert user_fixture.profile.preferences.monthly_spending_limit == 100.0


def test_set_negative_monthly_spending_limit(user_fixture: User):
    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        user_fixture.profile.set_monthly_spending_limit(-50.0)
