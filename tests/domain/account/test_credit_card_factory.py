import pytest
from uuid import uuid4
from datetime import date

from src.domain.account.credit_card_factory import CreditCardFactory
from src.domain.account import CreditCard
from src.domain.shared import Amount


@pytest.fixture
def valid_credit_card_data() -> dict:
    """Valid data for creating a credit card."""
    return {
        'id': uuid4(),
        'owner_id': uuid4(),
        'alias': 'Test Card',
        'limit': Amount(5000.0),
        'is_enabled': True,
        'main_credit_card_id': None,
        'next_closing_date': date(2025, 12, 15),
        'next_expiring_date': date(2025, 12, 25),
        'financing_limit': Amount(3000.0),
        'expenses': [],
    }


def test_create_credit_card_success(valid_credit_card_data: dict) -> None:
    """Test successful creation of a credit card."""
    credit_card = CreditCardFactory.create(**valid_credit_card_data)
    assert isinstance(credit_card, CreditCard)
    assert credit_card.alias == 'Test Card'


def test_create_credit_card_invalid_id(valid_credit_card_data: dict) -> None:
    """Test that invalid id raises ValueError."""
    valid_credit_card_data['id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='id must be a UUID'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_owner_id(valid_credit_card_data: dict) -> None:
    """Test that invalid owner_id raises ValueError."""
    valid_credit_card_data['owner_id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='owner_id must be a UUID'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_alias_empty(valid_credit_card_data: dict) -> None:
    """Test that empty alias raises ValueError."""
    valid_credit_card_data['alias'] = ''
    with pytest.raises(ValueError, match='alias must be a non-empty string'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_limit(valid_credit_card_data: dict) -> None:
    """Test that invalid limit raises ValueError."""
    valid_credit_card_data['limit'] = 5000.0
    with pytest.raises(ValueError, match='limit must be an instance of Amount'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_is_enabled(valid_credit_card_data: dict) -> None:
    """Test that invalid is_enabled raises ValueError."""
    valid_credit_card_data['is_enabled'] = 'true'
    with pytest.raises(ValueError, match='is_enabled must be a boolean'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_main_credit_card_id(valid_credit_card_data: dict) -> None:
    """Test that invalid main_credit_card_id raises ValueError."""
    valid_credit_card_data['main_credit_card_id'] = 'not-a-uuid'
    with pytest.raises(ValueError, match='main_credit_card_id must be a UUID'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_next_closing_date(valid_credit_card_data: dict) -> None:
    """Test that invalid next_closing_date raises ValueError."""
    valid_credit_card_data['next_closing_date'] = '2025-12-15'
    with pytest.raises(ValueError, match='next_closing_date must be a date'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_next_expiring_date(valid_credit_card_data: dict) -> None:
    """Test that invalid next_expiring_date raises ValueError."""
    valid_credit_card_data['next_expiring_date'] = '2025-12-25'
    with pytest.raises(ValueError, match='next_expiring_date must be a date'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_financing_limit(valid_credit_card_data: dict) -> None:
    """Test that invalid financing_limit raises ValueError."""
    valid_credit_card_data['financing_limit'] = 3000.0
    with pytest.raises(ValueError, match='financing_limit must be a positive number'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_expenses_not_list(valid_credit_card_data: dict) -> None:
    """Test that non-list expenses raises ValueError."""
    valid_credit_card_data['expenses'] = 'not-a-list'
    with pytest.raises(ValueError, match='expenses must be a list'):
        CreditCardFactory.create(**valid_credit_card_data)


def test_create_credit_card_invalid_expenses_wrong_type(valid_credit_card_data: dict) -> None:
    """Test that expenses with non-Expense items raises ValueError."""
    valid_credit_card_data['expenses'] = ['not-an-expense']
    with pytest.raises(ValueError, match='all items in expenses must be instances of Expense'):
        CreditCardFactory.create(**valid_credit_card_data)
