from uuid import uuid4

import pytest

from src.domain.expense import ExpenseCategory as Category, ExpenseCategoryFactory as Factory


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


def test_create_category_invalid_id_none(category_dict):
    """Test category creation fails with None id."""
    category_dict['id'] = None
    with pytest.raises(ValueError, match='id must be a UUID'):
        Factory.create(**category_dict)


def test_create_category_invalid_id_type(category_dict):
    """Test category creation fails with invalid id type."""
    category_dict['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='id must be a UUID'):
        Factory.create(**category_dict)


def test_create_category_invalid_name_none(category_dict):
    """Test category creation fails with None name."""
    category_dict['name'] = None
    with pytest.raises(ValueError, match='name must be a non-empty string'):
        Factory.create(**category_dict)


def test_create_category_invalid_name_empty(category_dict):
    """Test category creation fails with empty name."""
    category_dict['name'] = '   '
    with pytest.raises(ValueError, match='name must be a non-empty string'):
        Factory.create(**category_dict)


def test_create_category_invalid_owner_id_none(category_dict):
    """Test category creation fails with None owner_id."""
    category_dict['owner_id'] = None
    with pytest.raises(ValueError, match='owner_id must be a UUID'):
        Factory.create(**category_dict)


def test_create_category_invalid_owner_id_type(category_dict):
    """Test category creation fails with invalid owner_id type."""
    category_dict['owner_id'] = 123
    with pytest.raises(ValueError, match='owner_id must be a UUID'):
        Factory.create(**category_dict)


def test_create_category_invalid_description_none(category_dict):
    """Test category creation fails with None description."""
    category_dict['description'] = None
    with pytest.raises(ValueError, match='description must be a string'):
        Factory.create(**category_dict)


def test_create_category_invalid_description_type(category_dict):
    """Test category creation fails with invalid description type."""
    category_dict['description'] = 123
    with pytest.raises(ValueError, match='description must be a string'):
        Factory.create(**category_dict)


def test_create_category_invalid_is_income_none(category_dict):
    """Test category creation fails with None is_income."""
    category_dict['is_income'] = None
    with pytest.raises(ValueError, match='is_income must be a boolean'):
        Factory.create(**category_dict)


def test_create_category_invalid_is_income_type(category_dict):
    """Test category creation fails with invalid is_income type."""
    category_dict['is_income'] = 'yes'
    with pytest.raises(ValueError, match='is_income must be a boolean'):
        Factory.create(**category_dict)
