from uuid import uuid4
from datetime import date

import pytest

from src.domain.auth import Profile


@pytest.fixture
def profile() -> Profile:
    return Profile(id=uuid4(), first_name='John', last_name='Doe', birthdate=date(1990, 1, 1), preferences=None)


def test_profile_creation(profile: Profile):
    assert profile.first_name == 'John'
    assert profile.last_name == 'Doe'
    assert profile.birthdate == date(1990, 1, 1)
    assert profile.preferences.monthly_spending_limit == 0.0


def test_set_monthly_spending_limit(profile: Profile):
    profile.set_monthly_spending_limit(300.0)

    assert profile.preferences.monthly_spending_limit == 300.0


def test_to_dict(profile: Profile):
    profile.set_monthly_spending_limit(150.0)
    profile_dict = profile.to_dict()

    assert profile_dict['first_name'] == 'John'
    assert profile_dict['last_name'] == 'Doe'
    assert profile_dict['birthdate'] == '1990-01-01'
    assert profile_dict['preferences']['monthly_spending_limit'] == 150.0


def test_set_negative_monthly_spending_limit(profile: Profile):
    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        profile.set_monthly_spending_limit(-100.0)
