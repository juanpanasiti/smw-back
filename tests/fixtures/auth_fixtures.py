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
