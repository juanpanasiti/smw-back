from re import sub
from uuid import uuid4

import pytest

from src.domain.expense import ExpenseCategory as Category, ExpenseCategoryFactory as Factory
from src.domain.auth import User
from src.domain.shared import Amount


@pytest.fixture
def category_dict() -> dict:
    return {
        'id': uuid4(),
        'name': 'Groceries',
        'description': 'Grocery shopping',
        'is_income': False,
        'owner_id': uuid4(),
    }


def test_create_category(category_dict):
    category = Factory.create(**category_dict)
    assert isinstance(category, Category)
    assert category.id == category_dict['id']
    assert category.name == category_dict['name']
    assert category.description == category_dict['description']
    assert category.is_income == category_dict['is_income']
    assert category.owner_id == category_dict['owner_id']
