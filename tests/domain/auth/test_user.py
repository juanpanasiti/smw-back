from uuid import uuid4
from datetime import date

import pytest

from src.domain.auth import User, Role, Profile


def test_user_creation():
    user = User(
        id=uuid4(),
        email='test@example.com',
        username='SomeUsername',
        encrypted_password='encrypted_password',
        role=Role.FREE_USER,
        profile=Profile(
            id=uuid4(),
            first_name='John',
            last_name='Doe',
            birth_date=date(1990, 1, 1)
        )
    )
    assert user.username == 'SomeUsername'
    assert user.email == 'test@example.com'
    assert user.role == Role.FREE_USER
    assert user.profile.first_name == 'John'
    assert user.profile.last_name == 'Doe'
    assert user.profile.birth_date == date(1990, 1, 1)
    assert user.profile.preferences.monthly_spending_limit == 0.0


def test_to_dict():
    user = User(
        id=uuid4(),
        email='test@example.com',
        username='SomeUsername',
        encrypted_password='encrypted_password',
        role=Role.FREE_USER,
        profile=Profile(
            id=uuid4(),
            first_name='John',
            last_name='Doe',
            birth_date=date(1990, 1, 1)
        )
    )
    user_dict = user.to_dict()
    assert user_dict['id'] == str(user.id)
    assert user_dict['email'] == user.email
    assert user_dict['username'] == user.username
    assert user_dict['role'] == Role.FREE_USER.value
    assert user_dict['profile']['first_name'] == user.profile.first_name
    assert user_dict['profile']['last_name'] == user.profile.last_name
    assert user_dict['profile']['birth_date'] == user.profile.birth_date.isoformat()
    assert user_dict['profile']['preferences']['monthly_spending_limit'] == user.profile.preferences.monthly_spending_limit


def test_from_dict():
    data = {
        'id': uuid4(),
        'email': 'test@example.com',
        'username': 'SomeUsername',
        'encrypted_password': 'encrypted_password',
        'role': Role.FREE_USER.value,
        'profile': {
            'id': uuid4(),
            'first_name': 'John',
            'last_name': 'Doe',
            'birth_date': date(1990, 1, 1),
            'preferences': {
                'id': uuid4(),
                'monthly_spending_limit': 0.0
            }
        }
    }
    user = User.from_dict(data)
    assert user.id == data['id']
    assert user.email == data['email']
    assert user.username == data['username']
    assert user.role == data['role']
    assert user.profile.first_name == data['profile']['first_name']
    assert user.profile.last_name == data['profile']['last_name']
    assert user.profile.birth_date == data['profile']['birth_date']
    assert user.profile.preferences.monthly_spending_limit == data['profile']['preferences']['monthly_spending_limit']


def test_set_monthly_spending_limit():
    user = User(
        id=uuid4(),
        email='test@example.com',
        username='SomeUsername',
        encrypted_password='encrypted_password',
        role=Role.FREE_USER,
        profile=Profile(
            id=uuid4(),
            first_name='John',
            last_name='Doe',
            birth_date=date(1990, 1, 1)
        )
    )
    user.profile.set_monthly_spending_limit(100.0)
    assert user.profile.preferences.monthly_spending_limit == 100.0


def test_set_negative_monthly_spending_limit():
    user = User(
        id=uuid4(),
        email='test@example.com',
        username='SomeUsername',
        encrypted_password='encrypted_password',
        role=Role.FREE_USER,
        profile=Profile(
            id=uuid4(),
            first_name='John',
            last_name='Doe',
            birth_date=date(1990, 1, 1)
        )
    )
    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        user.profile.set_monthly_spending_limit(-50.0)
