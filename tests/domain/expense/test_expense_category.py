from uuid import uuid4

import pytest

from src.domain.expense import ExpenseCategory as Category


@pytest.fixture
def category() -> Category:
    return Category(
        id=uuid4(),
        owner_id=uuid4(),
        name='Groceries',
        description='Expenses for food and household items',
        is_income=False
    )


def test_to_dict(category: Category):
    category_dict = category.to_dict()
    assert isinstance(category_dict, dict)
    assert 'id' in category_dict
    assert 'owner_id' in category_dict
    assert 'name' in category_dict
    assert 'description' in category_dict
    assert 'is_income' in category_dict
    assert isinstance(category_dict['id'], str)
    assert isinstance(category_dict['owner_id'], str)
    assert isinstance(category_dict['name'], str)
    assert isinstance(category_dict['description'], str)
    assert isinstance(category_dict['is_income'], bool)
