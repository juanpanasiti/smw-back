from uuid import uuid4

import pytest

from src.domain.auth import Preferences


def test_set_monthly_spending_limit():
    prefs = Preferences(id=uuid4(), monthly_spending_limit=100.0)

    assert prefs.monthly_spending_limit == 100.0
    prefs.monthly_spending_limit = 200.0
    assert prefs.monthly_spending_limit == 200.0


def test_set_negative_monthly_spending_limit():
    prefs = Preferences(id=uuid4(), monthly_spending_limit=100.0)

    with pytest.raises(ValueError, match='Monthly spending limit cannot be negative'):
        prefs.monthly_spending_limit = -50.0


def test_to_dict():
    prefs = Preferences(id=uuid4(), monthly_spending_limit=150.0)
    prefs_dict = prefs.to_dict()

    assert prefs_dict['monthly_spending_limit'] == 150.0


def test_from_dict():
    data = {
        'id': uuid4(),
        'monthly_spending_limit': 250.0
    }
    prefs = Preferences.from_dict(data)

    assert prefs.monthly_spending_limit == 250.0
    assert prefs.id == data['id']
