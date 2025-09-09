from uuid import uuid4
from datetime import date

import pytest

from src.domain.auth import Profile


def test_profile_creation():
    profile = Profile(id=uuid4(), first_name='John', last_name='Doe', birth_date=date(1990, 1, 1))

    assert profile.first_name == 'John'
    assert profile.last_name == 'Doe'
    assert profile.birth_date == date(1990, 1, 1)
    assert profile.preferences.monthly_spending_limit == 0.0


def test_set_monthly_spending_limit():
    profile = Profile(id=uuid4(), first_name='Jane', last_name='Doe', birth_date=date(1992, 2, 2))
    profile.set_monthly_spending_limit(300.0)

    assert profile.preferences.monthly_spending_limit == 300.0


def test_to_dict():
    profile = Profile(id=uuid4(), first_name='Alice', last_name='Smith', birth_date=date(1985, 5, 15))
    profile.set_monthly_spending_limit(150.0)
    profile_dict = profile.to_dict()

    assert profile_dict['first_name'] == 'Alice'
    assert profile_dict['last_name'] == 'Smith'
    assert profile_dict['birth_date'] == '1985-05-15'
    assert profile_dict['preferences']['monthly_spending_limit'] == 150.0


def test_from_dict():
    data = {
        'id': uuid4(),
        'first_name': 'Bob',
        'last_name': 'Brown',
        'birth_date': date(1978, 8, 20),
        'preferences': {
            'id': uuid4(),
            'monthly_spending_limit': 400.0
        }
    }
    profile = Profile.from_dict(data)

    assert profile.first_name == 'Bob'
    assert profile.last_name == 'Brown'
    assert profile.birth_date == date(1978, 8, 20)
    assert profile.preferences.monthly_spending_limit == 400.0


def test_from_dict_no_preferences():
    data = {
        'id': uuid4(),
        'first_name': 'Charlie',
        'last_name': 'Davis',
        'birth_date': date(2000, 12, 31)
    }
    profile = Profile.from_dict(data)

    assert profile.first_name == 'Charlie'
    assert profile.last_name == 'Davis'
    assert profile.birth_date == date(2000, 12, 31)
    assert profile.preferences.monthly_spending_limit == 0.0


def test_set_negative_monthly_spending_limit():
    profile = Profile(id=uuid4(), first_name='Eve', last_name='White', birth_date=date(1995, 3, 3))

    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        profile.set_monthly_spending_limit(-100.0)
